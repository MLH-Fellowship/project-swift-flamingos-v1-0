#!/bin/bash

systemctl stop myportfolio
cd ~/personalSite
git fetch && git reset origin/main --hard
source python3-virtualenv/bin/activate 
pip3 install -r requirements.txt
systemctl start myportfolio