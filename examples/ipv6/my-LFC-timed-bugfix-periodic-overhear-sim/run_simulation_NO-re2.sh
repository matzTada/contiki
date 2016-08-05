#! /bin/bash
for i in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20
do
  echo entering
  cd scenario
  pwd
  echo re-write csc file
  python xml_re_writer_dgrm.py overhearing_dgrm_NO-re2.csc pdr_for_simulation.csv $i
  echo return to upper directory
  cd ..
  pwd

  echo entering
  cd ./result/normal-re2
  pwd
 
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
  java -jar $HOME/contiki/tools/cooja/dist/cooja.jar -nogui=$HOME/contiki/examples/ipv6/my-LFC-timed-bugfix-periodic-overhear-sim/scenario/overhearing_dgrm_NO-re2.csc -contiki=$HOME/contiki/
  echo return to upper directory
  cd ..
  pwd

  echo return to upper directory
  cd ../..
  pwd

done
echo all simulation finished. good job.
echo all simulation finished. good job.
echo all simulation finished. good job.
