#!/bin/bash
giti=$(dpkg -l | grep -E " git ")
if [[ "$giti" == "" ]]
then
    sudo apt-get install git -y
fi
giti=$(dpkg -l | grep -E "python-pip")
if [[ "$giti" == "" ]]
then
    sudo apt-get install python-pip -y
fi
giti=$(dpkg -l | grep -E "ipmitool")
if [[ "$giti" == "" ]]
then
    sudo apt-get install ipmitool -y
    sudo modprobe ipmi_msghandler
    sudo modprobe ipmi_devintf
    sudo modprobe ipmi_si
fi

sudo pip install requests

git clone https://github.com/LLCF/Host_imformation_System
cd Host_imformation_System
#sudo cp -f crontab /etc/crontab
cront=$(cat /etc/crontab | grep "hostinfo.py")
if [[ "$cront" == "" ]]
then
    sudo echo  "*/1 */1    * * *   root    python /etc/init.d/hostinfo.py" >> /etc/crontab
else
    sed '$d' /etc/crontab | sudo  tee /etc/crontab
    sudo echo  "1 */3    * * *   root    python /etc/init.d/hostinfo.py" >> /etc/crontab
fi
sudo cp hostinfo.py client.cfg  /etc/init.d/
result=$(cat /etc/issue | grep "16")
if [[ "$result" != "" ]]
then
    sudo systemctl restart cron.service
else
    sudo service cron restart
fi
cd ..
rm -rf Host_imformation_System
sudo /etc/init.d/hostinfo.py
echo "install success"
