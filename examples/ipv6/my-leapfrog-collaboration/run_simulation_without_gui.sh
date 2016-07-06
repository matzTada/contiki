#! /bin/bash

cd result

for i in `seq 3`
do
  if [ -d $i ]; then
    echo dir already exist. remove $i
    rm -rf $i
  fi
  echo make directory $i
  mkdir $i
  echo entering $i
  cd $i
  echo execute simulation
  java -jar /homes/tmatsui/contiki/tools/cooja/dist/cooja.jar -nogui=/homes/tmatsui/contiki/examples/ipv6/my-leapfrog-collaboration/scenario/ladder-sender-replicate.csc -contiki=/homes/tmatsui/contiki/
  cd ..
done
