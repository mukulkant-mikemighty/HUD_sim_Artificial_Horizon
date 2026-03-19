import socket
import threading
#import queue
import time
import pygame
from pygame.locals import *
import json

class Serv1(object):
    def __init__(self):
        self.HEADER=8
        self.PORT=5050
        #print("HIIIIII")
        self.SERVER="192.168.56.1"#"#socket.gethostbyname(socket.gethostname())#"10.10.10.1"#"127.0.0.1"#"192.168.56.1"#"10.10.10.1" #"192.168.16.1"##socket.gethostbyname(socket.gethostname())
        self.ADDR=(self.SERVER,self.PORT)
        self.FORMAT='utf-8'#format(enumerate)
        self.DISCONNECT_MESSAGE="!DISCONNECT"
        self.msg1={"roll":0,"pitch":0,"yaw":0}#pygame.key.ScancodeWrapper#queue.Queue()
        self.server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        

    
    def handle_client(self,conn,addr):
        print(f"\n[SERVER] [NEW CONNECTION] {addr} connected.")
        connected = True
        while connected:
            msg_length=conn.recv(self.HEADER)#.decode(self.FORMAT)
            if msg_length:
                msg_length=int.from_bytes(msg_length)
                self.msg1=json.loads(conn.recv(msg_length).decode(self.FORMAT))
                """self.msg1["roll"]=conn.recv(msg_length).decode(self.FORMAT)
                self.msg1["pitch"]=conn.recv(msg_length)#.decode(self.FORMAT)
                self.msg1["yaw"]=conn.recv(msg_length)#.decode(self.FORMAT)"""
                if self.msg1==self.DISCONNECT_MESSAGE:
                    connected=False
                #print(f"[{addr}] {self.msg1}")
                conn.send("\n[SERVER] Msg received.".encode(self.FORMAT))
        conn.close()

    
    def startServ(self):
        print("\n[SERVER] Binding server now...\n")
        self.server.bind(self.ADDR)
        print(f"[SERVER] [LISTENING] Server is listening on {self.SERVER}")
        self.server.listen()
        #time.sleep(30)
        print("[SERVER] listening over")
        while True:
            print("[SERVER] [ACCEPTING]...")
            conn,addr=self.server.accept()
            print("[SERVER] [ACCEPTED]")
            thread=threading.Thread(target=self.handle_client,args=(conn,addr))
            thread.start()
            print(f"\n[SERVER] [ACTIVE CONNECTIONS] {threading.active_count()-1}")

    
# print("[STARTING] Server is starting...")
# Serv1().startServ()