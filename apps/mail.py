#!/usr/bin python
from flask import Flask, render_template
from flask_mail import Mail, Message
import os
import requests
import threading
#app = Flask(__name__)
#app.config['MAIL_SERVER'] = 'smtp.163.com'
#app.config['MAIL_PORT'] = 994
#app.config['MAIL_USE_TLS'] = True
#app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
#app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')

#app.config['MAIL_USE_SSL']=True
#app.config['FLASKY_ADMIN']='charll@nvidia.com'
#app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[Flasky]'
#app.config['FLASKY_MAIL_SENDER'] = 'Flasky Admin <flasky@example.com>'
html=''
#def get_html():
#    html = requests.get("http://0.0.0.0:8000/")
def send_email(mail, datas):
    msg = Message('test subject', sender='likai87268758@163.com',recipients=['charll@nvidia.com'])
    msg.body = "HOSTS"
    html=''
    for data in datas:
        html += "<p>%s is using %s(%s) for %s</p>"%(data[0], data[1], data[2], data[3])
    msg.html = html
    #msg.html = "<b>%s is using %s(%s) for %s</b>"%(user, host, ip, usage)
#    with app.app_context():
    mail.send(msg)
 
