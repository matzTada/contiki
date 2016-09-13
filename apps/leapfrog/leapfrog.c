/*
 * Copyright (c) 2010, Swedish Institute of Computer Science.
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
 * This file is part of the Contiki operating system.
 *
 */

/**
 * \file
 *         Leapfrog Collaboration
 * \author
 *         TadaMatz <Telecom Bretange, Keio University>
 */

#include "contiki.h"
#include "leapfrog.h"
#include <stdio.h>
#include <string.h>

/* ----------------- leapfrog include and declaration start ----------------- */
//#ifdef WITH_LEAPFROG

char leapfrog_parent_id = 0;
char leapfrog_grand_parent_id = 0;
char leapfrog_alt_parent_id = 0;

char leapfrog_possible_parent_num = 0;
char leapfrog_possible_parent_id_array[LEAPFROG_NUM_NEIGHBOR_NODE] = {0};

char leapfrog_data_counter = 0;
char leapfrog_elimination_id_array[LEAPFROG_NUM_NODE] = {LEAPFROG_DATA_COUNTER_MAX};

extern rpl_instance_t * default_instance;
static struct simple_udp_connection leapfrog_unicast_connection;
PROCESS(leapfrog_beaconing_process, "Leapfrog beaconing process");

// #ifdef WITH_LEAPFROG_TSCH
// // extern struct tsch_slotframe *sf_lfat; //leapfrog alt traffic
// linkaddr_t alt_parent_linkaddr = {{0xc1, 0x0c, 0, 0, 0, 0, 0, 0}};
// #endif /*WITH_LEAPFROG_TSCH*/

char leapfrog_layer = 0; //default for 0. sender should be 1

//#endif //WITH_LEAPFROG
/* ----------------- leapfrog include and declaration end ----------------- */

