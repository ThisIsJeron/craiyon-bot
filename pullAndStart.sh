#!/bin/bash

git pull
source env/bin/activate
nohup python3 bot.py &
