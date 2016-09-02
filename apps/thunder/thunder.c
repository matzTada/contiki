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
 *        thunder.c
 *         
 * \author TadaMatz 
 */

#include "contiki.h"
#include "thunder.h"
#include "net/packetbuf.h"
#include "net/ipv6/uip-icmp6.h"
#include "net/rpl/rpl-private.h"

#define DEBUG DEBUG_PRINT
#include "net/ip/uip-debug.h"

static uint16_t slotframe_handle = 0;
static uint16_t channel_offset = 0;
static struct tsch_slotframe *sf_thunder;

/*---------------------------------------------------------------------------*/
static uint16_t
get_node_timeslot(const uint16_t src_id, const uint16_t dst_id)
{
  return (src_id - 1) * THUNDER_NUM_NODE + (dst_id - 1);
}
/*---------------------------------------------------------------------------*/
static uint16_t
get_eb_timeslot(const uint16_t src_id)
{
  return (src_id - 1) + THUNDER_NUM_NODE * THUNDER_NUM_NODE;
}
/*---------------------------------------------------------------------------*/
#ifdef WITH_LEAPFROG_BEACON_SLOT
static uint16_t
get_leapfrog_beacon_timeslot(const uint16_t src_id)
{
  return (src_id - 1) + THUNDER_NUM_NODE * THUNDER_NUM_NODE + THUNDER_NUM_NODE; //just after Enhanced beacon
}
#endif //WITH_LEAPFROG_BEACON_SLOT
/*---------------------------------------------------------------------------*/
void
thunder_callback_packet_ready(void)
{
  uint16_t timeslot = 0xffff;
  const linkaddr_t *dst_addr = packetbuf_addr(PACKETBUF_ADDR_RECEIVER);

/*
  int i = 0;
  printf("IPTCPH");
  for(i = -10; i < 10; i++){
    printf("- i:%d c:%c x:%x -, ", i, uip_buf[UIP_IPTCPH_LEN + i], uip_buf[UIP_IPTCPH_LEN + i]);
  }
  printf("IPUDPH");
  for(i = -10; i < 10; i++){
    printf("-i:%dc:%cx:%x-", i, uip_buf[UIP_IPUDPH_LEN + i], uip_buf[UIP_IPUDPH_LEN + i]);
  }
*/

  PRINTF("THUNDER: p r slot:");
  /* Judge packet and assign specified link */ 
  if(packetbuf_attr(PACKETBUF_ATTR_FRAME_TYPE) == FRAME802154_BEACONFRAME) {   /* EBs should be sent in Broadcast slot. Because virtual neighbor EB addr is {0}*/
    timeslot = get_eb_timeslot(THUNDER_LINKADDR_HASH(&linkaddr_node_addr));
    PRINTF("%d EB", timeslot);
  }
#ifdef WITH_LEAPFROG_BEACON_SLOT
  else if(packetbuf_attr(PACKETBUF_ATTR_FRAME_TYPE) == FRAME802154_DATAFRAME
           && uip_buf[UIP_IPUDPH_LEN] == LEAPFROG_BEACON_HEADER) { //Leapfrog Beacon. Hey!!!!!!!! Magic number
    timeslot = get_leapfrog_beacon_timeslot(THUNDER_LINKADDR_HASH(&linkaddr_node_addr));
    PRINTF("%d LB", timeslot);
  }
#endif //WITH_LEAPFROG_BEACON_SLOT
  else if(packetbuf_attr(PACKETBUF_ATTR_FRAME_TYPE) == FRAME802154_DATAFRAME 
           && !linkaddr_cmp(dst_addr, &linkaddr_null)) { /* Unicast data*/
    timeslot = get_node_timeslot(THUNDER_LINKADDR_HASH(&linkaddr_node_addr), THUNDER_LINKADDR_HASH(dst_addr));
    PRINTF("%d Uni", timeslot);
  }
  else{ /* Any other slots are sent in broadcast slot*/
    timeslot = get_node_timeslot(THUNDER_LINKADDR_HASH(&linkaddr_node_addr), THUNDER_LINKADDR_HASH(&linkaddr_node_addr));
    PRINTF("%d Bro", timeslot);
  }
  PRINTF("\n");

#if TSCH_WITH_LINK_SELECTOR
  packetbuf_set_attr(PACKETBUF_ATTR_TSCH_SLOTFRAME, slotframe_handle); //we have only one slotframe
  packetbuf_set_attr(PACKETBUF_ATTR_TSCH_TIMESLOT, timeslot);
#endif
}
/*---------------------------------------------------------------------------*/
#ifdef WITH_THUNDER_ADAPTIVE_EB_SLOT
void
thunder_callback_new_time_source(const struct tsch_neighbor *old, const struct tsch_neighbor *new)
{
  uint16_t old_ts = old != NULL ? get_eb_timeslot(THUNDER_LINKADDR_HASH(&old->addr)) : 0xffff;
  uint16_t new_ts = new != NULL ? get_eb_timeslot(THUNDER_LINKADDR_HASH(&new->addr)) : 0xffff;

  if(new_ts == old_ts) {
    return;
  }

  if(old_ts != 0xffff) {
    /* Stop listening to the old time source's EBs */
    if(old_ts == get_eb_timeslot(THUNDER_LINKADDR_HASH(&linkaddr_node_addr))) {
      /* This was the same timeslot as slot. Reset original link options */
      tsch_schedule_add_link(sf_thunder, 
        LINK_OPTION_TX, 
        LINK_TYPE_ADVERTISING_ONLY,
        &tsch_broadcast_address, 
        old_ts, 
        channel_offset);
    } else {
      /* Remove slot */
      tsch_schedule_remove_link_by_timeslot(sf_thunder, old_ts);
    }
  }
  if(new_ts != 0xffff) {
    uint8_t link_options = LINK_OPTION_RX;
    if(new_ts == get_eb_timeslot(THUNDER_LINKADDR_HASH(&linkaddr_node_addr))) {
      /* This is also our timeslot, add necessary flags */
      link_options |= LINK_OPTION_TX;
    }
    /* Listen to the time source's EBs */
    tsch_schedule_add_link(sf_thunder, 
      link_options,
      LINK_TYPE_ADVERTISING_ONLY,
      &tsch_broadcast_address, 
      new_ts, 
      channel_offset);
  }
}
#endif //WITH_THUNDER_ADAPTIVE_EB_SLOT
/*---------------------------------------------------------------------------*/
void
thunder_init(void)
{
  int i;
  uint16_t timeslot = 0xffff;

  /* Only one slotframe*/
  sf_thunder = tsch_schedule_add_slotframe(slotframe_handle, THUNDER_SLOTFRAME_LENGTH);

  /* Initialize Thunder  */
  PRINTF("Thunder: initializing\n");

#ifdef WITH_THUNDER_ADAPTIVE_EB_SLOT
  /* EB link: every neighbor uses its own to avoid contention */
  tsch_schedule_add_link(sf_thunder, 
    LINK_OPTION_TX,
    LINK_TYPE_ADVERTISING_ONLY, 
    &tsch_broadcast_address,
    get_eb_timeslot(THUNDER_LINKADDR_HASH(&linkaddr_node_addr)), 
    channel_offset);
#else //WITH_THUNDER_ADAPTIVE_EB_SLOT
  //EB Tx slots
  timeslot = get_eb_timeslot(THUNDER_LINKADDR_HASH(&linkaddr_node_addr)); //after all unicast and broadcast slot
  tsch_schedule_add_link(sf_thunder, 
    LINK_OPTION_TX, 
    LINK_TYPE_ADVERTISING_ONLY, 
    &tsch_broadcast_address,
    timeslot, 
    channel_offset);

  //EB Rx slots
  for(i = 1; i < THUNDER_NUM_NODE + 1; i++){
    if(THUNDER_LINKADDR_HASH(&linkaddr_node_addr) != i){ //when I am a sender, skip
      timeslot = get_eb_timeslot(i); 
      tsch_schedule_add_link(sf_thunder, 
       LINK_OPTION_RX, 
       LINK_TYPE_ADVERTISING_ONLY, 
       &tsch_broadcast_address,
       timeslot, 
       channel_offset);
    }
  }
#endif //WITH_THUNDER_ADAPTIVE_EB_SLOT

  //Unicast Tx slots
  for(i = 1; i < THUNDER_NUM_NODE + 1; i++){
    if(THUNDER_LINKADDR_HASH(&linkaddr_node_addr) != i){ //when I am a sender, skip
      timeslot = get_node_timeslot(THUNDER_LINKADDR_HASH(&linkaddr_node_addr), i); //(src = &linkaddr_node_addr = own linkaddr, dst = neighbor)
      tsch_schedule_add_link(sf_thunder, 
       LINK_OPTION_TX, 
       LINK_TYPE_NORMAL, 
       &tsch_broadcast_address,
       timeslot, 
       channel_offset);
    }
  }

  //Unicast Rx slots
  for(i = 1; i < THUNDER_NUM_NODE + 1; i++){
    if(THUNDER_LINKADDR_HASH(&linkaddr_node_addr) != i){ //when I am a sender, skip
      timeslot = get_node_timeslot(i, THUNDER_LINKADDR_HASH(&linkaddr_node_addr)); //(src = neighbor, dst = &linkaddr_node_addr = own linkaddr)
      tsch_schedule_add_link(sf_thunder, 
       LINK_OPTION_RX, 
       LINK_TYPE_NORMAL, 
       &tsch_broadcast_address,
       timeslot, 
       channel_offset);
    }
  }

  //Broadcast Tx slots
  timeslot = get_node_timeslot(THUNDER_LINKADDR_HASH(&linkaddr_node_addr), THUNDER_LINKADDR_HASH(&linkaddr_node_addr)); //(src = &linkaddr_node_addr = own linkaddr, dst = neighbor)
  tsch_schedule_add_link(sf_thunder, 
   LINK_OPTION_RX | LINK_OPTION_TX | LINK_OPTION_SHARED, 
   LINK_TYPE_NORMAL, 
   &tsch_broadcast_address,
   timeslot, 
   channel_offset);

  //Broadcast Rx slots
  for(i = 1; i < THUNDER_NUM_NODE + 1; i++){
    if(THUNDER_LINKADDR_HASH(&linkaddr_node_addr) != i){ //when I am a sender, skip
      timeslot = get_node_timeslot(i, i); //(src = neighbor, dst = neighbor) i.e. Broadcast (1-1)*8+(1-1) for ID:1, (2-1)*8+(2-1) for ID:2, (3-1)*8+(3-1) for ID:3
      tsch_schedule_add_link(sf_thunder, 
       LINK_OPTION_RX | LINK_OPTION_TX | LINK_OPTION_SHARED, 
       LINK_TYPE_NORMAL, 
       &tsch_broadcast_address,
       timeslot, 
       channel_offset);
    }
  }

#ifdef WITH_LEAPFROG_BEACON_SLOT
  //Leapfrog Beacon Tx slots
  timeslot = get_leapfrog_beacon_timeslot(THUNDER_LINKADDR_HASH(&linkaddr_node_addr)); //after all unicast and broadcast slot
  tsch_schedule_add_link(sf_thunder, 
    LINK_OPTION_RX | LINK_OPTION_TX | LINK_OPTION_SHARED, 
    LINK_TYPE_NORMAL,
    &tsch_broadcast_address,
    timeslot,
    channel_offset);


  //Leapfrog Beacon Rx slots
  for(i = 1; i < THUNDER_NUM_NODE + 1; i++){
    if(THUNDER_LINKADDR_HASH(&linkaddr_node_addr) != i){ //when I am a sender, skip
      timeslot = get_leapfrog_beacon_timeslot(i);
      tsch_schedule_add_link(sf_thunder,
       LINK_OPTION_RX | LINK_OPTION_TX | LINK_OPTION_SHARED,
       LINK_TYPE_NORMAL,
       &tsch_broadcast_address,
       timeslot,
       channel_offset);
    }
  }
#endif //WITH_LEAPFROG_BEACON_SLOT

  PRINTF("Thunder: initialization done\n");
}
