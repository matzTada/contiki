/*
serial communication by TadaMatz
25/May/2016

based on message on contiki mailing list
*/

#include "contiki.h"
//#include "dev/serial-line.h"
#include "dev/uart0.h"

#include <stdio.h>

PROCESS(test_serial, "Serial line test process");
AUTOSTART_PROCESSES(&test_serial);

char buf[128];
int cnt;

static int uart_rx_callback(unsigned char c)
{
	printf("Received %c %u\n", c, (uint8_t)c );
	if(c == '\n'){ //LF 
		printf("Line: ");
		int i;
		for(i = 0; i < cnt; i++) putchar(buf[i]);
		cnt = 0;
		return 1;
	}
	else{
		buf[cnt++] = c;
		return 0;
	}
	//uint8_t u;
	//printf("Received %c\n", c);
	//u = (uint8_t)c;
	//printf("Received %u\n", u);
}

PROCESS_THREAD(test_serial, ev, data)
{
	PROCESS_BEGIN();
	
	cnt = 0;

	uart0_init(BAUD2UBR(115200));
	uart0_set_input(uart_rx_callback);
		
	printf("PROCESS: test_serial starts");
	
	while(1){
		PROCESS_YIELD();
	}
	
	PROCESS_END();
}
