from distutils.command.install_egg_info import to_filename
import hashlib
from multiprocessing.forkserver import connect_to_new_process
import os
import socket
from _thread import *
from socketserver import TCPServer
import threading
from lrupart1 import cache
from time import sleep
import time

print_lock = threading.Lock()

n = 5
cache_size = 5
print("Number of clients = ", n)
print("Cache size = ", cache_size)

def md5checksum(fname):

    md5 = hashlib.md5()
    f = open(fname, "rb")
    while chunk := f.read(4096):
        md5.update(chunk)
    return md5.hexdigest()
def md5checkstring(fname):   
    return hashlib.md5(fname).hexdigest()


def distrib(num, file_name, conn_c): #for initial distribution of chunks

    with open(file_name, 'r') as file:
        data = file.read()

    byt= bytes(data, 'utf-8')
    file_size = len(byt)
    print("File Size is :", file_size, "bytes")
    num_chunks = file_size//1024
    if(file_size%1024 != 0):
        num_chunks += 1

    conn_c[0].send(str(num_chunks).encode('utf-8')) #sending number of chunks to client side
    print("Num_chunks conveyed to Client")

    chunks=[]
    for i in range(0, num_chunks-1):
        chunks += [byt[i*1024:1024*(1+i)]]
    if(file_size%1024 != 0):
        chunks+= [byt[(num_chunks-1)*1024:]]
    
    a = num_chunks//num
    print("Num_chunks = ",num_chunks, "  ", "Num_chunks per client = ",a)
    
    for j in range(0, num):
        start_new_thread(serv, (conn_c, j, a, num ,num_chunks, chunks,))

    return 0

def serv(conn_c, j, a, num, num_chunks, chunks):
    
    for i in range(0,a):
        conn_c[j].send(chunks[j*a+i])
    if (j==num-1):
        
        for f in range(num*a, num_chunks):
            conn_c[j].send(chunks[f])


servers=[]
for i in range(0,n):
    #created socket for server's ith port
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    port = 12000 + 20*i #port of server
    print ("Binded socket to %s" %(port))
    s.bind(('', port))
    s.listen(5)
    servers+=[s]

print("Server's TCP Side Up and Running") 
    

connected_servers=[]
conn_c=[]
while(len(connected_servers)<n):
    for s in servers:
        c, addr= s.accept()
        connected_servers+=[s]
        conn_c+= [c]

print("TCP connections established")

distrib(n, "A2_small_file.txt", conn_c)
print("init data transferred")

server_ports_UDP_request = [13001+ 5*i for i in range(0,n)]
server_to_clients_broadcast_UDP_ports = [13002+ 5*i for i in range(0,n)]
TCP_ports = [15003+ 5*i for i in range(0,n)]
TCP_dt = [14003+ 5*i for i in range(0,n)]



UDP_server_sockets=[]
for i in range(0,n):
    UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDPServerSocket.bind(("127.0.0.1", server_ports_UDP_request[i]))
    UDP_server_sockets+= [UDPServerSocket]

TCP_dts=[]
for i in range(0,n):
    TCPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    TCPServerSocket.bind(('', 14003+ 5*i))
    TCPServerSocket.listen(1)
    TCP_dts+= [TCPServerSocket]

cache = cache(cache_size,[],[], n)

sleep(4)
arr_TCP_clients=[]
for i in range(0,n):
    #created socket for client i
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    port = TCP_ports[i] #port of server it will connect to
    s.connect(('', port))
    arr_TCP_clients+=[s]

for i in range(0,n):  
    bool= True
    boo = True 
    while boo:
        if bool:
            c, addr= TCP_dts[i].accept()
        bytesAddressPair = UDP_server_sockets[i].recvfrom(100)
        missing = int(bytesAddressPair[0])
        if missing == -1:
            boo= False
            #print("client i = ", i, " now has full data")
        client_address = bytesAddressPair[1]
        #print("missing request received")

    
        #print("TCP server up and running")
        cache.ask_for_data(missing,c, arr_TCP_clients, UDP_server_sockets)
        #print("missing data sent")
        bool = False
        #TCPServerSocket.close()


#print(cache.stor_num)
#print(cache.storage)
