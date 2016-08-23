/*
 * Copyright (c) 2015, SICS Swedish ICT.
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
 * \author Simon Duquennoy <simonduq@sics.se>
 */

#ifndef __PROJECT_CONF_H__
#define __PROJECT_CONF_H__

//modified by TadaMatz 1/July/2016
//#define IGNORE_TSCH_RESEND //ignore TSCH resending in tsch-slot-operation
#define TSCH_CONF_MAC_MAX_FRAME_RETRIES 6//here can controll the number of re-transmission in TSCH. This should be 0 if used with Leapfrog Collaboration
#define CONDUCT_ORCHESTRA
#define WITH_DATA_SLOT
//#define WITH_LEAPFROG
//#define WITH_LEAPFROG_TSCH //if defined, make the new timeslot for alt-parent
//#define WITH_LEAPFROG_BEACON_SLOT
//#define WITH_OVERHEARING
//#define WITH_OVERHEARING_SLEEP
//#define WITH_DETERMINISTIC_SLEEP
#define WITH_POWERTRACE // for power trace
#define WITH_STABLETIMER // for waiting application traffic until network stabilized

//for data
#define DATA_UDP_PORT 1234
#define SERVICE_ID 190
#define DATA_SEND_INTERVAL   (60 * CLOCK_SECOND)
//#define SEND_TIME   (random_rand() % (SEND_INTERVAL))
#define DATA_SEND_TIME   (SEND_INTERVAL) //make it periodical

#define ORCHESTRA_CONF_UNICAST_SENDER_BASED 1
//#define ORCHESTRA_CONF_COLLISION_FREE_HASH 1

#ifdef WITH_DATA_SLOT
#define APPLICATION_DATA_HEADER 0xf3
#endif //WITH_DATA_SLOT

#ifdef WITH_STABLETIMER
#define STABLE_START_TIME (30 * 60 * CLOCK_SECOND)
#endif //WITH_STABLETIMER

#ifdef WITH_LEAPFROG
#define LEAPFROG_UDP_PORT 5678
#define LEAPFROG_SEND_INTERVAL   (15 * CLOCK_SECOND)
#define LEAPFROG_SEND_TIME   (random_rand() % (LEAPFROG_SEND_INTERVAL))
#define LEAPFROG_BEACON_HEADER 0xf1 //for in data packet
#define LEAPFROG_DATA_HEADER 0xf2 //for sending data
#define LEAPFROG_BEACON_OFFSET 48 //for avoiding NULL character in data packet
#define LEAPFROG_NUM_NODE 32 //used for elimination
#define LEAPFROG_NUM_NEIGHBOR_NODE 8 //used for possible parent
#define LEAPFROG_DATA_COUNTER_MAX 20 //since fixed value of header counter has limited value
#define LEAPFROG_DATA_COUNTER_WIDTH 10 //sender node sends data with sequential number, but it happens that the order to arrive dst can be inversed. This number shows how many packet should be discarded compared to current number.
#endif /*WITH_LEAPFROG*/
//==added

#ifdef WITH_OVERHEARING_SLEEP
#define OVERHEARING_SLEEP_TIME (DATA_SEND_INTERVAL / 2) //default. should corresponding to the slotframe length
//#define OVERHEARING_SLEEP_TIME ((LEAPFROG_SEND_INTERVAL) - (8 * 2 * CLOCK_SECOND)) //SEND_INTERVAL - NUM_of_nodes * Slotframe_length * Timeslot_time
#endif //WITH_OVERHEARING_SLEEP

#define WITH_ORCHESTRA 1

/* Set to run orchestra */
#ifndef WITH_ORCHESTRA
#define WITH_ORCHESTRA 0
#endif /* WITH_ORCHESTRA */

/* Set to enable TSCH security */
#ifndef WITH_SECURITY
#define WITH_SECURITY 0
#endif /* WITH_SECURITY */

/*******************************************************/
/********************* Enable TSCH *********************/
/*******************************************************/

/* Netstack layers */
#undef NETSTACK_CONF_MAC
#define NETSTACK_CONF_MAC     tschmac_driver
#undef NETSTACK_CONF_RDC
#define NETSTACK_CONF_RDC     nordc_driver
#undef NETSTACK_CONF_FRAMER
#define NETSTACK_CONF_FRAMER  framer_802154

/* IEEE802.15.4 frame version */
#undef FRAME802154_CONF_VERSION
#define FRAME802154_CONF_VERSION FRAME802154_IEEE802154E_2012

/* TSCH and RPL callbacks */
#define RPL_CALLBACK_PARENT_SWITCH tsch_rpl_callback_parent_switch
#define RPL_CALLBACK_NEW_DIO_INTERVAL tsch_rpl_callback_new_dio_interval
#define TSCH_CALLBACK_JOINING_NETWORK tsch_rpl_callback_joining_network
#define TSCH_CALLBACK_LEAVING_NETWORK tsch_rpl_callback_leaving_network

