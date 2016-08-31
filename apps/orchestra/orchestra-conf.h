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
 *         Orchestra configuration
 *
 * \author Simon Duquennoy <simonduq@sics.se>
 */

#ifndef __ORCHESTRA_CONF_H__
#define __ORCHESTRA_CONF_H__

#ifdef ORCHESTRA_CONF_RULES
#define ORCHESTRA_RULES ORCHESTRA_CONF_RULES
#else /* ORCHESTRA_CONF_RULES */
/* A default configuration with:
 * - a sender-based slotframe for EB transmission
 * - a sender-based or receiver-based slotframe for unicast to RPL parents and children
 * - a common shared slotframe for any other traffic (mostly broadcast)
 *  */

//modifieds by TadaMatz 31/Aug/2016. Sequence of rules is related to priority of rule.
#ifdef WITH_LEAPFROG_TSCH
 #ifdef WITH_DATA_SLOT
#define ORCHESTRA_RULES { &eb_per_time_source, &unicast_appdata_traffic, &leapfrog_alt_traffic, &unicast_per_neighbor_rpl_storing, &default_common}
 #endif //WITH_DATASLOT
#define ORCHESTRA_RULES { &eb_per_time_source, &leapfrog_alt_traffic, &unicast_per_neighbor_rpl_storing, &default_common}
#else //WITH_LEAPFROG_TSCH
 #ifdef WITH_DATA_SLOT
#define ORCHESTRA_RULES { &eb_per_time_source, &unicast_appdata_traffic, &unicast_per_neighbor_rpl_storing, &default_common} 
 #endif //WITH_DATASLOT
#define ORCHESTRA_RULES { &eb_per_time_source, &unicast_per_neighbor_rpl_storing, &default_common }
#endif //WITH_LEAPFROG_TSCH

/* Example configuration for RPL non-storing mode: */
/* #define ORCHESTRA_RULES { &eb_per_time_source, &unicast_per_neighbor_rpl_ns, &default_common } */

#endif /* ORCHESTRA_CONF_RULES */

#ifdef CONDUCT_ORCHESTRA //change unicast slot feature for Leapfrog
#define CONDUCT_EBSF_OFFSET 5 //recommended 8
#define CONDUCT_ALT_TRAFFIC_DRIFT_OFFSET 3 //recommended 3
#endif //CONDUCT_ORCHESTRA

#ifdef SEPARATE_ORCHESTRA //Every slotframe has the same slot frame lengths. added by TadaMatz 26/Aug/2016

#define SEPARATE_PERIOD 101
#define SEPARATE_EBSF_OFFSET 10
#define SEPARATE_UNICAST_OFFSET 10
//set all slotframe has same length
#define ORCHESTRA_CONF_EBSF_PERIOD SEPARATE_PERIOD
#define ORCHESTRA_CONF_COMMON_SHARED_PERIOD SEPARATE_PERIOD
#define ORCHESTRA_CONF_UNICAST_PERIOD SEPARATE_PERIOD

#ifdef WITH_DATA_SLOT
#define SEPARATE_UNICAST_DATA_OFFSET 20
#endif //WITH_DATA_SLOT

#ifdef WITH_LEAPFROG_TSCH
#define SEPARATE_ALT_TRAFFIC_OFFSET 20 //for alternate path
#define ORCHESTRA_CONF_LEAPFROG_ALT_TRAFFIC_PERIOD SEPARATE_PERIOD
#endif //WITH_LEAPFROG_TSCH

#endif //SEPARATE_ORCHESTRA

/* Length of the various slotframes. Tune to balance network capacity,
 * contention, energy, latency. */
#ifdef ORCHESTRA_CONF_EBSF_PERIOD
#define ORCHESTRA_EBSF_PERIOD                     ORCHESTRA_CONF_EBSF_PERIOD
#else /* ORCHESTRA_CONF_EBSF_PERIOD */
#ifdef CONDUCT_ORCHESTRA //by TadaMatz 2/July/2016
#define ORCHESTRA_EBSF_PERIOD                     300 //recommended 360. must be multiple of unicast period
#else //CONDUCT_ORCHESTRA
#define ORCHESTRA_EBSF_PERIOD                     397
#endif //CONDUCT_ORCHESTRA
#endif /* ORCHESTRA_CONF_EBSF_PERIOD */

