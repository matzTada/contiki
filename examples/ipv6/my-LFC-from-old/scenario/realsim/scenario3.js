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
flag600 = 0;
flag1200 = 0;
flag1800 = 0;
flag2400 = 0;
flag3000 = 0;
flag3600 = 0;
flag4200 = 0;
flag4800 = 0;
flag5400 = 0;
flag6000 = 0;
flag6600 = 0;

TIMEOUT(1508000, log.log("Simulation time expired Time " + time + " PDR " + (total_receive_count / total_send_count) + " #send " + total_send_count +  " #receive " + total_receive_count + " #replication " + total_replication_count + " #elimination " + total_elimination_count +  "\n")); /* milliseconds. print last msg at timeout */

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
    if (flag1 == 0){
      if(time >= 1000000){
        flag1 = 1;
        log.log("setedge 100" + "\n");
      }
    }
    else if(flag600 == 0){ if(time >= 600000000){
      flag600 = 1; 
      log.log("start default" + "\n"); 
      log.log("setedge 90" + "\n"); send_count = 0; receive_count = 0; replication_count = 0; elimination_count = 0;
    }}
    else if(flag1200 == 0){ if(time >= 900000000){
      flag1200 = 1;
      log.log("report link=90, PDR " + (receive_count/send_count) + " #s " + send_count + " #r " + receive_count + " #rep " + replication_count + " #eli " + elimination_count + "\n"); 
      log.log("setedge 10" + "\n"); send_count = 0; receive_count = 0; replication_count = 0; elimination_count = 0;
    }}
    else if(flag1800 == 0){ if(time >= 1200000000){
      flag1800 = 1;
      log.log("report link=10, PDR " + (receive_count/send_count) + " #s " + send_count + " #r " + receive_count + " #rep " + replication_count + " #eli " + elimination_count + "\n"); 
      log.log("setedge 90" + "\n"); send_count = 0; receive_count = 0; replication_count = 0; elimination_count = 0;
    }}
    else if(flag2400 == 0){ if(time >= 1500000000){
      flag2400 = 1;
      log.log("report link=90, PDR " + (receive_count/send_count) + " #s " + send_count + " #r " + receive_count + " #rep " + replication_count + " #eli " + elimination_count + "\n"); 
      // log.log("setedge 60" + "\n"); send_count = 0; receive_count = 0; replication_count = 0; elimination_count = 0;
    }}
    // else if(flag3000 == 0){ if(time >= 2400000000){
    //   flag3000 = 1; 
    //   log.log("report link=60, PDR " + (receive_count/send_count) + " #s " + send_count + " #r " + receive_count + " #rep " + replication_count + " #eli " + elimination_count + "\n"); 
    //   log.log("setedge 50" + "\n"); send_count = 0; receive_count = 0; replication_count = 0; elimination_count = 0;
    // }}
    // else if(flag3600 == 0){ if(time >= 3000000000){
    //   flag3600 = 1;
    //   log.log("report link=50, PDR " + (receive_count/send_count) + " #s " + send_count + " #r " + receive_count + " #rep " + replication_count + " #eli " + elimination_count + "\n"); 
    //   log.log("setedge 40" + "\n"); send_count = 0; receive_count = 0; replication_count = 0; elimination_count = 0;
    // }}
    // else if(flag4200 == 0){ if(time >= 3300000000){
    //   flag4200 = 1;
    //   log.log("report link=40, PDR " + (receive_count/send_count) + " #s " + send_count + " #r " + receive_count + " #rep " + replication_count + " #eli " + elimination_count + "\n"); 
    //   log.log("setedge 30" + "\n"); send_count = 0; receive_count = 0; replication_count = 0; elimination_count = 0;
    // }}
    // else if(flag4800 == 0){ if(time >= 3600000000){
    //   flag4800 = 1;
    //   log.log("report link=30, PDR " + (receive_count/send_count) + " #s " + send_count + " #r " + receive_count + " #rep " + replication_count + " #eli " + elimination_count + "\n"); 
    //   log.log("setedge 20" + "\n"); send_count = 0; receive_count = 0; replication_count = 0; elimination_count = 0;
    // }}
    // else if(flag5400 == 0){ if(time >= 4200000000){
    //   flag5400 = 1;
    //   log.log("report link=20, PDR " + (receive_count/send_count) + " #s " + send_count + " #r " + receive_count + " #rep " + replication_count + " #eli " + elimination_count + "\n"); 
    //   log.log("setedge 10" + "\n"); send_count = 0; receive_count = 0; replication_count = 0; elimination_count = 0;
    // }}
    // else if(flag6000 == 0){ if(time >= 4800000000){
    //   flag6000 = 1;
      // log.log("report link=10, PDR " + (receive_count/send_count) + " #s " + send_count + " #r " + receive_count + " #rep " + replication_count + " #eli " + elimination_count + "\n"); 
      // log.log("setedge 10" + "\n"); send_count = 0; receive_count = 0; replication_count = 0; elimination_count = 0;
    // }}
    // else if(flag6600 == 0){ if(time >= 6600000000){
    //   flag6600 = 1;
    //   log.log("report link=10, PDR " + (receive_count/send_count) + " #s " + send_count + " #r " + receive_count + " #rep " + replication_count + " #eli " + elimination_count + "\n"); 
    //   log.log("setedge 10" + "\n"); send_count = 0; receive_count = 0; replication_count = 0; elimination_count = 0;
    // }}
}
