from sqlalchemy import Column, String, Integer, ForeignKey,DateTime, update 
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from hostinfo import host
from datetime import datetime
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
    nowtime = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
#    def __repr__(self):
#        return "<Host(cards_name=%s,driver=%s,num_cards=%s,osenv=%s,alive=%s,host_name=%s,ip=%s,mac=%s)>" % self.cards_name,self.driver,self.num_cards,self.osenv,str(self.alive),self.host_name,self.ip,self.mac
def Host_init(h):
    H = Host(cards_name=''.join(e for e in h.cards_name ),driver=h.driver,num_cards=h.num_cards,osenv=h.osenv,alive=str(h.alive),host_name=h.host_name,ip=h.ip,mac=h.mac,bmc=h.ipmi)
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
            host[0].alive=h.alive
            host[0].host_name=h.host_name
            host[0].ip=h.ip
            host[0].nowtime = datetime.now()
            host[0].bmc=h.bmc
            print "update"
        else:
            print "add"
            self.s.add(h)
        self.s.commit()
    def update(self,data):
        host = self.s.query(Host).filter_by(mac=data["mac"]).all()
        host[0].user = data["user"]
        host[0].desc = data["desc"]
        host[0].bmc = data["bmc"]
        host[0].bmclo = data["bmclo"]
        host[0].login = data["login"]
        self.s.commit()
    def read_data(self):
        datas = self.s.query(Host).all()
        result = []
        for data in datas:
	    result.append({r"cards_name":data.cards_name,r"num_cards":" "+data.num_cards,"login":data.login,r"host_name":data.host_name,r"driver":data.driver,r"osenv":'Ubuntu'+data.osenv+'.04',r"ip":data.ip,"alive":data.alive,r"nowtime":str(data.nowtime)[5:-7],"mac":data.mac,"user":data.user,"desc":data.desc,"bmc":data.bmc,"bmclo":data.bmclo})
        return json.dumps(result)
    
     
if __name__ == '__main__':
    cdata = connect_data()
    h = host()
    h()
    cdata.insert_host(h)
