#!/bin/bash
sudo apt update -y && apt upgrade
sudo apt install git -y
git clone https://github.com/MayElbaz18/MoniTHOR--Project.git
cd MoniTHOR--Project
sudo apt install python3-pip
pip3 install -r requirements.txt --break-system-packages --ignore-installed
sudo chmod -R 777 .
sudo bash -c 'cat << EOF > /etc/systemd/system/MoniTHOR.service [Unit] Description=MoniTHOR instance, Flask application for domains monitoring After=network.target [Service] User=ubuntu Group=ubuntu WorkingDirectory=/home/ubuntu/MoniTHOR--Project Environment="/home/ubuntu/MoniTHOR--Project/.env" ExecStart=/usr/bin/python3 /home/ubuntu/MoniTHOR--Project/app.py [Install] WantedBy=multi-user.target EOF'
sudo systemctl daemon-reload
sudo systemctl start MoniTHOR.service
sudo systemctl enable MoniTHOR.service
sudo systemctl stop ufw 
sudo python3 app.py
