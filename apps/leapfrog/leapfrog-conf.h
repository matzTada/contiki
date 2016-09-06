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
 *         Leapfrog configuration
 *
 * \author Tadanori Matsui
 */

#ifndef __LEAPFROG_CONF_H__
#define __LEAPFROG_CONF_H__

// #ifdef WITH_LEAPFROG
#define LEAPFROG_UDP_PORT 5678
#define LEAPFROG_SEND_SLIDE_TIME (20 * CLOCK_SECOND)
#define LEAPFROG_SEND_INTERVAL   (30 * CLOCK_SECOND)
//#define LEAPFROG_SEND_TIME   (random_rand() % (LEAPFROG_SEND_INTERVAL))
#define LEAPFROG_BEACON_HEADER 0xf1 //for in data packet
#define LEAPFROG_DATA_HEADER 0xf2 //for sending data
#define LEAPFROG_BEACON_OFFSET 48 //for avoiding NULL character in data packet
#define LEAPFROG_NUM_NODE 32 //used for elimination
#define LEAPFROG_NUM_NEIGHBOR_NODE 8 //used for possible parent
#define LEAPFROG_DATA_COUNTER_MAX 50 //since fixed value of header counter has limited value
#define LEAPFROG_DATA_COUNTER_WIDTH 25 //sender node sends data with sequential number, but it happens that the order to arrive dst can be inversed. This number shows how many packet should be discarded compared to current number.
// #endif /*WITH_LEAPFROG*/
//==added


#endif /* __LEAPFROG_CONF_H__ */
