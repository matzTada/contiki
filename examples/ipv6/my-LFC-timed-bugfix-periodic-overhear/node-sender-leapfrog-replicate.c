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
 * \file
 *         A RPL+TSCH node able to act as either a simple node (6ln),
 *         DAG Root (6dr) or DAG Root with security (6dr-sec)
 *         Press use button at startup to configure.
 *
 * \author Simon Duquennoy <simonduq@sics.se>
 *
 * \file sender 
 * \modify enable application packet on RPL-TSCH by combining
 *  the rpl-tsch example and the simple-udp-rpl example
 * \author Tada Matz
 */

#include "contiki.h"
#include "node-id.h"
#include "net/rpl/rpl.h"
#include "net/ipv6/uip-ds6-route.h"
#include "net/mac/tsch/tsch.h"
#if WITH_ORCHESTRA
#include "orchestra.h"
#endif /* WITH_ORCHESTRA */
#ifdef WITH_POWERTRACE
#include "powertrace.h"
#endif //WITH_POWERTRACE

#define DEBUG DEBUG_PRINT
#include "net/ip/uip-debug.h"

#define CONFIG_VIA_BUTTON PLATFORM_HAS_BUTTON
#if CONFIG_VIA_BUTTON
#include "button-sensor.h"
#endif /* CONFIG_VIA_BUTTON */

/* ----------------- simple-udp-rpl include and declaration start----------------- */
#include "lib/random.h"
#include "sys/ctimer.h"
#include "sys/etimer.h"
#include "net/ip/uip.h"
#include "net/ipv6/uip-ds6.h"
// #include "net/ip/uip-debug.h"

#include "simple-udp.h"
//#include "servreg-hack.h"

// #include "net/rpl/rpl.h"

#include <stdio.h>
#include <string.h>

#define UDP_PORT 1234
#define SERVICE_ID 190

#define SEND_INTERVAL   (60 * CLOCK_SECOND)
//#define SEND_TIME   (random_rand() % (SEND_INTERVAL))
#define SEND_TIME   (SEND_INTERVAL) //make it periodical

static struct simple_udp_connection unicast_connection;

PROCESS(unicast_sender_process, "Unicast sender example process");
// AUTOSTART_PROCESSES(&unicast_sender_process);
/* ----------------- simple-udp-rpl include and declaration end ----------------- */

/* ----------------- leapfrog include and declaration start ----------------- */
#ifdef WITH_LEAPFROG
#define LEAPFROG_UDP_PORT 5678
#define LEAPFROG_SEND_INTERVAL   (15 * CLOCK_SECOND)
#define LEAPFROG_SEND_TIME   (random_rand() % (SEND_INTERVAL))
//#define LEAPFROG_BEACON_HEADER 0xf1 //for in data packet
//#define LEAPFROG_BEACON_OFFSET 48 //for avoid NULL character in data packet
//#define LEAPFROG_DATA_HEADER 0xf2 //for sending data

char leapfrog_parent_id = 0;
char leapfrog_grand_parent_id = 0;
char leapfrog_alt_parent_id = 0;

char leapfrog_possible_parent_num = 0;
char leapfrog_possible_parent_id_array[LEAPFROG_NUM_NEIGHBOR_NODE] = {0};

char leapfrog_data_counter = 0;
char leapfrog_elimination_id_array[LEAPFROG_NUM_NODE] = {255};

extern rpl_instance_t * default_instance;
static struct simple_udp_connection leapfrog_unicast_connection;
PROCESS(leapfrog_beaconing_process, "Leapfrog beaconing process");

#ifdef WITH_LEAPFROG_TSCH
// extern struct tsch_slotframe *sf_lfat; //leapfrog alt traffic
linkaddr_t alt_parent_linkaddr = {{0xc1, 0x0c, 0, 0, 0, 0, 0, 0}};
#endif /*WITH_LEAPFROG_TSCH*/

#endif //WITH_LEAPFROG
/* ----------------- leapfrog include and declaration end ----------------- */

