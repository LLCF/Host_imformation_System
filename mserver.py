from flask import Flask, request, abort, render_template
from apps.hostinfo import host
import pickle
from apps.database import connect_data
import json
from apps.scheduler import Scheduler
from flask_script import Manager
from flask_mail import Mail, Message
from apps.mail import send_email
import os
from time import sleep 

app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.nvidia.com' #'smtp.163.com'#'smtp.nvidia.com'
app.config['MAIL_USERNAME'] = "hostsinformation.nvidia.com"


mail = Mail(app)
manager = Manager(app)
def get_data():
    cdata = connect_data()
    return cdata.read_data()

@app.route('/requests', methods=['POST'])
def requests():
    info = request.form.get('info')
    h = pickle.loads(info)
    cdata = connect_data()
    cdata.insert_host(h)
    return '<p>OK</p>'
    
@app.route('/update', methods=['POST'])
def update():
    data = request.form.get('data')
    data = data.replace('(','[').replace(')',']').replace('\'','"')
    data = json.loads(data)
    cdata = connect_data()
    c_data=[]
    for d in data:
        mac = cdata.update(d)
        if mac != '':
            user, host, ip, usage = cdata.query_data(mac)
            if user != '':
                c_data.append([user, host, ip, usage])
    if len(c_data)>0 :
        print "send emails"
        send_email(mail, c_data)
        print "send success"
    return '<p>OK</p>' 

@app.route('/data.json')
def get_json():
    return get_data()

@app.route('/')
def x():
    return render_template('index.html')
@app.route('/server')
def admin():
    return render_template('server.html')

def check_status():
    cdata = connect_data() 
    cdata.check()
if __name__ == '__main__':
    scheduler = Scheduler(3600*6, check_status)
    scheduler.start()
    app.run(debug=False,host='0.0.0.0',port=8000)
    #manager.run(host='0.0.0.0',port=8000)
    scheduler.stop()



