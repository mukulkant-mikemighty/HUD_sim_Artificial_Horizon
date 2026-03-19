import socket
import pygame
from pygame.locals import *
#import queue
import json

class Client1(object):
    def __init__(self):
        self.HEADER=8
        self.PORT=5050
        self.SERVER="10.10.10.1"#"127.0.0.1"#"192.168.56.1"#"10.10.10.1"#"192.168.16.1"
        self.FORMAT='utf-8'#format(enumerate)
        self.DISCONNECT_MESSAGE="!DISCONNECT"
        self.ADDR=(self.SERVER,self.PORT)
        self.client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    def send(self,msg):
        self.message=msg#.encode(self.FORMAT) #.encode(FORMAT)
        self.msg_length=len(self.message)
        send_length=self.msg_length.to_bytes(self.HEADER) #.encode(FORMAT)
        #send_length+=b' '*(HEADER-len(send_length))
        self.client.send(send_length)
        self.client.send(self.message)
        #print(self.client.recv(2048).decode(self.FORMAT))

    def runClient(self):
        print("\n[Client] [Connecting]...\n")
        self.client.connect(self.ADDR)
        print("\n[Client] [Connected?]...\n")
        msg={"roll":0,"pitch":0,"yaw":0}
        while True:
            pygame.init()
            msg["roll"]=input("Enter value for roll:")#pygame.key.get_pressed()
            msg["pitch"]=input("Enter value for pitch:")
            msg["yaw"]=input("Enter value for yaw:")
            self.send(json.dumps(msg).encode(self.FORMAT))
            """
            msg=input("Enter value for roll:")
            self.send(msg)
            msg=input("Enter value for pitch:")
            self.send(msg)
            msg=input("Enter value for yaw:")
            self.send(msg)#.encode(self.FORMAT))
            """
            """if msg[K_ESCAPE]:
                self.send(self.DISCONNECT_MESSAGE)
            else:
                #FORMAT = pygame.K_0.__format__
                self.send(msg)"""

# Client1().runClient()
#send("Hello World!")
#send("Hello Everyone!!!")
#send(DISCONNECT_MESSAGE)