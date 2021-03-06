#! /bin/bash


for j in 100
do
  echo entering
  cd scenario
  pwd
  echo re-write csc file
  python xml_re_writer.py check.csc 100 $j
  echo return tp upper directory
  cd ..
  pwd

  echo entering
  cd ./result/check
  pwd

  if [ -d "100-${j}" ]; then
    echo dir already exist. 
  else
    echo make directory 100-${j}
    mkdir "100-${j}"
  fi
  echo entering
  cd "100-${j}"
  pwd

  for i in 1 2 3 4 5 6 7 8 9 10
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
    java -jar $HOME/contiki/tools/cooja/dist/cooja.jar -nogui=$HOME/contiki/examples/ipv6/my-LFC-sim-UDGM/scenario/check.csc -contiki=$HOME/contiki/
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
