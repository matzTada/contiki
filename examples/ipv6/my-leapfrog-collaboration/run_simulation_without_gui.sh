#! /bin/bash

cd result

for i in `seq 10`
do
  if [ -d $i ]; then
    rm -rf $i
  fi
  mkdir $i
  cd $i
  java -jar /home/tada/contiki/tools/cooja/dist/cooja.jar -nogui=/home/tada/contiki/examples/ipv6/my-leapfrog-collaboration/scenario/ladder-sender-replicate.csc -contiki=/home/tada/contiki/
  cd ..
done
