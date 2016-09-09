#!/bin/bash

grep -hrc "Starting Cooja" > tmp_grepped_file.txt #looking for in COOJA.testlog
echo "Attempted simulation"
grep -c 1 tmp_grepped_file.txt

grep -hrc "time expired" > tmp_grepped_file.txt #looking for in COOJA.testlog
echo "Launched simulation"
grep -c 1 tmp_grepped_file.txt