/*---------------------------------------------------------------------------*/
void
leapfrog_receiver(struct simple_udp_connection *c,
         const uip_ipaddr_t *sender_addr,
         uint16_t sender_port,
         const uip_ipaddr_t *receiver_addr,
         uint16_t receiver_port,
         const uint8_t *data,
         uint16_t datalen)
{
//#ifdef WITH_LEAPFROG //for beaconing
  if(datalen > 0 && data[0] == LEAPFROG_BEACON_HEADER){
    char temp_sid = 0; //sender id of packet
    char temp_pid = 0; //sender's parent id
//    char temp_gid = 0; //sender's grand parent id
    char temp_aid = 0; //sender's alt parent id
    char temp_layer = 0; //sender's layer
    temp_sid = sender_addr->u8[15]; //get most least byte. must be modified to store whole address
    temp_pid = data[2] - LEAPFROG_BEACON_OFFSET;
//    temp_gid = data[4] - LEAPFROG_BEACON_OFFSET;
    temp_aid = data[6] - LEAPFROG_BEACON_OFFSET;
    temp_layer = data[8] - LEAPFROG_BEACON_OFFSET;
    char temp_pps_num;
    char temp_pps_str[LEAPFROG_NUM_NEIGHBOR_NODE];
    int temp_pps_itr;
    temp_pps_num = data[10] - LEAPFROG_BEACON_OFFSET;
    for(temp_pps_itr = 0; temp_pps_itr < (int)temp_pps_num; temp_pps_itr++){ //do nothing if temp_pps_num = 0
      temp_pps_str[temp_pps_itr] = data[10 + 1 + temp_pps_itr];
    }
    // temp_pps_str[temp_pps_itr] = '\0';

    //printf("LEAPFROG: receive beacon S%dP%dGP%dAP%d#%dPPs%s\n", temp_sid, temp_pid, temp_gid, temp_aid, temp_pps_num, temp_pps_str);
    // printf("LEAPFROG: receive beacon '%s'\n", data);
    
    //preparing own informaiton
    char my_id = node_id;
    char my_pid = 0;
    uip_ipaddr_t * addr;
    addr = rpl_get_parent_ipaddr(default_instance->current_dag->preferred_parent);
    if(addr != NULL){
      my_pid = addr->u8[15];
    }

    //judging start
    //got new parent and reset P, GP, AP
    if(leapfrog_parent_id != my_pid){ //new parent and reset P, GP, AP
      leapfrog_parent_id = my_pid;
      leapfrog_grand_parent_id = 0;
      // leapfrog_alt_parent_id = 0;
      // printf("LEAPFROG: reset P GP AP\n");
    }
    //get Grand Parent
    if(leapfrog_parent_id > 0 && leapfrog_parent_id == my_pid){ //judge Grand Parent
      if(temp_sid == my_pid){
        if(temp_pid > 0 && temp_pid != my_pid){
          leapfrog_grand_parent_id = temp_pid; //get grand parent
        }
      }
    }
    //get Alternate Parent
    if(leapfrog_grand_parent_id > 0 && temp_pid > 0 && leapfrog_grand_parent_id == temp_pid && leapfrog_parent_id != temp_sid){ //judge Alt Parent
      if(leapfrog_alt_parent_id != temp_sid){
        leapfrog_alt_parent_id = temp_sid; //get alt parent
// #ifdef WITH_LEAPFROG_TSCH //add unicast tx link to AP based on own(child) ID
//         linkaddr_copy(&alt_parent_linkaddr, packetbuf_addr(PACKETBUF_ADDR_SENDER));
//         printf("LEAPFROG-TSCH: update alt tx normally -> AP %d\n", leapfrog_alt_parent_id);          
//         orchestra_leapfrog_add_uc_tx_link(leapfrog_alt_parent_id);
// #endif /*WITH_LEAPFROG_TSCH*/
      }
    }else{ //get Alternate Parent by Possible Parent
      if(my_pid != temp_sid){
        for(temp_pps_itr = 0; temp_pps_itr < (int)temp_pps_num; temp_pps_itr++){ //do nothing if temp_pps_num = 0
          if(leapfrog_grand_parent_id == temp_pps_str[temp_pps_itr] - LEAPFROG_BEACON_OFFSET){
            leapfrog_alt_parent_id = temp_sid;
// #ifdef WITH_LEAPFROG_TSCH
//             linkaddr_copy(&alt_parent_linkaddr, packetbuf_addr(PACKETBUF_ADDR_SENDER));
//             printf("LEAPFROG-TSCH: update alt tx by PP -> AP %d\n", leapfrog_alt_parent_id);
//             orchestra_leapfrog_add_uc_tx_link(leapfrog_alt_parent_id);
// #endif //WITH_LEAPFROG_TSCH
            break;
          }
        }
      }
    }

    //judge I am sender's Parent and prepare Rx link for child
    if(my_id != 0 && temp_pid != 0 && my_id == temp_pid){ //if I am sender's parent, store Rx slot for child
      if(temp_layer > 0){
        if(leapfrog_layer == 0){ //initialize
          leapfrog_layer = temp_layer + 1;
        }else if(leapfrog_layer > 0 && leapfrog_layer > temp_layer + 1){ //leapfrog_layer is minimum hop from bottom layer
          leapfrog_layer = temp_layer + 1;
        }
      }
// #ifdef WITH_LEAPFROG_TSCH
//       printf("LEAPFROG-TSCH: update rx <- C %d\n", temp_sid);
//       orchestra_unicast_add_uc_rx_link(temp_sid, LINK_OPTION_RX); 
#ifdef WITH_OVERHEARING  //if my child has alternate parent,
      if(temp_aid != 0){ //if sender has the Alt parent, store the promiscuous Rx slot to overhear the alt traffic
        // printf("OVERHEAR: update pro-rx <- (alt)C %d\n", temp_sid);
        thunder_add_link(temp_sid, temp_aid, LINK_OPTION_RX | LINK_OPTION_OVERHEARING);
        // orchestra_leapfrog_add_uc_rx_link(temp_sid, LINK_OPTION_RX | LINK_OPTION_PROMISCUOUS_RX); //to overhear the alt traffic
      }
#endif //WITH_OVERHEARING
// #endif //WITH_LEAPFROG_TSCH
    }   

    //judge I am sender's Alt Parent and prepare Rx link for alt child
    if(my_id !=0 && temp_aid != 0 && my_id == temp_aid){
      if(temp_layer > 0){
        if(leapfrog_layer == 0){ //initialize
          leapfrog_layer = temp_layer + 1;
        }else if(leapfrog_layer > 0 && leapfrog_layer > temp_layer + 1){ //leapfrog_layer is minimum hop from bottom layer
          leapfrog_layer = temp_layer + 1;
        }
      }
// #ifdef WITH_LEAPFROG_TSCH //judge I am sender's Alt Parent
//       printf("LEAPFROG-TSCH: update rx <- (alt)C %d\n", temp_sid);
//       orchestra_leapfrog_add_uc_rx_link(temp_sid, LINK_OPTION_RX);
#ifdef WITH_OVERHEARING //store the promiscuous Rx slot to overhear the preffered traffic
      // printf("OVERHEAR: update pro-rx <- C %d\n", temp_sid);
      thunder_add_link(temp_sid, temp_pid, LINK_OPTION_RX | LINK_OPTION_OVERHEARING);
      // orchestra_unicast_add_uc_rx_link(temp_sid, LINK_OPTION_RX | LINK_OPTION_PROMISCUOUS_RX); //to overhear the normal traffic
#endif //WITH_OVERHEARING
// #endif /*WITH_LEAPFROG_TSCH*/          
    }   

    //judge Siblings
    if(temp_pid > 0 && temp_pid == leapfrog_parent_id){
      //then temp_sid = sibling id
#ifdef WITH_OVERHEARING //if siblings, store timeslot for both preffered and alt traffic
      // printf("OVERHEAR: update pro-rx <- sibling %d\n", temp_sid);
      thunder_add_link(temp_sid, temp_pid, LINK_OPTION_RX | LINK_OPTION_OVERHEARING);
      if(temp_aid > 0){
        thunder_add_link(temp_sid, temp_aid, LINK_OPTION_RX | LINK_OPTION_OVERHEARING);
      }
      // orchestra_unicast_add_uc_rx_link(temp_sid, LINK_OPTION_RX | LINK_OPTION_PROMISCUOUS_RX);
      // orchestra_leapfrog_add_uc_rx_link(temp_sid, LINK_OPTION_RX | LINK_OPTION_PROMISCUOUS_RX);
#endif //WITH_OVERHEARIN
    }else if(temp_pid > 0 && temp_pps_num > 0){ //compare sender's possible parent and own parent
      for(temp_pps_itr = 0; temp_pps_itr < (int)temp_pps_num; temp_pps_itr++){ //do nothing if temp_pps_num = 0
        if(temp_pps_str[temp_pps_itr] - LEAPFROG_BEACON_OFFSET == leapfrog_parent_id){
          //then temp_sid = sibling id
#ifdef WITH_OVERHEARING
          // printf("OVERHEAR: update pro-rx <- sibling %d\n", temp_sid);
          thunder_add_link(temp_sid, temp_pid, LINK_OPTION_RX | LINK_OPTION_OVERHEARING);
          if(temp_aid > 0){
            thunder_add_link(temp_sid, temp_aid, LINK_OPTION_RX | LINK_OPTION_OVERHEARING);
          }
          // orchestra_unicast_add_uc_rx_link(temp_sid, LINK_OPTION_RX | LINK_OPTION_PROMISCUOUS_RX);
          // orchestra_leapfrog_add_uc_rx_link(temp_sid, LINK_OPTION_RX | LINK_OPTION_PROMISCUOUS_RX);
#endif //WITH_OVERHEARIN
// #ifdef WITH_LEAPFROG_TSCH
//             linkaddr_copy(&alt_parent_linkaddr, packetbuf_addr(PACKETBUF_ADDR_SENDER));
//             printf("LEAPFROG-TSCH: update alt tx by PP -> AP %d\n", leapfrog_alt_parent_id);
//             orchestra_leapfrog_add_uc_tx_link(leapfrog_alt_parent_id);
// #endif //WITH_LEAPFROG_TSCH
          break;
        }
      }
    }

    //end of judging process by beacon.
    //print calculated information
    for(temp_pps_itr = 0; temp_pps_itr < leapfrog_possible_parent_num; temp_pps_itr++){
       temp_pps_str[temp_pps_itr] = leapfrog_possible_parent_id_array[temp_pps_itr] + LEAPFROG_BEACON_OFFSET;
    }
    temp_pps_str[temp_pps_itr] = '\0';
    printf("LEAPFROG: own P%d GP%d AP%d PPs%d:%s L%d\n", leapfrog_parent_id, leapfrog_grand_parent_id, leapfrog_alt_parent_id, leapfrog_possible_parent_num, temp_pps_str, leapfrog_layer);

  } //if(data[0] == LEAPFROG_BEACON_HEADER)
//#endif /*WITH_LEAPFROG*/
}
/*---------------------------------------------------------------------------*/
//#ifdef WITH_LEAPFROG
/* ----------------- leapfrog process start----------------- */
PROCESS_THREAD(leapfrog_beaconing_process, ev, data)
{
  static struct etimer lf_beacon_periodic_timer;
  //static struct etimer lf_beacon_send_timer;

  PROCESS_BEGIN();

  simple_udp_register(&leapfrog_unicast_connection, LEAPFROG_UDP_PORT, NULL, LEAPFROG_UDP_PORT, leapfrog_receiver);

  //slide timer added 5/Sep/2016 to avoid collision with network print and application data
  etimer_set(&lf_beacon_periodic_timer, LEAPFROG_SEND_SLIDE_TIME);
  PROCESS_WAIT_EVENT_UNTIL(etimer_expired(&lf_beacon_periodic_timer));

  etimer_set(&lf_beacon_periodic_timer, LEAPFROG_SEND_INTERVAL);
  while(1) {
      PROCESS_WAIT_EVENT_UNTIL(etimer_expired(&lf_beacon_periodic_timer));
      etimer_reset(&lf_beacon_periodic_timer);
      //etimer_set(&lf_beacon_send_timer, LEAPFROG_SEND_TIME);
  
      //PROCESS_WAIT_EVENT_UNTIL(etimer_expired(&lf_beacon_send_timer));
      
    if(tsch_is_associated){
      /*--- target address decision ---*/
      /*-- linklocal rplnodes mcast --*/
      // uip_ipaddr_t *addr;
      uip_ipaddr_t temp_ipaddr;
      uip_create_linklocal_rplnodes_mcast(&temp_ipaddr);  //uip_ip6addr(&temp_ipaddr, 0xff02,0,0,0,0,0,0,0x001a);
      //uip_create_linklocal_allnodes_mcast(&temp_ipaddr);  //refer to contiki/examples/ipv6/simple-udp-rpl/broadcast-example.c
      //uip_create_linklocal_allrouters_mcast(&temp_ipaddr); //refer to core/net/ip/uip.h#L2027. Usually, all nodes are Routers in TSCH network, at least in my understanding
      // addr = &temp_ipaddr;

      /*--- sending ---*/ 
//      if(&temp_ipaddr != NULL) {
        static unsigned int message_number;
        char buf[20];
        char possible_parent_str[1 + LEAPFROG_NUM_NEIGHBOR_NODE];

        possible_parent_str[0] = leapfrog_possible_parent_num + LEAPFROG_BEACON_OFFSET;
        int i;
        for(i = 0; i < leapfrog_possible_parent_num; i++){
          possible_parent_str[1 + i] = leapfrog_possible_parent_id_array[i] + LEAPFROG_BEACON_OFFSET;
        }

        sprintf(buf, "%cP%cG%cA%cL%cC%sN%d",
          LEAPFROG_BEACON_HEADER, 
          leapfrog_parent_id + LEAPFROG_BEACON_OFFSET,
          leapfrog_grand_parent_id + LEAPFROG_BEACON_OFFSET,
          leapfrog_alt_parent_id + LEAPFROG_BEACON_OFFSET,
          leapfrog_layer + LEAPFROG_BEACON_OFFSET, //for layer
          possible_parent_str, //C for candidate
          message_number);
        // printf("LEAPFROG: Sending beacon to ");
        // uip_debug_ipaddr_print(addr);
        uip_debug_ipaddr_print(&temp_ipaddr);
        printf(" '");
        printf(buf);
        printf("'\n");
        message_number++;
        // simple_udp_sendto(&unicast_connection, buf, strlen(buf) + 1, addr);
        simple_udp_sendto(&leapfrog_unicast_connection, buf, strlen(buf) + 1, &temp_ipaddr);
        //simple_udp_sendto(&unicast_connection, buf, cnt, addr);
//      } else {
//        printf("LEAPFROG: addr is null!!");
//      }
    } //if tsch_is_associated
  }

  PROCESS_END();
}
/* ----------------- leapfrog process end ----------------- */
//#endif /*WITH_LEAPFROG*/
/*---------------------------------------------------------------------------*/
void
leapfrog_init()
{
  int initialize_elimination_itr = 0;
  for(initialize_elimination_itr = 0; initialize_elimination_itr < LEAPFROG_NUM_NODE; initialize_elimination_itr++){
    leapfrog_elimination_id_array[initialize_elimination_itr] = LEAPFROG_DATA_COUNTER_MAX; //Do not forget the initialization
  }

  process_start(&leapfrog_beaconing_process, NULL);
}
