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

TIMEOUT(6600000, log.log("Simulation time expired Time " + time + " PDR " + (receive_count / send_count) + " #send " + send_count +  " #receive " + receive_count + " #replication " + replication_count + " #elimination " + elimination_count +  "\n")); /* milliseconds. print last msg at timeout */

log.log("Simulation starts\n");

while(true){
    YIELD(); /* wait for another mote output */
    if(stable_flag == 1){
      if(msg.match(/Hello/)){ //if "msg" contains "Hello" in it, write "msg" to log
        log.log("COM: ID: " + id + " time " + time + " " + msg + "\n");
        if(msg.match(/Sending/)){ //count up tx
          send_count++;
          //log.log(send_count + "\n");
        }else if(msg.match(/received/)){ //count up rx
          receive_count++;
          //log.log(receive_count + "\n");
        }
      }else if(msg.match(/^(?=.*P)(?=.*radio)/)){
        log.log("PWR: ID: " + id + " time " + time + " " + msg + "\n");
      }else if(msg.match(/Replication/)){
        log.log("Rep: ID: " + id + " time " + time + " " + msg + "\n");
        replication_count++;
      }else if(msg.match(/Elimination/)){
        log.log("Eli: ID: " + id + " time " + time + " " + msg + "\n");
        elimination_count++;
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
    else if(flag600 == 0){ if(time >= 600000000){flag600 = 1; log.log("setedge 100" + "\n"); send_count = 0; receive_count = 0;}}
    else if(flag1200 == 0){ if(time >= 1200000000){flag1200 = 1; log.log("Link=100, PDR " + (receive_count/send_count) + " #s " + send_count + " #r " + receive_count + "\n"); 
      log.log("setedge 90" + "\n"); send_count = 0; receive_count = 0;}}
    else if(flag1800 == 0){ if(time >= 1800000000){flag1800 = 1; log.log("Link=90, PDR " + (receive_count/send_count) + " #s " + send_count + " #r " + receive_count + "\n"); 
      log.log("setedge 80" + "\n"); send_count = 0; receive_count = 0;}}
    else if(flag2400 == 0){ if(time >= 2400000000){flag2400 = 1; log.log("Link=80, PDR " + (receive_count/send_count) + " #s " + send_count + " #r " + receive_count + "\n"); 
      log.log("setedge 70" + "\n"); send_count = 0; receive_count = 0;}}
    else if(flag3000 == 0){ if(time >= 3000000000){flag3000 = 1; log.log("Link=70, PDR " + (receive_count/send_count) + " #s " + send_count + " #r " + receive_count + "\n"); 
      log.log("setedge 60" + "\n"); send_count = 0; receive_count = 0;}}
    else if(flag3600 == 0){ if(time >= 3600000000){flag3600 = 1; log.log("Link=60, PDR " + (receive_count/send_count) + " #s " + send_count + " #r " + receive_count + "\n"); 
      log.log("setedge 50" + "\n"); send_count = 0; receive_count = 0;}}
    else if(flag4200 == 0){ if(time >= 4200000000){flag4200 = 1; log.log("Link=50, PDR " + (receive_count/send_count) + " #s " + send_count + " #r " + receive_count + "\n"); 
      log.log("setedge 40" + "\n"); send_count = 0; receive_count = 0;}}
    else if(flag4800 == 0){ if(time >= 4800000000){flag4800 = 1; log.log("Link=40, PDR " + (receive_count/send_count) + " #s " + send_count + " #r " + receive_count + "\n"); 
      log.log("setedge 30" + "\n"); send_count = 0; receive_count = 0;}}
    else if(flag5400 == 0){ if(time >= 5400000000){flag5400 = 1; log.log("Link=30, PDR " + (receive_count/send_count) + " #s " + send_count + " #r " + receive_count + "\n"); 
      log.log("setedge 20" + "\n"); send_count = 0; receive_count = 0;}}
    else if(flag6000 == 0){ if(time >= 6000000000){flag6000 = 1; log.log("Link=20, PDR " + (receive_count/send_count) + " #s " + send_count + " #r " + receive_count + "\n"); 
      log.log("setedge 10" + "\n"); send_count = 0; receive_count = 0;}}
}
