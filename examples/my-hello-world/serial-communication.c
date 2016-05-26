/*
serial communication by TadaMatz
25/May/2016
copy of contiki wiki Input-and-output

does not work
*/

#include "contiki.h"
#include "dev/uart0.h"
#include "dev/serial-line.h"
#include <stdio.h>

PROCESS(test_serial, "Serial line test process");
AUTOSTART_PROCESSES(&test_serial, &serial_line_process);

PROCESS_THREAD(test_serial, ev, data)
{
	PROCESS_BEGIN();

	uart0_set_input(serial_line_input_byte); //here must be changed corresponding to mote
	serial_line_init();
	
	while(1){
		PROCESS_YIELD();
		if(ev == serial_line_event_message){
			printf("received line: %s\n", (char *) data);
		}
	}
	
	PROCESS_END();
}
