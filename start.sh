#!/bin/bash

mkdir -p /downloads

aria2c --conf-path=aria2.conf &

python bot.py