#ifdef ORCHESTRA_CONF_COMMON_SHARED_PERIOD
#define ORCHESTRA_COMMON_SHARED_PERIOD            ORCHESTRA_CONF_COMMON_SHARED_PERIOD
#else /* ORCHESTRA_CONF_COMMON_SHARED_PERIOD */
#ifdef CONDUCT_ORCHESTRA //by TadaMatz 2/July/2016
#define ORCHESTRA_COMMON_SHARED_PERIOD            30 //recommended 36. must be multiple of unicast period
#else //CONDUCT_ORCHESTRA
#define ORCHESTRA_COMMON_SHARED_PERIOD            31
#endif //CONDUCT_ORCHESTRA
#endif /* ORCHESTRA_CONF_COMMON_SHARED_PERIOD */

#ifdef ORCHESTRA_CONF_UNICAST_PERIOD
#define ORCHESTRA_UNICAST_PERIOD                  ORCHESTRA_CONF_UNICAST_PERIOD
#else /* ORCHESTRA_CONF_UNICAST_PERIOD */
#ifdef CONDUCT_ORCHESTRA //by TadaMatz 2/July/2016
#define ORCHESTRA_UNICAST_PERIOD                  15 //recommended 18. basis of conduct orchestra
#else //CONDUCT_ORCHESTRA
#define ORCHESTRA_UNICAST_PERIOD                  17
#endif //CONDUCT_ORCHESTRA
#endif /* ORCHESTRA_CONF_UNICAST_PERIOD */

/* Is the per-neighbor unicast slotframe sender-based (if not, it is receiver-based).
 * Note: sender-based works only with RPL storing mode as it relies on DAO and
 * routing entries to keep track of children and parents. */
#ifdef ORCHESTRA_CONF_UNICAST_SENDER_BASED
#define ORCHESTRA_UNICAST_SENDER_BASED            ORCHESTRA_CONF_UNICAST_SENDER_BASED
#else /* ORCHESTRA_CONF_UNICAST_SENDER_BASED */
#define ORCHESTRA_UNICAST_SENDER_BASED            0
#endif /* ORCHESTRA_CONF_UNICAST_SENDER_BASED */

//added by TadaMatz 15/June/2016
#ifdef WITH_LEAPFROG_TSCH
#ifdef ORCHESTRA_CONF_LEAPFROG_ALT_TRAFFIC_PERIOD
#define ORCHESTRA_LEAPFROG_ALT_TRAFFIC_PERIOD                  ORCHESTRA_CONF_LEAPFROG_ALT_TRAFFIC_PERIOD
#else /* ORCHESTRA_CONF_LEAPFROG_ALT_TRAFFIC_PERIOD */
#ifdef CONDUCT_ORCHESTRA //by TadaMatz 2/July/2016
#define ORCHESTRA_LEAPFROG_ALT_TRAFFIC_PERIOD                  ORCHESTRA_UNICAST_PERIOD //can be same because both calculate timeslot based on sender
#else //CONDUCT_ORCHESTRA
#define ORCHESTRA_LEAPFROG_ALT_TRAFFIC_PERIOD                  19
#endif //CONDUCT_ORCHESTRA
#endif /* ORCHESTRA_CONF_LEAPFROG_ALT_TRAFFIC_PERIOD */
#endif /*WITH_LEAPFROG_TSCH*/

/* The hash function used to assign timeslot to a given node (based on its link-layer address) */
#ifdef ORCHESTRA_CONF_LINKADDR_HASH
#define ORCHESTRA_LINKADDR_HASH                   ORCHESTRA_CONF_LINKADDR_HASH
#else /* ORCHESTRA_CONF_LINKADDR_HASH */
#define ORCHESTRA_LINKADDR_HASH(addr)             ((addr != NULL) ? (addr)->u8[LINKADDR_SIZE - 1] : -1)
#endif /* ORCHESTRA_CONF_LINKADDR_HASH */

/* The maximum hash */
#ifdef ORCHESTRA_CONF_MAX_HASH
#define ORCHESTRA_MAX_HASH                        ORCHESTRA_CONF_MAX_HASH
#else /* ORCHESTRA_CONF_MAX_HASH */
#define ORCHESTRA_MAX_HASH                        0x7fff
#endif /* ORCHESTRA_CONF_MAX_HASH */

/* Is the "hash" function collision-free? (e.g. it maps to unique node-ids) */
#ifdef ORCHESTRA_CONF_COLLISION_FREE_HASH
#define ORCHESTRA_COLLISION_FREE_HASH             ORCHESTRA_CONF_COLLISION_FREE_HASH
#else /* ORCHESTRA_CONF_COLLISION_FREE_HASH */
#define ORCHESTRA_COLLISION_FREE_HASH             0 /* Set to 1 if ORCHESTRA_LINKADDR_HASH returns unique hashes */
#endif /* ORCHESTRA_CONF_COLLISION_FREE_HASH */

#endif /* __ORCHESTRA_CONF_H__ */
