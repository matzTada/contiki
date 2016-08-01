/*
 * Copyright (c) 2015, Swedish Institute of Computer Science.
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 * 1. Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 * 3. Neither the name of the Institute nor the names of its contributors
 *    may be used to endorse or promote products derived from this software
 *    without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE INSTITUTE AND CONTRIBUTORS ``AS IS'' AND
 * ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED.  IN NO EVENT SHALL THE INSTITUTE OR CONTRIBUTORS BE LIABLE
 * FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
 * DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
 * OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
 * HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
 * LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
 * OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
 * SUCH DAMAGE.
 *
 */
/**
 * \file
 *         Orchestra: a slotframe dedicated to unicast data transmission.
 *         If sender-based:
 *           Nodes listen at a timeslot defined as hash(MAC) % ORCHESTRA_SB_UNICAST_PERIOD
 *           Nodes transmit at: for each nbr in RPL children and RPL preferred parent,
 *                                             hash(nbr.MAC) % ORCHESTRA_SB_UNICAST_PERIOD
 *         If receiver-based: the opposite
 *
 * \author Simon Duquennoy <simonduq@sics.se>
 */

#include "contiki.h"
#include "orchestra.h"
#include "net/ipv6/uip-ds6-route.h"
#include "net/packetbuf.h"

#if ORCHESTRA_UNICAST_SENDER_BASED && ORCHESTRA_COLLISION_FREE_HASH
#define UNICAST_SLOT_SHARED_FLAG    ((ORCHESTRA_UNICAST_PERIOD < (ORCHESTRA_MAX_HASH + 1)) ? LINK_OPTION_SHARED : 0)
#else
#define UNICAST_SLOT_SHARED_FLAG      LINK_OPTION_SHARED
#endif

static uint16_t slotframe_handle = 0;
static uint16_t channel_offset = 0;
static struct tsch_slotframe *sf_unicast;

