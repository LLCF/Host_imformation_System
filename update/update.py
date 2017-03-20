import os
import threading
from sys import argv
hosts = [94,126,96,93,17,135,165,140,168,159,186,177,187,191,210]
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
    os.popen(r"/usr/bin/expect update.exp "+hostname + r" " + username+r" "+password)
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
