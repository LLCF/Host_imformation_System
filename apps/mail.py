#!/usr/bin python
from flask_mail import Mail, Message
import os
html=''
def send_email(mail, datas):
    msg = Message('Hosts Informations', sender='host@nvidia.com',recipients=['dl-qa-farm-user@exchange.nvidia.com'])
    msg.body = "HOSTS"
    html=''
    for data in datas:
        html += "<p>%s is using %s(%s) for %s</p>"%(data[0], data[1], data[2], data[3])
    msg.html = html + "<p>To see more detail in this <a href=http://10.19.192.46>page</a></p>"
    mail.send(msg)
 
