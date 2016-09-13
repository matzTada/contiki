/*
 * Example Contiki test script (JavaScript).
 * A Contiki test script acts on mote output, such as via printf()'s.
 * The script may operate on the following variables:
 *  Mote mote, int id, String msg
 * 
 * modified by TadaMatz 
 */

send_count = 0;
receive_count = 0;
replication_count = 0;
elimination_count = 0;
stable_flag = 1; //if 0 useing stable timer, 1 always log
total_send_count = 0;
total_receive_count = 0;
total_replication_count = 0;
total_elimination_count = 0;

//flags for realsim test
flag1 = 0;
flag2 = 0;
flag3 = 0;
flag4 = 0;
flag5 = 0;
flag6 = 0;
flag7 = 0;
flag8 = 0;
flag9 = 0;
flag10 = 0;
flag11 = 0;
flag12 = 0;
flag13 = 0;
flag14 = 0;
flag15 = 0;

TIMEOUT(4808000, log.log("Simulation time expired Time " + time + " PDR " + (total_receive_count / total_send_count) + " #send " + total_send_count +  " #receive " + total_receive_count + " #replication " + total_replication_count + " #elimination " + total_elimination_count +  "\n")); /* milliseconds. print last msg at timeout */

log.log("Simulation starts\n");

while(true){
    YIELD(); /* wait for another mote output */
    if(stable_flag == 1){
      if(msg.match(/Hello/)){ //if "msg" contains "Hello" in it, write "msg" to log
        log.log("COM: ID: " + id + " time " + time + " " + msg + "\n");
        if(msg.match(/Sending/)){ //count up tx
          send_count++;
          total_send_count++;
          //log.log(send_count + "\n");
        }else if(msg.match(/received/)){ //count up rx
          receive_count++;
          total_receive_count++;
          //log.log(receive_count + "\n");
        }
      }else if(msg.match(/^(?=.*P)(?=.*radio)/)){
        log.log("PWR: ID: " + id + " time " + time + " " + msg + "\n");
      }else if(msg.match(/Replication/)){
        log.log("Rep: ID: " + id + " time " + time + " " + msg + "\n");
        replication_count++;
        total_replication_count++;
      }else if(msg.match(/Elimination/)){
        log.log("Eli: ID: " + id + " time " + time + " " + msg + "\n");
        elimination_count++;
        total_elimination_count++;
      }else if(msg.match(/LEAPFROG: default route/)){
        log.log("Def: ID: " + id + " time " + time + " " + msg + "\n");
      }else{
        log.log("Oth: ID: " + id + " time " + time + " " + msg + "\n");
      }
    }
    if(msg.match(/Starting/)){
      log.log("Start: ID: " + id + " time " + time + " " + msg + "\n");
    }else if(msg.match(/Stable timer expired/)){
      stable_flag = 1;
      log.log("Stable: ID: " + id + " time " + time + " " + msg + "\n");
    }
    //realsim test
    if (flag1 == 0){if(time >= 30000000){
      flag1 = 1;
      log.log(time + " configure with RealSim" + "\n");
    }}
    else if(flag2 == 0){ if(time >= 900000000){
      flag2 = 1; 
      log.log(time + " setedge def" + "\n"); send_count = 0; receive_count = 0; replication_count = 0; elimination_count = 0;
    }}
    else if(flag3 == 0){ if(time >= 1200000000){
      flag3 = 1;
      log.log(time + " report def PDR " + (receive_count/send_count) + " #s " + send_count + " #r " + receive_count + " #rep " + replication_count + " #eli " + elimination_count + "\n"); 
      log.log(time + " setedge bad id:2" + "\n"); send_count = 0; receive_count = 0; replication_count = 0; elimination_count = 0;
    }}
    else if(flag4 == 0){ if(time >= 1500000000){
      flag4 = 1;
      log.log(time + " report bad id:2 PDR " + (receive_count/send_count) + " #s " + send_count + " #r " + receive_count + " #rep " + replication_count + " #eli " + elimination_count + "\n"); 
      log.log(time + " setedge def id:2" + "\n"); send_count = 0; receive_count = 0; replication_count = 0; elimination_count = 0;
    }}
    else if(flag5 == 0){ if(time >= 1800000000){
      flag5 = 1;
      log.log(time + " report def id:2 PDR " + (receive_count/send_count) + " #s " + send_count + " #r " + receive_count + " #rep " + replication_count + " #eli " + elimination_count + "\n"); 
      log.log(time + " setedge bad id:5" + "\n"); send_count = 0; receive_count = 0; replication_count = 0; elimination_count = 0;
    }}
    else if(flag6 == 0){ if(time >= 2100000000){
      flag6 = 1; 
      log.log(time + " report bad id:5 PDR " + (receive_count/send_count) + " #s " + send_count + " #r " + receive_count + " #rep " + replication_count + " #eli " + elimination_count + "\n"); 
      log.log(time + " setedge def id:5" + "\n"); send_count = 0; receive_count = 0; replication_count = 0; elimination_count = 0;
    }}
    else if(flag7 == 0){ if(time >= 2400000000){
      flag7 = 1;
      log.log(time + " report def id:5 PDR " + (receive_count/send_count) + " #s " + send_count + " #r " + receive_count + " #rep " + replication_count + " #eli " + elimination_count + "\n"); 
      log.log(time + " setedge bad id:6" + "\n"); send_count = 0; receive_count = 0; replication_count = 0; elimination_count = 0;
    }}
    else if(flag8 == 0){ if(time >= 2700000000){
      flag8 = 1;
      log.log(time + " report bad id:6 PDR " + (receive_count/send_count) + " #s " + send_count + " #r " + receive_count + " #rep " + replication_count + " #eli " + elimination_count + "\n"); 
      log.log(time + " setedge def id:6" + "\n"); send_count = 0; receive_count = 0; replication_count = 0; elimination_count = 0;
    }}
    else if(flag9 == 0){ if(time >= 3000000000){
      flag9 = 1;
      log.log(time + " report def id:6 PDR " + (receive_count/send_count) + " #s " + send_count + " #r " + receive_count + " #rep " + replication_count + " #eli " + elimination_count + "\n"); 
      log.log(time + " setedge bad id:3" + "\n"); send_count = 0; receive_count = 0; replication_count = 0; elimination_count = 0;
    }}
    else if(flag10 == 0){ if(time >= 3300000000){
      flag10 = 1;
      log.log(time + " report bad id:3 PDR " + (receive_count/send_count) + " #s " + send_count + " #r " + receive_count + " #rep " + replication_count + " #eli " + elimination_count + "\n"); 
      log.log(time + " setedge def id:3" + "\n"); send_count = 0; receive_count = 0; replication_count = 0; elimination_count = 0;
    }}
    else if(flag11 == 0){ if(time >= 3600000000){
      flag11 = 1;
      log.log(time + " report def id:3 PDR " + (receive_count/send_count) + " #s " + send_count + " #r " + receive_count + " #rep " + replication_count + " #eli " + elimination_count + "\n"); 
      log.log(time + " setedge bad id:4" + "\n"); send_count = 0; receive_count = 0; replication_count = 0; elimination_count = 0;
    }}
    else if(flag12 == 0){ if(time >= 3900000000){
      flag12 = 1;
      log.log(time + " report bad id:4 PDR " + (receive_count/send_count) + " #s " + send_count + " #r " + receive_count + " #rep " + replication_count + " #eli " + elimination_count + "\n"); 
      log.log(time + " setedge def id:4" + "\n"); send_count = 0; receive_count = 0; replication_count = 0; elimination_count = 0;
    }}
    else if(flag13 == 0){ if(time >= 4200000000){
      flag13 = 1;
      log.log(time + " report def id:4 PDR " + (receive_count/send_count) + " #s " + send_count + " #r " + receive_count + " #rep " + replication_count + " #eli " + elimination_count + "\n"); 
      log.log(time + " setedge bad id:7" + "\n"); send_count = 0; receive_count = 0; replication_count = 0; elimination_count = 0;
    }}
    else if(flag14 == 0){ if(time >= 4500000000){
      flag14 = 1;
      log.log(time + " report bad id:7 PDR " + (receive_count/send_count) + " #s " + send_count + " #r " + receive_count + " #rep " + replication_count + " #eli " + elimination_count + "\n"); 
      log.log(time + " setedge def id:7" + "\n"); send_count = 0; receive_count = 0; replication_count = 0; elimination_count = 0;
    }}
    else if(flag15 == 0){ if(time >= 4800000000){
      flag15 = 1;
      log.log(time + " report def id:7 PDR " + (receive_count/send_count) + " #s " + send_count + " #r " + receive_count + " #rep " + replication_count + " #eli " + elimination_count + "\n"); 
      // log.log(time + " setedge def id:2" + "\n"); send_count = 0; receive_count = 0; replication_count = 0; elimination_count = 0;
    }}
}
