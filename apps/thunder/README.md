# Thunder

## Overview

Manual configuration of TSCH scheduling. All schedules are defined at the intialization process. No timeslots are deleted in the network, in other words, all timeslots are fixed.

## Requirements

Thunder requires a system running TSCH and RPL.

## Getting Started

To use Thunder, add a couple global definitions, e.g in your `project-conf.h` file.

Disable 6TiSCH minimal schedule:

`#define TSCH_SCHEDULE_CONF_WITH_6TISCH_MINIMAL 0`

Enable TSCH link selector (allows Orchestra to assign TSCH links to outgoing packets):

`#define TSCH_CONF_WITH_LINK_SELECTOR 1`

Set up the following callbacks:  

```
#define TSCH_CALLBACK_PACKET_READY thunder_callback_packet_ready  
#define TSCH_CALLBACK_NEW_TIME_SOURCE thunder_callback_new_time_source
```

To use Orchestra, fist add it to your makefile `APPS` with `APPS += thunder`.
 
Finally:
* add Orchestra to your makefile `APPS` with `APPS += orchestra`;
* start Orchestra by calling `thunder_init()` from your application, after
including `#include "thunder.h"`.

##Memo

* Source codes are based on Orchestra  
* Store timeslots for BOTH unicast and broadcast
* do not make a timeslot dedcicated for EB
* 