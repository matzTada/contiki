#! /bin/bash


for j in 90 80 70 60 50 40 30 20 10
do
  echo entering
  cd scenario
  pwd
  echo re-write csc file
  python xml_re_writer.py ladder-sender-replicate.csc 100 $j
  echo return tp upper directory
  cd ..
  pwd

  echo entering
  cd ./result/normal
  pwd

  if [ -d "100-${j}" ]; then
    echo dir already exist. remove 100-${j}
    rm -rf "100-${j}"
  fi
  echo make directory 100-${j}
  mkdir "100-${j}"
  echo entering
  cd "100-${j}"
  pwd

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
    pwd
    echo execute simulation
    java -jar $HOME/contiki/tools/cooja/dist/cooja.jar -nogui=$HOME/contiki/examples/ipv6/my-leapfrog-collaboration/scenario/ladder-sender-replicate.csc -contiki=$HOME/contiki/
    echo return to upper directory
    cd ..
    pwd
  done
  echo return to upper directory
  cd ../../.. 
  pwd
done
echo all simulation finished. good job.
echo all simulation finished. good job.
echo all simulation finished. good job.
