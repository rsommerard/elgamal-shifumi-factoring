#!/bin/bash

exec 2>/dev/null

python3 main.py true
sleep 3

while true
do
  python3 main.py
  sleep 3
done