/* ----------------- stable timer start ----------------- */
#ifdef WITH_STABLETIMER
int stable_flag = 0;
PROCESS(stable_timer_process, "Stable timer process");
#endif //WITH_STABLETIMER
/* ----------------- stable timer end ----------------- */

/*---------------------------------------------------------------------------*/
#ifdef WITH_STABLETIMER
#ifdef WITH_LEAPFROG
PROCESS(node_process, "RPL Node sender leapfrog");
AUTOSTART_PROCESSES(&node_process, &sensors_process, &unicast_sender_process, &leapfrog_beaconing_process, &stable_timer_process);
#else //WITH_LEAPFROG
PROCESS(node_process, "RPL Node sender leapfrog");
AUTOSTART_PROCESSES(&node_process, &sensors_process, &unicast_sender_process, &stable_timer_process);
#endif //WITH_LEAPFROG
#else //WITH_STABLETIMER
#ifdef WITH_LEAPFROG
PROCESS(node_process, "RPL Node sender leapfrog");
#if CONFIG_VIA_BUTTON
AUTOSTART_PROCESSES(&node_process, &sensors_process, &unicast_sender_process, &leapfrog_beaconing_process);
#else /* CONFIG_VIA_BUTTON */
AUTOSTART_PROCESSES(&node_process, &unicast_sender_process, &leapfrog_beaconing_process);
#endif /* CONFIG_VIA_BUTTON */
#else /*WITH_LEAPFROG*/
PROCESS(node_process, "RPL Node sender leapfrog");
#if CONFIG_VIA_BUTTON
AUTOSTART_PROCESSES(&node_process, &sensors_process, &unicast_sender_process);
#else /* CONFIG_VIA_BUTTON */
AUTOSTART_PROCESSES(&node_process, &unicast_sender_process);
#endif /* CONFIG_VIA_BUTTON */
#endif /*WITH_LEAPFROG*/
#endif // WITH_STABLETIMER
/*---------------------------------------------------------------------------*/
static void
print_network_status(void)
{
  int i;
  uint8_t state;
  uip_ds6_defrt_t *default_route;
  uip_ds6_route_t *route;

  PRINTA("--- Network status ---\n");
  
  /* Our IPv6 addresses */
  PRINTA("- Server IPv6 addresses:\n");
  for(i = 0; i < UIP_DS6_ADDR_NB; i++) {
    state = uip_ds6_if.addr_list[i].state;
    if(uip_ds6_if.addr_list[i].isused &&
       (state == ADDR_TENTATIVE || state == ADDR_PREFERRED)) {
      PRINTA("-%d- ",i);
      uip_debug_ipaddr_print(&uip_ds6_if.addr_list[i].ipaddr);
      PRINTA("\n");
    }
  }
  
  /* Our default route */
  PRINTA("- Default route:\n");
  default_route = uip_ds6_defrt_lookup(uip_ds6_defrt_choose());
  if(default_route != NULL) {
    PRINTA("-- ");
    uip_debug_ipaddr_print(&default_route->ipaddr);;
    PRINTA(" (lifetime: %lu seconds)\n", (unsigned long)default_route->lifetime.interval);
  } else {
    PRINTA("-- None\n");
  }

  /* Our routing entries */
  PRINTA("- Routing entries (%u in total):\n", uip_ds6_route_num_routes());
  route = uip_ds6_route_head();
  while(route != NULL) {
    PRINTA("-- ");
    uip_debug_ipaddr_print(&route->ipaddr);
    PRINTA(" via ");
    uip_debug_ipaddr_print(uip_ds6_route_nexthop(route));
    PRINTA(" (lifetime: %lu seconds)\n", (unsigned long)route->state.lifetime);
    route = uip_ds6_route_next(route); 
  }
  
  PRINTA("----------------------\n");
}
/*---------------------------------------------------------------------------*/
static void
net_init(uip_ipaddr_t *br_prefix)
{
  uip_ipaddr_t global_ipaddr;

  if(br_prefix) { /* We are RPL root. Will be set automatically
                     as TSCH pan coordinator via the tsch-rpl module */
    memcpy(&global_ipaddr, br_prefix, 16);
    uip_ds6_set_addr_iid(&global_ipaddr, &uip_lladdr);
    uip_ds6_addr_add(&global_ipaddr, 0, ADDR_AUTOCONF);
    rpl_set_root(RPL_DEFAULT_INSTANCE, &global_ipaddr);
    rpl_set_prefix(rpl_get_any_dag(), br_prefix, 64);
    rpl_repair_root(RPL_DEFAULT_INSTANCE);
  }

  NETSTACK_MAC.on();
}
/*---------------------------------------------------------------------------*/
/* ----------------- simple-udp-rpl functions start----------------- */
/*simple-udp-rpl---------------------------------------------------------------------------*/
static void
receiver(struct simple_udp_connection *c,
         const uip_ipaddr_t *sender_addr,
         uint16_t sender_port,
         const uip_ipaddr_t *receiver_addr,
         uint16_t receiver_port,
         const uint8_t *data,
         uint16_t datalen)
{
  printf("DATA: received from ");
  //uip_debug_ipaddr_print(sender_addr);
//  printf(" on port %d from port %d with length %d: '%s'\n", receiver_port, sender_port, datalen, data);
  printf("ID:%d l:%d '%s'\n", sender_addr->u8[15], datalen, data); //make it shorter

#ifdef WITH_LEAPFROG //for beaconing
  if(data[0] == LEAPFROG_BEACON_HEADER){
    char temp_sid = 0; //sender id of packet
    char temp_pid = 0; //sender's parent id
//    char temp_gid = 0; //sender's grand parent id
    char temp_aid = 0; //sender's alt parent id
    temp_sid = sender_addr->u8[15]; //get most least byte. must be modified to store whole address
    temp_pid = data[2] - LEAPFROG_BEACON_OFFSET;
//    temp_gid = data[4] - LEAPFROG_BEACON_OFFSET;
    temp_aid = data[6] - LEAPFROG_BEACON_OFFSET;
    char temp_pps_num;
    char temp_pps_str[LEAPFROG_NUM_NEIGHBOR_NODE];
    int temp_pps_itr;
    temp_pps_num = data[8] - LEAPFROG_BEACON_OFFSET;
    for(temp_pps_itr = 0; temp_pps_itr < (int)temp_pps_num; temp_pps_itr++){ //do nothing if temp_pps_num = 0
      temp_pps_str[temp_pps_itr] = data[8 + 1 + temp_pps_itr];
    }
    temp_pps_str[temp_pps_itr] = '\0';

    //printf("LEAPFROG: receive beacon S%dP%dGP%dAP%d#%dPPs%s\n", temp_sid, temp_pid, temp_gid, temp_aid, temp_pps_num, temp_pps_str);
    printf("LEAPFROG: receive beacon '%s'\n", data);
    
    //preparing own informaiton
    #ifdef WITH_LEAPFROG_TSCH
    char my_id = node_id;
    #endif //WITH_LEAPFROG_TSCH
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
      leapfrog_alt_parent_id = 0;
      printf("LEAPFROG: reset P GP AP\n");
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
#ifdef WITH_LEAPFROG_TSCH //add unicast tx link to AP based on own(child) ID
        linkaddr_copy(&alt_parent_linkaddr, packetbuf_addr(PACKETBUF_ADDR_SENDER));
        printf("LEAPFROG-TSCH: update alt tx normally -> AP %d\n", leapfrog_alt_parent_id);          
        orchestra_leapfrog_add_uc_tx_link(leapfrog_alt_parent_id);
#endif /*WITH_LEAPFROG_TSCH*/
      }
    }else{ //get Alternate Parent by Possible Parent
      if(my_pid != temp_sid){
        for(temp_pps_itr = 0; temp_pps_itr < (int)temp_pps_num; temp_pps_itr++){ //do nothing if temp_pps_num = 0
          if(leapfrog_grand_parent_id == data[8 + 1 + temp_pps_itr] - LEAPFROG_BEACON_OFFSET){
            leapfrog_alt_parent_id = temp_sid;
#ifdef WITH_LEAPFROG_TSCH
            linkaddr_copy(&alt_parent_linkaddr, packetbuf_addr(PACKETBUF_ADDR_SENDER));
            printf("LEAPFROG-TSCH: update alt tx by PP -> AP %d\n", leapfrog_alt_parent_id);
            orchestra_leapfrog_add_uc_tx_link(leapfrog_alt_parent_id);
#endif //WITH_LEAPFROG_TSCH
            break;
          }
        }
      }
    }

    //print calculated information
    for(temp_pps_itr = 0; temp_pps_itr < leapfrog_possible_parent_num; temp_pps_itr++){
      temp_pps_str[temp_pps_itr] = leapfrog_possible_parent_id_array[temp_pps_itr] + LEAPFROG_BEACON_OFFSET;
    }
    temp_pps_str[temp_pps_itr] = '\0';
    printf("LEAPFROG: own P %d GP %d AP %d PPs #%d %s\n", leapfrog_parent_id, leapfrog_grand_parent_id, leapfrog_alt_parent_id, leapfrog_possible_parent_num, temp_pps_str);

    //judge I am sender's Parent and prepare Rx link for child
