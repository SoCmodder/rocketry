#!/bin/sh
# launcher.sh
# navigate to home directory, then to this directory, then execute python script, then back home
# add to crontab with:
# sudo crontab -e
# @reboot sh /home/pi/bbt/launcher.sh >/home/pi/logs/cronlog 2>&1

cd /
cd home/pi/scripts
echo "Sleeping for 20 then running python record.py"
sleep 20
echo "Starting Camera Recording"
sudo python record_video.py
echo "Recording Finished"
cd /