/* Needed for cc2420 platforms only */
/* Disable DCO calibration (uses timerB) */
#undef DCOSYNCH_CONF_ENABLED
#define DCOSYNCH_CONF_ENABLED            0
/* Enable SFD timestamps (uses timerB) */
#undef CC2420_CONF_SFD_TIMESTAMPS
#define CC2420_CONF_SFD_TIMESTAMPS       1

/*******************************************************/
/******************* Configure TSCH ********************/
/*******************************************************/

/* TSCH logging. 0: disabled. 1: basic log. 2: with delayed
 * log messages from interrupt */
#undef TSCH_LOG_CONF_LEVEL
#define TSCH_LOG_CONF_LEVEL 2

/* IEEE802.15.4 PANID */
#undef IEEE802154_CONF_PANID
#define IEEE802154_CONF_PANID 0xabcd

/* Do not start TSCH at init, wait for NETSTACK_MAC.on() */
#undef TSCH_CONF_AUTOSTART
#define TSCH_CONF_AUTOSTART 0

/* 6TiSCH minimal schedule length.
 * Larger values result in less frequent active slots: reduces capacity and saves energy. */
#undef TSCH_SCHEDULE_CONF_DEFAULT_LENGTH
#define TSCH_SCHEDULE_CONF_DEFAULT_LENGTH 3

#if WITH_SECURITY

/* Enable security */
#undef LLSEC802154_CONF_ENABLED
#define LLSEC802154_CONF_ENABLED 1
/* TSCH uses explicit keys to identify k1 and k2 */
#undef LLSEC802154_CONF_USES_EXPLICIT_KEYS
#define LLSEC802154_CONF_USES_EXPLICIT_KEYS 1
/* TSCH uses the ASN rather than frame counter to construct the Nonce */
#undef LLSEC802154_CONF_USES_FRAME_COUNTER
#define LLSEC802154_CONF_USES_FRAME_COUNTER 0

#endif /* WITH_SECURITY */

#if WITH_ORCHESTRA

/* See apps/orchestra/README.md for more Orchestra configuration options */
#define TSCH_SCHEDULE_CONF_WITH_6TISCH_MINIMAL 0 /* No 6TiSCH minimal schedule */
#define TSCH_CONF_WITH_LINK_SELECTOR 1 /* Orchestra requires per-packet link selection */
/* Orchestra callbacks */
#define TSCH_CALLBACK_NEW_TIME_SOURCE orchestra_callback_new_time_source
#define TSCH_CALLBACK_PACKET_READY orchestra_callback_packet_ready
#define NETSTACK_CONF_ROUTING_NEIGHBOR_ADDED_CALLBACK orchestra_callback_child_added
#define NETSTACK_CONF_ROUTING_NEIGHBOR_REMOVED_CALLBACK orchestra_callback_child_removed

#endif /* WITH_ORCHESTRA */

/*******************************************************/
/************* Other system configuration **************/
/*******************************************************/

#if CONTIKI_TARGET_Z1
/* Save some space to fit the limited RAM of the z1 */
#undef UIP_CONF_TCP
#define UIP_CONF_TCP 0
#undef QUEUEBUF_CONF_NUM
#define QUEUEBUF_CONF_NUM 4
#undef UIP_CONF_MAX_ROUTES
#define UIP_CONF_MAX_ROUTES  8
#undef NBR_TABLE_CONF_MAX_NEIGHBORS
#define NBR_TABLE_CONF_MAX_NEIGHBORS 8
#undef UIP_CONF_ND6_SEND_NA
#define UIP_CONF_ND6_SEND_NA 0
#undef SICSLOWPAN_CONF_FRAG
#define SICSLOWPAN_CONF_FRAG 0

#if WITH_SECURITY
/* Note: on sky or z1 in cooja, crypto operations are done in S/W and
 * cannot be accommodated in normal slots. Use 65ms slots instead, and
 * a very short 6TiSCH minimal schedule length */
#undef TSCH_CONF_DEFAULT_TIMESLOT_LENGTH
#define TSCH_CONF_DEFAULT_TIMESLOT_LENGTH 65000
#undef TSCH_SCHEDULE_CONF_DEFAULT_LENGTH
#define TSCH_SCHEDULE_CONF_DEFAULT_LENGTH 2
/* Reduce log level to make space for security on z1 */
#undef TSCH_LOG_CONF_LEVEL
#define TSCH_LOG_CONF_LEVEL 0
#endif /* WITH_SECURITY */

#endif /* CONTIKI_TARGET_Z1 */

#endif /* __PROJECT_CONF_H__ */
