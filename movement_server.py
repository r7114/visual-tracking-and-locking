import time
import socket
from threading import Thread
import pickle
import movement


HEADERSIZE = 10

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('127.0.0.1', 50030))
s.listen(1)
clientsocket, address = s.accept()
print(f"Connection from {address} has been established.")



def rec(s):
    msg = s.recv(HEADERSIZE)
    msglen = int(msg)

    msg = s.recv(msglen)
    return pickle.loads(msg)
        
def send(s,d):
    msg = pickle.dumps(d)
    msg = bytes(f"{len(msg):<{HEADERSIZE}}", 'utf-8')+msg
    s.send(msg)
    
    
def recever():
    last_firing = False
    while True:
        data = rec(clientsocket)
        #print(data)
        if data[0] == 0:
            l = data[1]
            #print(l)
            if l[0] != None:
                movement.tar_x = l[0]
            if l[1] != None:
                movement.tar_y = l[1]
        
        
        elif data[0] == 1:
            c = data[1]
            try:
                exec(c)
            except Exception as e:
                print(e)
                
                
def sender():
    c = 0
    ok2send = False
    while True:
        if ok2send:
            x_pos = movement.now_x
            y_pos = movement.now_y


            send(clientsocket,(x_pos,y_pos,0,False,0))
            #print((x_pos,y_pos,ammo_no,loaded,lms))

            time.sleep(0.02)
        else:
            if rec(clientsocket) == 'Client started':
                ok2send = True
                Thread(target=recever).start()
                print('stuff started')

                
                
                
                
                
Thread(target=sender).start()


while True:
    time.sleep(10)
