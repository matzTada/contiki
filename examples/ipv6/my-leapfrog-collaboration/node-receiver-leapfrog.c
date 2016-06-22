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

#define SEND_INTERVAL   (10 * CLOCK_SECOND)
#define SEND_TIME   (random_rand() % (SEND_INTERVAL))

static struct simple_udp_connection unicast_connection;

PROCESS(unicast_receiver_process, "Unicast receiver example process");
// AUTOSTART_PROCESSES(&unicast_receiver_process);
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

char leapfrog_data_counter = 0;
char leapfrog_elimination_id_array[LEAPFROG_NUM_NODE];

extern rpl_instance_t * default_instance;
static struct simple_udp_connection leapfrog_unicast_connection;
PROCESS(leapfrog_beaconing_process, "Leapfrog beaconing process");

#ifdef WITH_LEAPFROG_TSCH
// extern struct tsch_slotframe *sf_lfat; //leapfrog alt traffic
linkaddr_t alt_parent_linkaddr = {{0xc1, 0x0c, 0, 0, 0, 0, 0, 0}};
#endif /*WITH_LEAPFROG_TSCH*/

#endif //WITH_LEAPFROG
/* ----------------- leapfrog include and declaration end ----------------- */


/*---------------------------------------------------------------------------*/
#ifdef WITH_LEAPFROG
PROCESS(node_process, "RPL Node receiver leapfrog");
#if CONFIG_VIA_BUTTON
AUTOSTART_PROCESSES(&node_process, &sensors_process, &unicast_receiver_process, &leapfrog_beaconing_process);
#else /* CONFIG_VIA_BUTTON */
AUTOSTART_PROCESSES(&node_process, &unicast_receiver_process, &leapfrog_beaconing_process);
#endif /* CONFIG_VIA_BUTTON */
#else /*WITH_LEAPFROG*/
PROCESS(node_process, "RPL Node receiver leapfrog");
#if CONFIG_VIA_BUTTON
AUTOSTART_PROCESSES(&node_process, &sensors_process, &unicast_receiver_process);
#else /* CONFIG_VIA_BUTTON */
AUTOSTART_PROCESSES(&node_process, &unicast_receiver_process);
#endif /* CONFIG_VIA_BUTTON */
#endif /*WITH_LEAPFROG*/
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
// #ifdef WITH_LEAPFROG //for packet elimination
//   int leapfrog_elimination_flag = 0;
    
//   if(data[0] == LEAPFROG_DATA_HEADER){
//     char tmp_lf_pc = data[1] - LEAPFROG_BEACON_OFFSET;
//     int tmp_sid = sender_addr->u8[15];
//     char tmp_lf_an = leapfrog_elimination_id_array[tmp_sid];

//     if(tmp_lf_an <= LEAPFROG_DATA_COUNTER_WIDTH){
//       if(tmp_lf_pc <= tmp_lf_an || LEAPFROG_DATA_COUNTER_MAX - (LEAPFROG_DATA_COUNTER_WIDTH - tmp_lf_an ) <= tmp_lf_pc) leapfrog_elimination_flag = 1; 
//     }else{
//       if(tmp_lf_an - LEAPFROG_DATA_COUNTER_WIDTH <= tmp_lf_pc && tmp_lf_pc <= tmp_lf_an) leapfrog_elimination_flag = 1;
//     }

//     if(leapfrog_elimination_flag == 1){
//       PRINTF("LEAPFROG: Elimination discard data\n");
//     }else{
//       PRINTF("LEAPFROG: ");
//       leapfrog_elimination_id_array[tmp_sid] = tmp_lf_pc;
//     }
//   }

//   if(leapfrog_elimination_flag != 1){
// #endif /*WITH_LEAPFROG*/

  printf("DATA: received from ");
  uip_debug_ipaddr_print(sender_addr);
  printf(" on port %d from port %d with length %d: '%s'\n",
         receiver_port, sender_port, datalen, data);

