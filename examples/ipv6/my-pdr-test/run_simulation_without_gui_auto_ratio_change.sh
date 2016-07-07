#! /bin/bash

for tx in 100 90 80 70 60 50 40 30 20 10
do
  for rx in 100 90 80 70 60 50 40 30 20 10
  do
    echo entering
    cd scenario
    pwd
    echo re-write csc file
    python xml_re_writer.py pdr-test.csc $tx $rx
    echo return tp upper directory
    cd ..
    pwd

    echo entering
    cd ./result
    pwd

    if [ -d "${tx}-${rx}" ]; then
      echo dir already exist. remove ${tx}-${rx}
      rm -rf "${tx}-${rx}"
    fi
    echo make directory ${tx}-${rx}
    mkdir "${tx}-${rx}"
    echo entering
    cd "${tx}-${rx}"
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
      java -jar $HOME/contiki/tools/cooja/dist/cooja.jar -nogui=$HOME/contiki/examples/ipv6/my-pdr-test/scenario/pdr-test.csc -contiki=$HOME/contiki/
      echo return to upper directory
      cd ..
      pwd
    done
    echo return to upper directory
    cd ../..
    pwd
  done
done
echo all simulation finished. good job.
echo all simulation finished. good job.
echo all simulation finished. good job.
