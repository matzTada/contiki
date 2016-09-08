#! /bin/bash
#for realsim
#should be run from prject home

for scenario in scenario1 scenario2 scenario3
do
  #changing scenario file
  #echo entering
  #cd scenario/realsim
  #pwd
  #echo re-write csc file
  #python xml_re_writer_scenario_change.py ladder_NO-re8_realsim.csc $scenario
  #echo return to upper directory
  #cd ../..
  #pwd #should be in project home

  for i in `seq 10`
  do

    #changing random seed
    #echo entering
    #cd ./scenario/realsim
    #pwd
    #echo re-write csc file
    #python xml_re_writer_seed_decide.py ladder_NO-re8_realsim.csc $i
    #echo return to upper directory
    #cd ../..
    #pwd #should be in project home


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

    if [ -d normal-re8 ]; then
      echo dir already exist. 
    else
      echo make directory leapfrog
      mkdir normal-re8
    fi
    echo entering
    cd normal-re8
    pwd #i.e. [project]/result/realsim/scenario/config(no, re2, re4, re6, re8, lf)

    if [ -d $i ]; then
      echo dir already exist. remove $i
      rm -rf $i
    fi
    echo make directory $i
    mkdir $i
    echo entering $i
    cd $i
    pwd #i.e. [project]/result/realsim/scenario/config(no, re2, re4, re6, re8, lf)/i
    echo execute simulation
    #java -jar $HOME/contiki/tools/cooja/dist/cooja.jar -nogui=$HOME/contiki/examples/ipv6/my-LFC-from-old/scenario/realsim/ladder_NO-re8_realsim.csc -contiki=$HOME/contiki/
    java -jar $HOME/contiki/tools/cooja/dist/cooja.jar -nogui=$HOME/contiki/examples/ipv6/my-LFC-from-old/scenario/realsim/ladder_NO-re8_realsim_gui_${scenario}.csc -contiki=$HOME/contiki/
    echo return to upper directory
    cd ../../../../.. #should be in project home
    pwd
  done
  pwd
done
echo all simulation finished. good job.
echo all simulation finished. good job.
echo all simulation finished. good job.
