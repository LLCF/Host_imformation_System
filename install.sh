#!/bin/bash
giti=$(dpkg -l | grep -E " git ")
if [[ "$giti" == "" ]]
then
    sudo apt-get install git -y
fi

git clone https://github.com/LLCF/Host_imformation_System
cd Host_imformation_System
sudo echo  "1 */1    * * *   root    python /etc/init.d/hostinfo.py" >> /etc/crontab
sudo cp hostinfo.py /etc/init.d/
result=$(cat /etc/issue | grep "16")
if [[ "$result" != "" ]]
then
    sudo systemctl restart cron
else
    sudo system service cron restart
fi
cd ..
rm -rf Host_imformation_System
