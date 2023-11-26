#!/bin/bash

mkdir part1
mkdir part2a
mkdir part2b
mkdir part3

./waf --run "scratch/Part1_334 --transport_prot=TcpVegas" > part1/vegas.dat 2>&1 &
echo "TCP Vegas Data Generated"
wait
./waf --run "scratch/Part1_334 --transport_prot=TcpVeno" > part1/veno.dat 2>&1 &
echo "TCP Veno Data Generated"
wait
./waf --run "scratch/Part1_334 --transport_prot=TcpNewReno" > part1/newreno.dat 2>&1 &
echo "TCP NewReno Data Generated"
wait
./waf --run "scratch/Part1_334 --transport_prot=TcpWestwood" > part1/westwood.dat 2>&1 &
echo "TCP WestWood Data Generated"
wait 

./waf --run "scratch/part2 --crate=3Mbps" > part2a/c3.txt 2>&1 &
echo "Data Generated for channel rate = 3Mbps"
wait
./waf --run "scratch/part2 --crate=5Mbps" > part2a/c5.txt 2>&1 &
echo "Data Generated for channel rate = 5Mbps"
wait
./waf --run "scratch/part2 --crate=10Mbps" > part2a/c10.txt 2>&1 &
echo "Data Generated for channel rate = 10Mbps"
wait
./waf --run "scratch/part2 --crate=15Mbps" > part2a/c15.txt 2>&1 &
echo "Data Generated for channel rate = 15Mbps"
wait
./waf --run "scratch/part2 --crate=30Mbps" > part2a/c30.txt 2>&1 &
echo "Data Generated for channel rate = 30Mbps"
wait

./waf --run "scratch/part2 --apprate=1Mbps" > part2b/a1.txt 2>&1 &
echo "Data Generated for Application rate = 1Mbps"
wait
./waf --run "scratch/part2 --apprate=2Mbps" > part2b/a2.txt 2>&1 &
\echo "Data Generated for Application rate = 2Mbps"
wait
./waf --run "scratch/part2 --apprate=4Mbps" > part2b/a4.txt 2>&1 &
echo "Data Generated for Application rate = 4Mbps"
wait
./waf --run "scratch/part2 --apprate=8Mbps" > part2b/a8.txt 2>&1 &
echo "Data Generated for Application rate = 8Mbps"
wait
./waf --run "scratch/part2 --apprate=12Mbps" > part2b/a12.txt 2>&1 &
echo "Data Generated for Application rate = 12Mbps"
wait


./waf --run scratch/part3 > part3/part3.txt 2>&1 &
echo "Running Task 3..."
wait

echo "Generating Graphs"
python gg.py
echo "Done!"


