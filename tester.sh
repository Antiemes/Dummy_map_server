#!/bin/bash

while true
  do
    x=$(echo "($RANDOM / 1000)-15" | bc -l)
    y=$(echo "($RANDOM / 1000)-15" | bc -l)
    z=$(echo "($RANDOM / 1000)-15" | bc -l)
    curl -X POST -d '{"x":"'$x'","y":"'$y'","z":"'$z'"}' http://localhost:8088
  done
