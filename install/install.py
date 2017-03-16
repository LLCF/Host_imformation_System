import os
import threading
from sys import argv
hosts = [17,159,218,187,53,210,163,80,86,186,221,165,135,170,180,191,211,219,113,73,96]
def install(ip):
    username=r"swqa"
    host=r"10.19.192."
    password=r'labuser'

    if ip == 191:
        username=r"ryluo"
    if ip == 211:
        username=r"neo"
        password=r'neo'
    hostname = host+str(ip)
    os.popen(' ssh-keygen -f "/home/charl/.ssh/known_hosts" -R '+hostname)
    os.popen(r"/usr/bin/expect install.exp "+hostname + r" " + username+r" "+password)
    print("****************"+ hostname +"************")

if __name__ == '__main__':
    try:
        _, host = argv
    except:
        host=''
    if len(host)>0:
        hosts = [host]
    threads=[]
    for i in range(len(hosts)):
        threads.append(threading.Thread(target=install,args=(hosts[i],)))
    for i in range(len(hosts)):
        threads[i].start()
    for i in range(len(hosts)):
        threads[i].join()
    print "All Done.."
