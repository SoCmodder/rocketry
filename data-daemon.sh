#!/bin/sh
# launcher.sh
# navigate to home directory, then to this directory, then execute python script, then back home
# add to crontab with:
# sudo crontab -e
# @reboot sh /home/pi/scripts/data-daemon.sh >/home/pi/logs/cronlog 2>&1

cd /
cd home/pi/rocketry
echo "Sleeping for 5 then running python record_altitude.py"
sleep 5
echo "Starting Data Recording"
sudo python record_altitude.py
echo "Data Recording Finished"
cd /