#ifdef WITH_LEAPFROG //for beaconing
  if(data[0] == LEAPFROG_BEACON_HEADER){
    char temp_sid = 0; //sender id of packet
    char temp_pid = 0; //sender's parent id
    char temp_gid = 0; //sender's grand parent id
    char temp_aid = 0; //sender's alt parent id
    temp_sid = sender_addr->u8[15]; //get most least byte. must be modified to store whole address
    temp_pid = data[2] - LEAPFROG_BEACON_OFFSET;
    temp_gid = data[4] - LEAPFROG_BEACON_OFFSET;
    temp_aid = data[6] - LEAPFROG_BEACON_OFFSET;
    printf("LEAPFROG: beacon S %d P %d GP %d AP %d\n", temp_sid, temp_pid, temp_gid, temp_aid);
    
    //judge and registor parent, grandparent, alt parent 
    char my_id = 0;
    uip_ipaddr_t * addr;
    addr = &uip_ds6_if.addr_list[2].ipaddr; //get own ID. [2] seems to be default
    if(addr != NULL){
      my_id = addr->u8[15];
    }
    addr = rpl_get_parent_ipaddr(default_instance->current_dag->preferred_parent);
    if(addr != NULL){
      char my_pid = addr->u8[15];
//      if(leapfrog_parent_id == 0){ //registor parent
//        leapfrog_parent_id = my_pid;
//      }else 
      if(leapfrog_parent_id != my_pid){ //new parent and reset P, GP, AP
        leapfrog_parent_id = my_pid;
        leapfrog_grand_parent_id = 0;
        leapfrog_alt_parent_id = 0;
        printf("LEAPFROG: reset P GP AP\n");
      }
      if(leapfrog_parent_id > 0 && leapfrog_parent_id == my_pid){ //judge Grand Parent
        if(temp_sid == my_pid){
          if(temp_pid > 0 && temp_pid != my_pid){
            leapfrog_grand_parent_id = temp_pid; //get grand parent
          }
        }
      }
      if(leapfrog_grand_parent_id > 0 && temp_pid > 0 && leapfrog_grand_parent_id == temp_pid && leapfrog_parent_id != temp_sid){ //judge Alt Parent
        if(leapfrog_alt_parent_id != temp_sid){
          leapfrog_alt_parent_id = temp_sid; //get alt parent
          linkaddr_copy(&alt_parent_linkaddr, packetbuf_addr(PACKETBUF_ADDR_SENDER));
          //alt_parent_linkaddr.u8[7] = leapfrog_alt_parent_id; //for tsch
          printf("LEAPFROG: get new AP %d %02x:%02x:%02x:%02x:%02x:%02x:%02x:%02x\n", 
            leapfrog_alt_parent_id,
            alt_parent_linkaddr.u8[0],
            alt_parent_linkaddr.u8[1],
            alt_parent_linkaddr.u8[2],
            alt_parent_linkaddr.u8[3],
            alt_parent_linkaddr.u8[4],
            alt_parent_linkaddr.u8[5],
            alt_parent_linkaddr.u8[6],
            alt_parent_linkaddr.u8[7]
           );
#ifdef WITH_LEAPFROG_TSCH //add unicast tx link to AP based on own(child) ID
          printf("LEAPFROG-TSCH: update timeslot tx -> AP %d\n", leapfrog_alt_parent_id);
          
          orchestra_leapfrog_add_uc_tx_link(leapfrog_alt_parent_id);
          // uint16_t child_timeslot = 0;
          // child_timeslot = linkaddr_node_addr.u8[7] % ORCHESTRA_LEAPFROG_ALT_TRAFFIC_PERIOD; //like ORCHESTRA_LINKADDR_HASH(linkaddr)%PERIOD
          // linkaddr_t altparent_linkaddr = {{0xc1, 0x0c, 0, 0, 0, 0, 0, leapfrog_alt_parent_id}};

          // struct tsch_link *child_l;
          // child_l = tsch_schedule_get_link_by_timeslot(sf_lfat, child_timeslot);
          // if(child_l != NULL) {
          //   tsch_schedule_remove_link(sf_lfat, child_l);
          // }
          // tsch_schedule_add_link(
          //   sf_lfat,
          //   LINK_OPTION_TX | LINK_OPTION_SHARED,
          //   LINK_TYPE_NORMAL,
          //   &altparent_linkaddr, //dest linkaddr
          //   child_timeslot,
          //   sf_lfat->handle); //should be modified to get correct channel_offset of link
#endif /*WITH_LEAPFROG_TSCH*/
        }
      }
      printf("LEAPFROG: own P %d GP %d AP %d\n", leapfrog_parent_id, leapfrog_grand_parent_id, leapfrog_alt_parent_id);

#ifdef WITH_LEAPFROG_TSCH //judge I am sender's Alt Parent
      if(temp_aid != 0 && my_id == temp_aid){
        printf("LEAPFROG-TSCH: update timeslot rx <- (alt)C %d\n", temp_sid);

        orchestra_leapfrog_add_uc_rx_link(temp_sid);
        // //linkaddr_t child_linkaddr = {{0xc1, 0x0c, 0, 0, 0, 0, 0, temp_sid}};
        // uint16_t altparent_timeslot = temp_sid % ORCHESTRA_LEAPFROG_ALT_TRAFFIC_PERIOD; //like ORCHESTRA_LINKADDR_HASH(linkaddr)%PERIOD

        // struct tsch_link *altparent_l;
        // altparent_l = tsch_schedule_get_link_by_timeslot(sf_lfat, altparent_timeslot);
        // if(altparent_l != NULL) {
        //   tsch_schedule_remove_link(sf_lfat, altparent_l);
        // }
        // tsch_schedule_add_link(
        //   sf_lfat,
        //   LINK_OPTION_RX,
        //   LINK_TYPE_NORMAL,
        //   &tsch_broadcast_address, //welcome everyone
        //   altparent_timeslot,
        //   sf_lfat->handle); //should be modified to get correct channel_offset of link
      }
#endif /*WITH_LEAPFROG_TSCH*/      
    }
  }

  // }else{
  //   //receiving processes is skipped because of elimination
  // }
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
PROCESS_THREAD(unicast_receiver_process, ev, data)
{
  //uip_ipaddr_t *ipaddr;

  PROCESS_BEGIN();

  //servreg_hack_init();

  // ipaddr = set_global_address();
  //ipaddr = &uip_ds6_if.addr_list[0].ipaddr; //oh... should be nice

  // create_rpl_dag(ipaddr);

  //servreg_hack_register(SERVICE_ID, ipaddr);

  simple_udp_register(&unicast_connection, UDP_PORT,
                      NULL, UDP_PORT, receiver);

  while(1) {
    PROCESS_WAIT_EVENT();
  }
  PROCESS_END();
}
/* ----------------- simple-udp-rpl process end ----------------- */