/*---------------------------------------------------------------------------*/
static uint16_t
get_node_timeslot(const linkaddr_t *addr)
{
  if(addr != NULL && ORCHESTRA_UNICAST_PERIOD > 0) {
#ifdef CONDUCT_ORCHESTRA
#ifdef WITH_OVERHEARING
    return (ORCHESTRA_LINKADDR_HASH(addr) - 1) % CONDUCT_UNICAST_OFFSET + CONDUCT_EBSF_OFFSET + 1; //to obey to the standard?
#else //WITH_OVERHEARING
    return (ORCHESTRA_LINKADDR_HASH(addr) - 1) % (ORCHESTRA_UNICAST_PERIOD - 1 - CONDUCT_EBSF_OFFSET) + CONDUCT_EBSF_OFFSET + 1; //for my proposal. frequent.
#endif //WITH_OVERHEARING
#else //CONDUCT_ORCHESTRA
    return ORCHESTRA_LINKADDR_HASH(addr) % ORCHESTRA_UNICAST_PERIOD;
#endif
  } else {
    return 0xffff;
  }
}
/*---------------------------------------------------------------------------*/
#ifdef WITH_OVERHEARING
static uint16_t
get_node_timeslot_by_id(char id){
  if(id >= 0){
#ifdef CONDUCT_ORCHESTRA
    return (id - 1) % CONDUCT_UNICAST_OFFSET + CONDUCT_EBSF_OFFSET + 1;
#else//CONDUCT_ORECHESTRA
    return id % ORCHESTRA_LEAPFROG_ALT_TRAFFIC_PERIOD;
#endif //CONDUCT_ORCHESTRA
  }else{
    return 0xffff;
  }
}
#endif //WITH_OVERHEARING
/*---------------------------------------------------------------------------*/
static int
neighbor_has_uc_link(const linkaddr_t *linkaddr)
{
//#ifdef CONDUCT_ORCHESTRA
//  return 1;
//#else //CONDUCT_ORCHESTRA
  if(linkaddr != NULL && !linkaddr_cmp(linkaddr, &linkaddr_null)) {
    if((orchestra_parent_knows_us || !ORCHESTRA_UNICAST_SENDER_BASED)
       && linkaddr_cmp(&orchestra_parent_linkaddr, linkaddr)) {
      return 1;
    }
    if(nbr_table_get_from_lladdr(nbr_routes, (linkaddr_t *)linkaddr) != NULL) {
      return 1;
    }
  }
  return 0;
//#endif //CONDUCT_ORCHESTRA
}
//#ifndef CONDUCT_ORCHESTRA
/*---------------------------------------------------------------------------*/
static void
add_uc_link(const linkaddr_t *linkaddr)
{
  if(linkaddr != NULL) {
    uint16_t timeslot = get_node_timeslot(linkaddr);
    tsch_schedule_add_link(
        sf_unicast,
        ORCHESTRA_UNICAST_SENDER_BASED ? LINK_OPTION_RX : LINK_OPTION_TX | UNICAST_SLOT_SHARED_FLAG,
        LINK_TYPE_NORMAL, 
        &tsch_broadcast_address, //linkaddr,
        timeslot, 
        channel_offset);
  }
}
/*---------------------------------------------------------------------------*/
static void
remove_uc_link(const linkaddr_t *linkaddr)
{
  uint16_t timeslot;
  struct tsch_link *l;

  if(linkaddr == NULL) {
    return;
  }

  timeslot = get_node_timeslot(linkaddr);
  l = tsch_schedule_get_link_by_timeslot(sf_unicast, timeslot);
  if(l == NULL) {
    return;
  }
  /* Does our current parent need this timeslot? */
  if(timeslot == get_node_timeslot(&orchestra_parent_linkaddr)) {
    /* Yes, this timeslot is being used, return */
    return;
  }
  /* Does any other child need this timeslot?
   * (lookup all route next hops) */
  nbr_table_item_t *item = nbr_table_head(nbr_routes);
  while(item != NULL) {
    linkaddr_t *addr = nbr_table_get_lladdr(nbr_routes, item);
    if(timeslot == get_node_timeslot(addr)) {
      /* Yes, this timeslot is being used, return */
      return;
    }
    item = nbr_table_next(nbr_routes, item);
  }
  tsch_schedule_remove_link(sf_unicast, l);
}
/*---------------------------------------------------------------------------*/
static void
child_added(const linkaddr_t *linkaddr)
{
  add_uc_link(linkaddr);
}
/*---------------------------------------------------------------------------*/
static void
child_removed(const linkaddr_t *linkaddr)
{
  remove_uc_link(linkaddr);
}
/*---------------------------------------------------------------------------*/
//#endif //ifndef CONDUCT_ORCHESTRA
/*---------------------------------------------------------------------------*/
static int
select_packet(uint16_t *slotframe, uint16_t *timeslot)
{
  /* Select data packets we have a unicast link to */
  const linkaddr_t *dest = packetbuf_addr(PACKETBUF_ADDR_RECEIVER);
  if(packetbuf_attr(PACKETBUF_ATTR_FRAME_TYPE) == FRAME802154_DATAFRAME
     && neighbor_has_uc_link(dest)) {
    if(slotframe != NULL) {
      *slotframe = slotframe_handle;
    }
    if(timeslot != NULL) {
      *timeslot = ORCHESTRA_UNICAST_SENDER_BASED ? get_node_timeslot(&linkaddr_node_addr) : get_node_timeslot(dest);
    }
    return 1;
  }
  return 0;
}
/*---------------------------------------------------------------------------*/
static void
new_time_source(const struct tsch_neighbor *old, const struct tsch_neighbor *new)
{
  if(new != old) {
    const linkaddr_t *new_addr = new != NULL ? &new->addr : NULL; //if(new!=NULL){new_addr=&new->addr}else{new_addr=NULL}
    if(new_addr != NULL) {
      linkaddr_copy(&orchestra_parent_linkaddr, new_addr);
    } else {
      linkaddr_copy(&orchestra_parent_linkaddr, &linkaddr_null);
    }
//#ifdef CONDUCT_ORCHESTRA
//    orchestra_conduct_add_uc_link(&linkaddr_node_addr, LINK_OPTION_TX);
//#else //CONDUCT_ORCHESTRA
    remove_uc_link(new_addr);
    add_uc_link(new_addr);
//#endif //CONDUCT_ORCHESTRA
  }
}
/*---------------------------------------------------------------------------*/
static void
init(uint16_t sf_handle)
{
  slotframe_handle = sf_handle;
  channel_offset = sf_handle;
//  channel_offset = 0;
  /* Slotframe for unicast transmissions */
  sf_unicast = tsch_schedule_add_slotframe(slotframe_handle, ORCHESTRA_UNICAST_PERIOD);
  uint16_t timeslot = get_node_timeslot(&linkaddr_node_addr);
  tsch_schedule_add_link(sf_unicast,
            ORCHESTRA_UNICAST_SENDER_BASED ? LINK_OPTION_TX | UNICAST_SLOT_SHARED_FLAG: LINK_OPTION_RX,
            LINK_TYPE_NORMAL, &tsch_broadcast_address,
            timeslot, channel_offset);
}
/*---------------------------------------------------------------------------*/
struct orchestra_rule unicast_per_neighbor = {
  init,
  new_time_source,
  select_packet,
  child_added,
  child_removed,
};
/*---------------------------------------------------------------------------*/
#ifdef CONDUCT_ORCHESTRA
// to get Tx slot based on own ID
void
orchestra_conduct_add_uc_link(const linkaddr_t *linkaddr, uint8_t link_option)
{
  uint16_t timeslot = get_node_timeslot(linkaddr);

  struct tsch_link *l;
  l = tsch_schedule_get_link_by_timeslot(sf_unicast, timeslot);
  if(l != NULL) {
    tsch_schedule_remove_link(sf_unicast, l);
  }

  tsch_schedule_add_link(
    sf_unicast,
    link_option,
    LINK_TYPE_NORMAL,
    &tsch_broadcast_address, //&altparent_linkaddr, //dest linkaddr
    timeslot,
    channel_offset); //should be modified to get correct channel_offset of link
}
#endif //CONDUCT_ORCHESTRA

#ifdef WITH_LEAPFROG_TSCH
/*---------------------------------------------------------------------------*/
void
orchestra_unicast_add_uc_rx_link(char child_id, uint8_t link_option)
{
  uint16_t parent_timeslot = 0;
  parent_timeslot = get_node_timeslot_by_id(child_id);
  //altparent_timeslot = (child_id + CONDUCT_EBSF_OFFSET) % ORCHESTRA_LEAPFROG_ALT_TRAFFIC_PERIOD; //like ORCHESTRA_LINKADDR_HASH(linkaddr)%PERIOD

  struct tsch_link *parent_l;
  parent_l = tsch_schedule_get_link_by_timeslot(sf_unicast, parent_timeslot);
  if(parent_l != NULL) {
    tsch_schedule_remove_link(sf_unicast, parent_l);
  }
  tsch_schedule_add_link(
    sf_unicast,
    link_option, //here should be LINK_OPTION_RX or LINK_OPTION_PROMISCUOUS_RX
    LINK_TYPE_NORMAL,
    &tsch_broadcast_address, //welcome everyone
    parent_timeslot,
    channel_offset); //should be modified to get correct channel_offset of link
}
#endif //WITH_OVERHEARING
