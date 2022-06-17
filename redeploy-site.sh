#!/bin/bash
tmux kill-server
cd ~/personalSite
git fetch && git reset origin/main --hard
source python3-virtualenv/bin/activate 
pip3 install -r requirements.txt
tmux new-session -d -s personalSite 'source python3-virtualenv/bin/activate && flask run --host=0.0.0.0'
