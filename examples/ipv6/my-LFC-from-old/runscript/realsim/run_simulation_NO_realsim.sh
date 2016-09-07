#! /bin/bash
#for realsim
#should be run from prject home

for scenario in scenario1 scenario2 scenario3
do
  #changing scenario file
  echo entering
  cd scenario/realsim
  pwd
  echo re-write csc file
  python xml_re_writer_scenario_change.py ladder_NO_realsim.csc $scenario
  echo return to upper directory
  cd ../..
  pwd #should be in project home

  #entering result saving directory
  echo entering
  cd ./result/realsim
  pwd

  if [ -d ${scenario} ]; then
    echo dir already exist. 
  else
    echo make directory ${scenario}
    mkdir ${scenario}
  fi
  echo entering
  cd ${scenario} 
  pwd #i.e. [project]/result/realsim/scenario

  if [ -d normal ]; then
    echo dir already exist. 
  else
    echo make directory normal
    mkdir normal
  fi
  echo entering
  cd normal
  pwd #i.e. [project]/result/realsim/scenario/config(no, re2, re4, re6, re8, lf)

  for i in `seq 10`
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
    java -jar $HOME/contiki/tools/cooja/dist/cooja.jar -nogui=$HOME/contiki/examples/ipv6/my-LFC-from-old/scenario/realsim/ladder_NO_realsim.csc -contiki=$HOME/contiki/
    echo return to upper directory
    cd ..
    pwd
  done
  echo return to upper directory
  cd ../../../.. #should be in project home
  pwd
done
echo all simulation finished. good job.
echo all simulation finished. good job.
echo all simulation finished. good job.