#ifdef WITH_LEAPFROG_TSCH
    if(my_id != 0 && temp_pid != 0 && my_id == temp_pid){ //if I am sender's parent, store Rx slot for child
      printf("LEAPFROG-TSCH: update rx <- C %d\n", temp_sid);
      orchestra_unicast_add_uc_rx_link(temp_sid, LINK_OPTION_RX); 
#ifdef WITH_OVERHEARING  //if my child has alternate parent,
      if(temp_aid != 0){ //if sender has the Alt parent, store the promiscuous Rx slot to overhear the alt traffic
        printf("OVERHEAR: update pro-rx <- (alt)C %d\n", temp_sid);
        orchestra_leapfrog_add_uc_rx_link(temp_sid, LINK_OPTION_RX | LINK_OPTION_PROMISCUOUS_RX); //to overhear the alt traffic
      }
#endif //WITH_OVERHEARING
    }   
#endif //WITH_LEAPFROG_TSCH

    //judge I am sender's Alt Parent and prepare Rx link for alt child
#ifdef WITH_LEAPFROG_TSCH //judge I am sender's Alt Parent
    if(my_id !=0 && temp_aid != 0 && my_id == temp_aid){
      printf("LEAPFROG-TSCH: update rx <- (alt)C %d\n", temp_sid);
      orchestra_leapfrog_add_uc_rx_link(temp_sid, LINK_OPTION_RX);
#ifdef WITH_OVERHEARING
      printf("OVERHEAR: update pro-rx <- C %d\n", temp_sid);
      orchestra_unicast_add_uc_rx_link(temp_sid, LINK_OPTION_RX | LINK_OPTION_PROMISCUOUS_RX); //to overhear the normal traffic
#endif //WITH_OVERHEARING
    }   