#ifdef WITH_LEAPFROG
/* ----------------- leapfrog process start----------------- */
PROCESS_THREAD(leapfrog_beaconing_process, ev, data)
{
  static struct etimer periodic_timer;
  static struct etimer send_timer;
  uip_ipaddr_t *addr;

  PROCESS_BEGIN();

  simple_udp_register(&leapfrog_unicast_connection, LEAPFROG_UDP_PORT,
                      NULL, LEAPFROG_UDP_PORT, receiver);

  etimer_set(&periodic_timer, LEAPFROG_SEND_INTERVAL);
  while(1) {
    PROCESS_WAIT_EVENT_UNTIL(etimer_expired(&periodic_timer));
    etimer_reset(&periodic_timer);
    etimer_set(&send_timer, LEAPFROG_SEND_TIME);

    PROCESS_WAIT_EVENT_UNTIL(etimer_expired(&send_timer));
    
    /*--- target address decision ---*/
    /*-- linklocal rplnodes mcast --*/
    uip_ipaddr_t temp_ipaddr;
    uip_ip6addr(&temp_ipaddr, 0xff02,0,0,0,0,0,0,0x001a);
    addr = &temp_ipaddr;

    /*--- sending ---*/ 
    if(addr != NULL) {
      static unsigned int message_number;
      char buf[20];

      sprintf(buf, "%cP%cG%cA%cN%d", 
	LEAPFROG_BEACON_HEADER, 
	leapfrog_parent_id + LEAPFROG_BEACON_OFFSET, 
	leapfrog_grand_parent_id + LEAPFROG_BEACON_OFFSET,
        leapfrog_alt_parent_id + LEAPFROG_BEACON_OFFSET,
	message_number);
      printf("LEAPFROG: Sending beacon to ");
      uip_debug_ipaddr_print(addr);
      printf(" '");
      printf(buf);
      printf("'\n");
      message_number++;
      simple_udp_sendto(&unicast_connection, buf, strlen(buf) + 1, addr);
      //simple_udp_sendto(&unicast_connection, buf, cnt, addr);
    } else {
      printf("LEAPFROG: addr is null!!");
    }
  }

  PROCESS_END();
}
/* ----------------- leapfrog process end ----------------- */
#endif /*WITH_LEAPFROG*/
