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
    if (time == 1000) log.log("setedge 100")
    else if(time == 600000) log.log("setedge 100")
    else if(time == 1200000) log.log("setedge 90")
    else if(time == 1800000) log.log("setedge 80")
    else if(time == 2400000) log.log("setedge 70")
    else if(time == 3000000) log.log("setedge 60")
    else if(time == 3600000) log.log("setedge 50")
    else if(time == 4200000) log.log("setedge 40")
    else if(time == 4800000) log.log("setedge 30")
    else if(time == 5400000) log.log("setedge 20")
    else if(time == 6000000) log.log("setedge 10")
}
