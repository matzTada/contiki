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

#ifdef WITH_LEAPFROG_TSCH
static uint16_t slotframe_handle = 0;
static uint16_t channel_offset = 0;
static struct tsch_slotframe *sf_lfat; //leapfrog alt traffic
#endif //WITH_LEAPFROG_TSCH

/*---------------------------------------------------------------------------*/
static void
init(uint16_t sf_handle)
{
#ifdef WITH_LEAPFROG_TSCH
  slotframe_handle = sf_handle;
  channel_offset = sf_handle;
//  channel_offset = 0;
  /* Slotframe for Leapfrog alt traffic */
  sf_lfat = tsch_schedule_add_slotframe(slotframe_handle, ORCHESTRA_LEAPFROG_ALT_TRAFFIC_PERIOD);
#endif //WITH_LEAPFROG_TSCH
}
/*---------------------------------------------------------------------------*/
struct orchestra_rule leapfrog_alt_traffic = {
  init,
  NULL, //new_time_source,
  NULL, //select_packet,
  NULL, //child_added,
  NULL, //child_removed,
};
/*---------------------------------------------------------------------------*/
#ifdef WITH_LEAPFROG_TSCH
static uint16_t
get_node_timeslot_by_id(char id){
  if(id >= 0){
#ifdef CONDUCT_ORCHESTRA
#ifdef WITH_OVERHEARING
    return (id - 1) % CONDUCT_ALT_OFFSET + CONDUCT_UNICAST_OFFSET + CONDUCT_EBSF_OFFSET + 1;
#else //WITH_OVERHEARING
    return (id - 1 + CONDUCT_ALT_TRAFFIC_DRIFT_OFFSET) % (ORCHESTRA_LEAPFROG_ALT_TRAFFIC_PERIOD - 1 - CONDUCT_EBSF_OFFSET) + CONDUCT_EBSF_OFFSET + 1;
#endif //WITH_OVERHEARING
#else//CONDUCT_ORECHESTRA
    return id % ORCHESTRA_LEAPFROG_ALT_TRAFFIC_PERIOD;
#endif //CONDUCT_ORCHESTRA
  }else{
    return 0xffff;
  }
}
/*---------------------------------------------------------------------------*/
//to test the alt traffic slot in unicast frame
void
orchestra_leapfrog_add_uc_tx_link(char alt_parent_id)
{
  uint16_t child_timeslot = 0;
  child_timeslot = get_node_timeslot_by_id(linkaddr_node_addr.u8[7]);
  //child_timeslot = (linkaddr_node_addr.u8[7] + CONDUCT_EBSF_OFFSET) % ORCHESTRA_LEAPFROG_ALT_TRAFFIC_PERIOD; //like ORCHESTRA_LINKADDR_HASH(linkaddr)%PERIOD
  //  linkaddr_t altparent_linkaddr = {{0xc1, 0x0c, 0, 0, 0, 0, 0, alt_parent_id}};

  struct tsch_link *child_l;
  child_l = tsch_schedule_get_link_by_timeslot(sf_lfat, child_timeslot);
  if(child_l != NULL) {
    tsch_schedule_remove_link(sf_lfat, child_l);
  }

  tsch_schedule_add_link(
    sf_lfat,
    LINK_OPTION_TX | LINK_OPTION_SHARED,
    LINK_TYPE_NORMAL,
    &tsch_broadcast_address, //    &altparent_linkaddr, //dest linkaddr
    child_timeslot, 
    channel_offset); //should be modified to get correct channel_offset of link
}
/*---------------------------------------------------------------------------*/
void
orchestra_leapfrog_add_uc_rx_link(char child_id, uint8_t link_option)
{
  uint16_t altparent_timeslot = 0;
  altparent_timeslot = get_node_timeslot_by_id(child_id);
  //altparent_timeslot = (child_id + CONDUCT_EBSF_OFFSET) % ORCHESTRA_LEAPFROG_ALT_TRAFFIC_PERIOD; //like ORCHESTRA_LINKADDR_HASH(linkaddr)%PERIOD

  struct tsch_link *altparent_l;
  altparent_l = tsch_schedule_get_link_by_timeslot(sf_lfat, altparent_timeslot);
  if(altparent_l != NULL) {
    tsch_schedule_remove_link(sf_lfat, altparent_l);
  }
  tsch_schedule_add_link(
    sf_lfat,
    link_option, //here should be LINK_OPTION_RX or LINK_OPTION_PROMISCUOUS_RX
    LINK_TYPE_NORMAL,
    &tsch_broadcast_address, //welcome everyone
    altparent_timeslot,
    channel_offset); //should be modified to get correct channel_offset of link
}
/*---------------------------------------------------------------------------*/
void
orchestra_leapfrog_set_packetbuf_attr(char child_id)
{
  uint16_t child_timeslot = 0;
  child_timeslot = get_node_timeslot_by_id(linkaddr_node_addr.u8[7]);
  //child_timeslot = (linkaddr_node_addr.u8[7] + CONDUCT_EBSF_OFFSET) % ORCHESTRA_LEAPFROG_ALT_TRAFFIC_PERIOD; //like ORCHESTRA_LINKADDR_HASH(linkaddr)%PERIOD
  
  packetbuf_set_attr(PACKETBUF_ATTR_TSCH_SLOTFRAME, slotframe_handle);
  packetbuf_set_attr(PACKETBUF_ATTR_TSCH_TIMESLOT, child_timeslot);
}
#endif //WITH_LEAPFROG_TSCH
