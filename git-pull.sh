#!/bin/bash
# on the raspi, drop any local changes and pull latest from github
# called on reboot in /etc/rc.local to ensure easy pull mechanism on update

echo "Git pulling latest score code $(date)";

(cd /opt/hackathon-table-tennis-score-pi || exit; \
  git fetch origin; \
  git reset --hard origin/master; \
  git pull)
