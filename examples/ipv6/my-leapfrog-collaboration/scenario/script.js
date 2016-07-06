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

TIMEOUT(180000, log.log("Simulation time expired PDR " + (receive_count / send_count) + " % #send " + send_count +  " #receive " + receive_count + "\n")); /* milliseconds. print last msg at timeout */

log.log("Simulation starts\n");

while(true){
    YIELD(); /* wait for another mote output */
    if(msg.match(/Hello/)){ //if "msg" contains "Hello" in it, write "msg" to log
      log.log("COM: ID: " + id + " " + msg + "\n");
      if(msg.match(/Sending/)){ //count up tx
        send_count++;
        //log.log(send_count + "\n");
      }else if(msg.match(/received/)){ //count up rx
        receive_count++;
        //log.log(receive_count + "\n");
      }
    }else if(msg.match(/radio/)){
      log.log("PWR: ID: " + id + " " + msg + "\n");
    }
}
