#! /bin/bash


echo entering
cd scenario
pwd
echo re-write csc file
python xml_re_writer.py ladder_SINGLE.csc 100 100
echo return tp upper directory
cd ..
pwd

echo entering
cd ./result/single
pwd

echo execute simulation
java -jar $HOME/contiki/tools/cooja/dist/cooja.jar -nogui=$HOME/contiki/examples/ipv6/my-LFC-from-old/scenario/ladder_SINGLE.csc -contiki=$HOME/contiki/
echo return to upper directory
cd ../..

echo all simulation finished. good job.
echo all simulation finished. good job.
echo all simulation finished. good job.