#endif /*WITH_LEAPFROG_TSCH*/          

#ifdef WITH_OVERHEARING
    //judge Siblings
    if(temp_pid > 0 && leapfrog_parent_id > 0 && temp_pid == leapfrog_parent_id){
      //then temp_sid = sibling id
      printf("OVERHEAR: update pro-rx <- sibling %d\n", temp_sid);
      orchestra_unicast_add_uc_rx_link(temp_sid, LINK_OPTION_RX | LINK_OPTION_PROMISCUOUS_RX);
      orchestra_leapfrog_add_uc_rx_link(temp_sid, LINK_OPTION_RX | LINK_OPTION_PROMISCUOUS_RX);
    }else if(temp_pid > 0 && leapfrog_possible_parent_num > 0){ //compare sender's parent and own possible parents
      for(temp_pps_itr = 0; temp_pps_itr < (int)leapfrog_possible_parent_num; temp_pps_itr++){
        if(temp_pid == leapfrog_possible_parent_id_array[temp_pps_itr]){
          //then temp_sid = sibling id
          printf("OVERHEAR: update pro-rx <- sibling %d\n", temp_sid);
          orchestra_unicast_add_uc_rx_link(temp_sid, LINK_OPTION_RX | LINK_OPTION_PROMISCUOUS_RX);
          orchestra_leapfrog_add_uc_rx_link(temp_sid, LINK_OPTION_RX | LINK_OPTION_PROMISCUOUS_RX);
          break;
        }
      }
    }
