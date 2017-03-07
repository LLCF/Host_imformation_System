from flask import Flask, request, abort, render_template
from hostinfo import host
import pickle
from database import connect_data
import json
import sqlite3 as lite
import pandas as pd

app = Flask(__name__)

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
    #data = request.get_data()
    #print data
    #data = json.loads(data)a
    data = request.form.get('data')
    data = data.replace('(','[').replace(')',']').replace('\'','"')
    data = json.loads(data)
    cdata = connect_data()
    for d in data:
        cdata.update(d)
    
    return '<p>OK</p>' 
@app.route('/data.json')
def get_json():
    #datas = get_data()
    #print "******"+datas.to_json()+"*****"
    #return datas.to_json(date_format='iso')
    #print get_data()
    return get_data()
    #return [{"cards_name":"GeForce GTX 1080","num_cards": "1"}]


@app.route('/')
def x():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0',port=8000)
