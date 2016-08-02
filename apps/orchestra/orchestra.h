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
 *         Orchestra header file
 *
 * \author Simon Duquennoy <simonduq@sics.se>
 */

#ifndef __ORCHESTRA_H__
#define __ORCHESTRA_H__

#include "net/mac/tsch/tsch.h"
#include "net/mac/tsch/tsch-conf.h"
#include "net/mac/tsch/tsch-schedule.h"
#include "orchestra-conf.h"

/* The structure of an Orchestra rule */
struct orchestra_rule {
  void (* init)(uint16_t slotframe_handle);
  void (* new_time_source)(const struct tsch_neighbor *old, const struct tsch_neighbor *new);
  int  (* select_packet)(uint16_t *slotframe, uint16_t *timeslot);
  void (* child_added)(const linkaddr_t *addr);
  void (* child_removed)(const linkaddr_t *addr);
};

struct orchestra_rule eb_per_time_source;
struct orchestra_rule unicast_per_neighbor;
struct orchestra_rule default_common;
//added by TadaMatz 15/June/2016
#ifdef WITH_LEAPFROG_TSCH
struct orchestra_rule leapfrog_alt_traffic;
#endif /*WITH_LEAPFROG_TSCH*/

extern linkaddr_t orchestra_parent_linkaddr;
extern int orchestra_parent_knows_us;

/* Call from application to start Orchestra */
void orchestra_init(void);
/* Callbacks requied for Orchestra to operate */
/* Set with #define TSCH_CALLBACK_PACKET_READY orchestra_callback_packet_ready */
void orchestra_callback_packet_ready(void);
/* Set with #define TSCH_CALLBACK_NEW_TIME_SOURCE orchestra_callback_new_time_source */
void orchestra_callback_new_time_source(const struct tsch_neighbor *old, const struct tsch_neighbor *new);
/* Set with #define NETSTACK_CONF_ROUTING_NEIGHBOR_ADDED_CALLBACK orchestra_callback_child_added */
void orchestra_callback_child_added(const linkaddr_t *addr);
/* Set with #define NETSTACK_CONF_ROUTING_NEIGHBOR_REMOVED_CALLBACK orchestra_callback_child_removed */
void orchestra_callback_child_removed(const linkaddr_t *addr);

#ifdef WITH_LEAPFROG_TSCH
/*call from Leapfrog TSCH to handle slotframe*/
void orchestra_leapfrog_add_uc_tx_link(char alt_parent_id);
void orchestra_leapfrog_add_uc_rx_link(char child_id, uint8_t link_option);
void orchestra_leapfrog_set_packetbuf_attr(char child_id);
#endif /*WITH_LEAPFROG_TSCH*/

#ifdef CONDUCT_ORCHESTRA
void orchestra_conduct_add_uc_link(const linkaddr_t *linkaddr, uint8_t link_option);
#endif //CONDUCT_ORCHESTRA

#ifdef WITH_DATA_SLOT
void orchestra_unicast_data_set_packetbuf_attr();
#endif //WITH_DATA_SLOT

#ifdef WITH_OVERHEARING
void orchestra_unicast_add_uc_rx_link(char child_id, uint8_t link_option);
#endif //WITH_OVERHEARING

#ifdef WITH_LEAPFROG_BEACON_SLOT
void orchestra_leapfrog_beacon_set_packetbuf_attr(void);
#endif //WITH_LEAPFROG_BEACON_SLOT

#endif /* __ORCHESTRA_H__ */