#endif //WITH_OVERHEARING
    //end of judging process by beacon.
  } //if(data[0] == LEAPFROG_BEACON_HEADER)
#endif /*WITH_LEAPFROG*/
}
/* ----------------- simple-udp-rpl functions end ----------------- */
/*---------------------------------------------------------------------------*/
PROCESS_THREAD(node_process, ev, data)
{
  static struct etimer et;
  PROCESS_BEGIN();

  /* 3 possible roles:
     * - role_6ln: simple node, will join any network, secured or not
     * - role_6dr: DAG root, will advertise (unsecured) beacons
     * - role_6dr_sec: DAG root, will advertise secured beacons
     * */
  static int is_coordinator = 0;
  static enum { role_6ln, role_6dr, role_6dr_sec } node_role;
  node_role = role_6ln;
  
  /* Set node with ID == 1 as coordinator, convenient in Cooja. */
  if(node_id == 1) {
    if(LLSEC802154_ENABLED) {
      node_role = role_6dr_sec;
    } else {
      node_role = role_6dr;
    }
  } else {
    node_role = role_6ln;
  }

#if CONFIG_VIA_BUTTON
  {
#define CONFIG_WAIT_TIME 5

    SENSORS_ACTIVATE(button_sensor);
    etimer_set(&et, CLOCK_SECOND * CONFIG_WAIT_TIME);

    while(!etimer_expired(&et)) {
      printf("Init: current role: %s. Will start in %u seconds. Press user button to toggle mode.\n",
                node_role == role_6ln ? "6ln" : (node_role == role_6dr) ? "6dr" : "6dr-sec",
                CONFIG_WAIT_TIME);
      PROCESS_WAIT_EVENT_UNTIL(((ev == sensors_event) &&
                                (data == &button_sensor) && button_sensor.value(0) > 0)
                               || etimer_expired(&et));
      if(ev == sensors_event && data == &button_sensor && button_sensor.value(0) > 0) {
        node_role = (node_role + 1) % 3;
        if(LLSEC802154_ENABLED == 0 && node_role == role_6dr_sec) {
          node_role = (node_role + 1) % 3;
        }
        etimer_restart(&et);
      }
    }
  }

#endif /* CONFIG_VIA_BUTTON */

  printf("Init: node starting with role %s\n",
      node_role == role_6ln ? "6ln" : (node_role == role_6dr) ? "6dr" : "6dr-sec");

  tsch_set_pan_secured(LLSEC802154_ENABLED && (node_role == role_6dr_sec));
  is_coordinator = node_role > role_6ln;

  if(is_coordinator) {
    uip_ipaddr_t prefix;
    uip_ip6addr(&prefix, UIP_DS6_DEFAULT_PREFIX, 0, 0, 0, 0, 0, 0, 0);
    net_init(&prefix);
  } else {
    net_init(NULL);
  }
  
#if WITH_ORCHESTRA
  orchestra_init();
#endif /* WITH_ORCHESTRA */

#ifdef WITH_POWERTRACE
  powertrace_start(CLOCK_SECOND * 10);
#endif
  
  /* Print out routing tables every minute */
  etimer_set(&et, CLOCK_SECOND * 60);
  //etimer_set(&et, CLOCK_SECOND * 10);
  while(1) {      
    print_network_status();
    /*Print tsch schedule*/
    tsch_schedule_print();
    PROCESS_YIELD_UNTIL(etimer_expired(&et));
    etimer_reset(&et);
  }
  
  PROCESS_END();
}
/*---------------------------------------------------------------------------*/
/* ----------------- simple-udp-rpl process start----------------- */
/*simple-udp-rpl---------------------------------------------------------------------------*/
/*simple-udp-rpl---------------------------------------------------------------------------*/
PROCESS_THREAD(unicast_sender_process, ev, data)
{
  static struct etimer uni_periodic_timer;
//  static struct etimer send_timer;
  uip_ipaddr_t *addr;


  PROCESS_BEGIN();

  //servreg_hack_init();

  // set_global_address();

  simple_udp_register(&unicast_connection, UDP_PORT,
                      NULL, UDP_PORT, receiver);

  etimer_set(&uni_periodic_timer, SEND_INTERVAL);
  while(1) {
      PROCESS_WAIT_EVENT_UNTIL(etimer_expired(&uni_periodic_timer));
      etimer_reset(&uni_periodic_timer);
//      etimer_set(&send_timer, SEND_TIME);
//      PROCESS_WAIT_EVENT_UNTIL(etimer_expired(&send_timer));

#ifdef WITH_STABLETIMER    
    if(stable_flag){
#else //WITH_STABLETIMER
    if(tsch_is_associated){
#endif //WITH_STABLETIMER
      /*--- target address decision ---*/
      /*-- to registered target with servreg_hack --*/
      //addr = servreg_hack_lookup(SERVICE_ID);
      /*-- to default route --*/
      //uip_ds6_defrt_t *default_route;
      //default_route = uip_ds6_defrt_lookup(uip_ds6_defrt_choose());
      //if(default_route != NULL) addr = &default_route->ipaddr;
      //else addr = NULL;
      /*-- decide by address directory--*/
      uip_ipaddr_t temp_ipaddr;
      uip_ip6addr(&temp_ipaddr,0xfd00,0,0,0,0xc30c,0,0,1);
      addr = &temp_ipaddr;
      /*-- linklocal rplnodes mcast --*/
      //uip_ipaddr_t temp_ipaddr;
      //uip_ip6addr(&temp_ipaddr, 0xff02,0,0,0,0,0,0,0x001a);
      //addr = &temp_ipaddr;
      /*-- to default parent --*/
      //addr = rpl_get_parent_ipaddr(default_instance->current_dag->preferred_parent); 

      /*--- sending ---*/ 
      if(addr != NULL) {
        static unsigned int message_number;
        char buf[20];

#ifdef WITH_LEAPFROG
        sprintf(buf, "%c%cHello Tada %04d", LEAPFROG_DATA_HEADER, leapfrog_data_counter + LEAPFROG_BEACON_OFFSET, message_number);
//        uip_ipaddr_t * my_addr;
//        my_addr = &uip_ds6_if.addr_list[2].ipaddr; //get own ID. [2] seems to be default
//        if(my_addr != NULL){
//          leapfrog_elimination_id_array[(int)addr->u8[15]] = leapfrog_data_counter;
//        }
        leapfrog_elimination_id_array[node_id] = leapfrog_data_counter;
        printf("LEAPFROG: prepare data own:%d pc#%d\n", node_id, leapfrog_data_counter);
        leapfrog_data_counter++;
        if(leapfrog_data_counter >= LEAPFROG_DATA_COUNTER_MAX) leapfrog_data_counter = 0;
#else
#ifdef WITH_DATA_SLOT
        sprintf(buf, "%cHello Tada %04d", APPLICATION_DATA_HEADER, message_number);
#else //WITH_DATA_SLOT
        sprintf(buf, "NoHello Tada %04d", message_number);
#endif //WITH_DATA_SLOT
#endif
        printf("DATA: Sending unicast to ");
//        uip_debug_ipaddr_print(addr);
        printf("ID:%d", addr->u8[15]);
        printf(" '");
        printf(buf);
        printf("'\n");
        message_number++;
        simple_udp_sendto(&unicast_connection, buf, strlen(buf) + 1, addr);
      } else {
        printf("DATA: addr is NULL!!");
      }
    } //if(tsch_is_associated)
  }

  PROCESS_END();
}
/* ----------------- simple-udp-rpl process end ----------------- */
/* ----------------- simple-udp-rpl process end ----------------- */

#ifdef WITH_LEAPFROG
/* ----------------- leapfrog process start----------------- */
PROCESS_THREAD(leapfrog_beaconing_process, ev, data)
{
  static struct etimer lfb_periodic_timer;
  static struct etimer lfb_send_timer;
  uip_ipaddr_t *addr;

  PROCESS_BEGIN();

  simple_udp_register(&leapfrog_unicast_connection, LEAPFROG_UDP_PORT,
                      NULL, LEAPFROG_UDP_PORT, receiver);

  etimer_set(&lfb_periodic_timer, LEAPFROG_SEND_INTERVAL);
printf("timer periodic initiated\n");
  while(1) {
      etimer_reset(&lfb_periodic_timer); //printf("timer periodic reset\n");
      PROCESS_WAIT_EVENT_UNTIL(etimer_expired(&lfb_periodic_timer)); //printf("timer periodic expired\n");
      //etimer_set(&lfb_periodic_timer, LEAPFROG_SEND_INTERVAL); printf("timer periodic initiated\n");
      etimer_set(&lfb_send_timer, LEAPFROG_SEND_TIME); //printf("timer send initiated\n");
      PROCESS_WAIT_EVENT_UNTIL(etimer_expired(&lfb_send_timer)); //printf("timer send expired\n");
    if(tsch_is_associated){
      /*--- target address decision ---*/
      /*-- linklocal rplnodes mcast --*/
      uip_ipaddr_t temp_ipaddr;
      uip_ip6addr(&temp_ipaddr, 0xff02,0,0,0,0,0,0,0x001a);
      addr = &temp_ipaddr;

      /*--- sending ---*/ 
      if(addr != NULL) {
        static unsigned int message_number;
        char buf[20];
        char possible_parent_str[1 + LEAPFROG_NUM_NEIGHBOR_NODE];

        possible_parent_str[0] = leapfrog_possible_parent_num + LEAPFROG_BEACON_OFFSET;
        int i;
        for(i = 0; i < leapfrog_possible_parent_num; i++){
          possible_parent_str[1 + i] = leapfrog_possible_parent_id_array[i] + LEAPFROG_BEACON_OFFSET;
        }

        sprintf(buf, "%cP%cG%cA%cC%sN%d", 
 	  LEAPFROG_BEACON_HEADER, 
	  leapfrog_parent_id + LEAPFROG_BEACON_OFFSET, 
	  leapfrog_grand_parent_id + LEAPFROG_BEACON_OFFSET,
          leapfrog_alt_parent_id + LEAPFROG_BEACON_OFFSET,
          possible_parent_str, //C for candidate
	  message_number);
        printf("LEAPFROG: Sending beacon");
//        uip_debug_ipaddr_print(addr);
        printf(" '");
        printf(buf);
        printf("'\n");
        message_number++;
        simple_udp_sendto(&unicast_connection, buf, strlen(buf) + 1, addr);
        //simple_udp_sendto(&unicast_connection, buf, cnt, addr);
      } else {
        printf("LEAPFROG: addr is null!!");
      }
    } //if(tsch_is_associated)
  }

  PROCESS_END();
}
/* ----------------- leapfrog process end ----------------- */
#endif /*WITH_LEAPFROG*/

#ifdef WITH_STABLETIMER
/* ----------------- stable_timer process start ----------------- */
PROCESS_THREAD(stable_timer_process, ev, data)
{
  static struct etimer stable_timer;

  PROCESS_BEGIN();
  etimer_set(&stable_timer, CLOCK_SECOND * 60 * 15); //15min
  printf("Set Stable timer\n");
  
  PROCESS_WAIT_EVENT_UNTIL(etimer_expired(&stable_timer));
  etimer_stop(&stable_timer);
   
  stable_flag = 1;
  printf("Stable timer expired!! Start to send application traffic\n");
  PROCESS_EXIT();

  PROCESS_END();
}
/* ----------------- stable_timer process end ----------------- */
#endif //WITH_STABLE_TIMER
