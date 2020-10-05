#!/bin/bash
### BEGIN INIT INFO
# Provides:          automate
# Required-Start:    $all
# Required-Stop:
# Default-Start:     2 3 4 5
# Default-Stop:
# Short-Description: Automate à lait
### END INIT INFO

/usr/bin/python3 /home/pi/auto_lait.py
