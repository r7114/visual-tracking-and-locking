import time
import socket
import pickle
from threading import Thread

HEADERSIZE = 10

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 50030))

def rec(s):
    msg = s.recv(HEADERSIZE)
    msglen = int(msg)

    msg = s.recv(msglen)
    return pickle.loads(msg)

def send(s,d):
    msg = pickle.dumps(d)
    msg = bytes(f"{len(msg):<{HEADERSIZE}}", 'utf-8')+msg
    s.send(msg)


class handler_class:
    def __init__(self,s):
        self.s = s
        Thread(target=self.recever).start()
        time.sleep(1)

    def recever(self):
        send(s,'Client started')
        while True:
            #print('heheh')
            self.x_pos,self.y_pos,self.ammo_no,self.loaded,self.lms = rec(self.s)

    def update_server_data(self,x=None,y=None,m=None,f=None,xs=None,ys=None):
        l=[x,y,m,f,xs,ys]
        send(self.s,[0,l])

    def server_exec(self,c):
        send(self.s,[1,c])


handler = handler_class(s)