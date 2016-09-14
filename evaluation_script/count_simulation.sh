#!/bin/bash

if [ $# -eq 0 ]; then
  echo "explore all"

  grep -hrc "Starting Cooja" > tmp_grepped_file.txt #looking for in COOJA.testlog
  echo "Attempted simulation"
  grep -c 1 tmp_grepped_file.txt

  grep -hrc "time expired" > tmp_grepped_file.txt #looking for in COOJA.testlog
  echo "Launched simulation"
  grep -c 1 tmp_grepped_file.txt
else
  echo "having argument"
  grep -hrc "Starting Cooja" $@ > tmp_grepped_file.txt #looking for in COOJA.testlog
  echo "Attempted simulation"
  grep -c 1 tmp_grepped_file.txt

  grep -hrc "time expired" $@ > tmp_grepped_file.txt #looking for in COOJA.testlog
  echo "Launched simulation"
  grep -c 1 tmp_grepped_file.txt
fi


rm tmp_grepped_file.txt



