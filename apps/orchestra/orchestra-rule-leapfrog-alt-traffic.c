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
 *         Orchestra: a slotframe dedicated to leapfrog alt traffic.
 *
 * \author Tadanori Matsui
 * \modified from orchestra-rule-unicast-per-neighbor.c
 * \date started 15/June/2016
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
static struct tsch_slotframe *sf_lfat; //leapfrog alt traffic

/*---------------------------------------------------------------------------*/
static uint16_t
get_node_timeslot(const linkaddr_t *addr)
{
  if(addr != NULL && ORCHESTRA_LEAPFROG_ALT_TRAFFIC_PERIOD > 0) {
    return ORCHESTRA_LINKADDR_HASH(addr) % ORCHESTRA_LEAPFROG_ALT_TRAFFIC_PERIOD;
  } else {
    return 0xffff;
  }
}
/*---------------------------------------------------------------------------*/
static int
neighbor_has_uc_link(const linkaddr_t *linkaddr)
{
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
}
/*---------------------------------------------------------------------------*/
static void
child_added(const linkaddr_t *linkaddr)
{
  // add_uc_link(linkaddr);
}
/*---------------------------------------------------------------------------*/
static void
child_removed(const linkaddr_t *linkaddr)
{
  // remove_uc_link(linkaddr);
}
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
}
/*---------------------------------------------------------------------------*/
static void
init(uint16_t sf_handle)
{
  slotframe_handle = sf_handle;
  channel_offset = sf_handle;
  /* Slotframe for Leapfrog alt traffic */
  sf_lfat = tsch_schedule_add_slotframe(slotframe_handle, ORCHESTRA_LEAPFROG_ALT_TRAFFIC_PERIOD);
}
/*---------------------------------------------------------------------------*/
struct orchestra_rule leapfrog_alt_traffic = {
  init,
  new_time_source,
  select_packet,
  child_added,
  child_removed,
};
/*---------------------------------------------------------------------------*/
void
orchestra_leapfrog_add_uc_tx_link(char alt_parent_id)
{
  uint16_t child_timeslot = 0;
  child_timeslot = linkaddr_node_addr.u8[7] % ORCHESTRA_LEAPFROG_ALT_TRAFFIC_PERIOD; //like ORCHESTRA_LINKADDR_HASH(linkaddr)%PERIOD
  linkaddr_t altparent_linkaddr = {{0xc1, 0x0c, 0, 0, 0, 0, 0, alt_parent_id}};

  struct tsch_link *child_l;
  child_l = tsch_schedule_get_link_by_timeslot(sf_lfat, child_timeslot);
  if(child_l != NULL) {
    tsch_schedule_remove_link(sf_lfat, child_l);
  }

  tsch_schedule_add_link(
    sf_lfat,
    LINK_OPTION_TX | LINK_OPTION_SHARED,
    LINK_TYPE_NORMAL,
    &tsch_broadcast_address,
//    &altparent_linkaddr, //dest linkaddr
    child_timeslot,
    channel_offset); //should be modified to get correct channel_offset of link
}
/*---------------------------------------------------------------------------*/
void
orchestra_leapfrog_add_uc_rx_link(char child_id)
{
  uint16_t altparent_timeslot = child_id % ORCHESTRA_LEAPFROG_ALT_TRAFFIC_PERIOD; //like ORCHESTRA_LINKADDR_HASH(linkaddr)%PERIOD

  struct tsch_link *altparent_l;
  altparent_l = tsch_schedule_get_link_by_timeslot(sf_lfat, altparent_timeslot);
  if(altparent_l != NULL) {
    tsch_schedule_remove_link(sf_lfat, altparent_l);
  }
  tsch_schedule_add_link(
    sf_lfat,
    LINK_OPTION_RX,
    LINK_TYPE_NORMAL,
    &tsch_broadcast_address, //welcome everyone
    altparent_timeslot,
    channel_offset); //should be modified to get correct channel_offset of link
}
