from distutils.command.install_egg_info import to_filename
import hashlib
from multiprocessing.forkserver import connect_to_new_process
import os
import socket
from _thread import *
from socketserver import TCPServer
import threading
from lrupart2 import cache
from time import sleep
import time

print_lock = threading.Lock()

n = 5
cache_size = 5

print("Number of Clients = ", n)
print("cache size = ", cache_size)


def md5checksum(fname):

    md5 = hashlib.md5()
    f = open(fname, "rb")
    while chunk := f.read(4096):
        md5.update(chunk)
    return md5.hexdigest()
def md5checkstring(fname):   
    return hashlib.md5(fname).hexdigest()


def distrib(num, file_name, conn_c):

    with open(file_name, 'r') as file:
        data = file.read()

    byt= bytes(data, 'utf-8')
    file_size = len(byt)
    print("File Size is :", file_size, "bytes")
    num_chunks = file_size//1024
    if(file_size%1024 != 0):
        num_chunks += 1

    conn_c[0].send(str(num_chunks).encode('utf-8')) 
    print("Num_chunks = ", num_chunks, " conveyed to the clients")

    chunks=[]
    for i in range(0, num_chunks-1):
        chunks += [byt[i*1024:1024*(1+i)]]
    if(file_size%1024 != 0):
        chunks+= [byt[(num_chunks-1)*1024:]]
    
    a = num_chunks//num
    for j in range(0, num):
        start_new_thread(serv, (conn_c, j, a, num ,num_chunks, chunks,))

    return 0

def serv(conn_c, j, a, num, num_chunks, chunks):
    
    for i in range(0,a):
        conn_c[j].send(chunks[j*a+i])
    if (j==num-1):
        
        for f in range(num*a, num_chunks):
            print("sent misc")
            conn_c[j].send(chunks[f])


'''
n TCPS for broadcasting and relay back
whatever client wants file, makes a TCP with corresponding server
corresponding server checks whether it has file
else sequentially communicate w clients through TCP
if found, UDP data tranfer through corresponsding ports
'''

servers=[]
for i in range(0,n):
    #created socket for server's ith port
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    port = 12000 + 20*i #port of server
    print ("Server side of TCP socket binded to %s" %(port))
    s.bind(('', port))
    s.listen(5)
    servers+=[s]

print("Server Side of Ports Up and Running") 
    

connected_servers=[]
conn_c=[]
while(len(connected_servers)<n):
    for s in servers:
        c, addr= s.accept()
        connected_servers+=[s]
        conn_c+= [c]
        
        
print("TCP connected from Servers' end")

distrib(n, "A2_small_file.txt", conn_c)
print("init data transferred")

server_UDP_ports = [13001+ 5*i for i in range(0,n)] 
clients_UDP_ports = [13002+ 5*i for i in range(0,n)]
TCP_ports = [15003+ 5*i for i in range(0,n)] #for missing request, arr_TCP
TCP_dt = [14003+ 5*i for i in range(0,n)] #for confirming whether we have data or not, broadcast and acknowledging



UDP_server_sockets=[]
for i in range(0,n):
    UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDPServerSocket.bind(("127.0.0.1", server_UDP_ports[i]))
    UDP_server_sockets+= [UDPServerSocket]

TCP_dts=[]
for i in range(0,n):
    TCPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    TCPServerSocket.bind(('', 14003+ 5*i))
    TCPServerSocket.listen(1)
    TCP_dts+= [TCPServerSocket]
#TCP_dts socket side listening

cache = cache(cache_size,[],[], n) #creating cache object

sleep(4)

arr_TCP=[]#
for i in range(0,n):
    #created socket for client i
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    port = TCP_ports[i] # TCP_ports ka client connection
    s.connect(('', port))
    arr_TCP+=[s]

print("TCP_ports connected")

TCP_dts_servers=[]
TCP_dts_conn_c=[]
while(len(TCP_dts_servers)<n):
    for s in TCP_dts:
        c, addr= s.accept()
        TCP_dts_servers+=[s]
        TCP_dts_conn_c+= [c]

print("TCP_dts connected")

for i in range(0,n):  

    boo = True 
    while boo:
        bytesAddressPair = arr_TCP[i].recv(100)
        missing = str(bytesAddressPair.decode())
        missing = int(missing.split("#")[0])
        #missing request received for packet = "
        if missing == -1:
            boo= False
            print("Client i = ", i, " now has full data")
        cache.ask_for_data(missing, i, TCP_dts_conn_c, UDP_server_sockets)
        


