from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
import json
Base = declarative_base()

class Host(Base):
    __tablename__ = "Hosts_Imformations"
    id = Column(Integer, primary_key=True)
    cards_name = Column(String)
    driver =  Column(String) 
    num_cards= Column(String)
    osenv = Column(String)
    alive = Column(String)
    host_name = Column(String)
    ip = Column(String)
    mac = Column(String)
    user=Column(String)
    login=Column(String)
    desc=Column(String)
    bmc=Column(String)
    bmclo=Column(String)
    loc=Column(String)
    ttime = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
    nowtime = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
def Host_init(h):
    try:
        H = Host(cards_name=''.join(e for e in h.cards_name ),driver=h.driver,num_cards=h.num_cards,osenv=h.osenv,alive=str(h.alive),host_name=h.host_name,ip=h.ip,mac=h.mac,bmc=h.bmc)
    except:
        H = Host(cards_name=' ',num_cards=" ", driver=h.driver,osenv=h.osenv,alive=str(h.alive),host_name=h.host_name,ip=h.ip,mac=h.mac)
    return H
class connect_data():
    def __init__(self):
        self.engine = create_engine('sqlite:///idata.db')
        self.session = sessionmaker()
        self.session.configure(bind=self.engine)
        Base.metadata.create_all(self.engine)
        self.s = self.session()
    def insert_host(self, h):
        h = Host_init(h)
        host = self.s.query(Host).filter_by(mac=h.mac).all()
        if len(host)==1:
            host[0].cards_name = h.cards_name
            host[0].driver = h.driver
            host[0].num_cards=h.num_cards
            host[0].osenv=h.osenv
            if host[0].alive=="False" and h.alive=="False" and host[0].ttime < datetime.now():
                host[0].user=""
                host[0].desc=""
            host[0].alive=h.alive
            host[0].host_name=h.host_name
            host[0].ip=h.ip
            host[0].nowtime = datetime.now()
            try:
                if len(h.bmc)>8:
                    host[0].bmc=h.bmc
                else:
                    host[0].bmc="None"
            except:
                host[0].bmc="None"
                self.s.commit()
                return
        else:
            self.s.add(h)
        self.s.commit()
    def update(self,data):
        host = self.s.query(Host).filter_by(mac=data["mac"]).all()
        mac=''
        host[0].bmc = data["bmc"]
        host[0].bmclo = data["bmclo"]
        host[0].login = data["login"]
        host[0].loc = data["loc"]
        if host[0].user == data["user"] and host[0].desc == data["desc"] and self.time_to_days(host[0].ttime) == data["uday"]:
            self.s.commit()
            return mac
        mac=host[0].mac
        host[0].user = data["user"]
        host[0].desc = data["desc"]
        host[0].ttime = self.days_to_time(data["uday"])
        self.s.commit()
        return mac
    def check(self):
        hosts = self.s.query(Host).all()
        now = datetime.now()
        for host in hosts:
            if (now - host.nowtime).seconds > 3600*2:
                host.user=""
                host.desc=""
                host.osenv="Unknown"
                host.driver="Unknown"
                host.cards_name="Unknown"
                host.host_name="Unconnected"
                host.alive = "False"
                self.s.commit()
    @staticmethod
    def time_to_days(ttime):
        if ttime != None and ttime != '' and ttime > datetime.now():
            days = str((ttime - datetime.now()).total_seconds()/86400.)[0:4]
        else:
            days = "0"
        return days
    @staticmethod
    def days_to_time(days):
        if days != '':
            try:
                days = float(days)
                if days < 0:
                    days = 0
            except:
                days = 0
        else:
            days = 0
        return datetime.now() + timedelta(days=days)
    def query_data(self, macc):
        host = self.s.query(Host).filter_by(mac=macc).all()
        return host[0].user, host[0].cards_name, host[0].ip, host[0].desc
    def read_data(self):
        datas = self.s.query(Host).all()
        result = []
        for data in datas:
            days = self.time_to_days(data.ttime)
            result.append({r"cards_name":data.cards_name,"uday":days,r"num_cards":" "+data.num_cards,"login":data.login,r"host_name":data.host_name,r"driver":data.driver,r"osenv":data.osenv,r"ip":data.ip,"alive":data.alive,r"nowtime":str(data.nowtime)[5:-7],"mac":data.mac,"user":data.user,"desc":data.desc,"bmc":data.bmc,"bmclo":data.bmclo,"loc":data.loc})
        return json.dumps(result)
