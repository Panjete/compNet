from http import server
from random import randint
import socket
from _thread import *
import threading
import hashlib
from time import sleep
import time
from statistics import mean

arr_clients = []
n=5

def md5checksum(fname):

    md5 = hashlib.md5()
    f = open(fname, "rb")
    while chunk := f.read(4096):
        md5.update(chunk)
    return md5.hexdigest()

arr_clients=[]
for i in range(0,n):
    #created socket for client i
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    port = 12000 + 20*i #port of server it will connect to
    s.connect(('', port))
    arr_clients+=[s]

num_chunks = int(arr_clients[0].recv(100).decode('utf-8'))
h=num_chunks//n
print(num_chunks)

client_data= [ [b""]*num_chunks for i in range(0,n)]
for k in range(0,n):
    s= arr_clients[k]
    print("client connected")
    
      
    for i in range(0,h):  
        client_data[k][k*h+i] = s.recv(1049)    
    if (k==n-1):
        print("Transferring Chunks from Server to Client...")
        if (num_chunks%n>0):
            for f in range(0, num_chunks%n): #confusion h or n
                client_data[n-1][n*h+f] = s.recv(1049)
                #print(f)
    print("Client = ", k, "received initial chunks of data")


print("Clients Created")

server_ports_UDP_request = [13001+ 5*i for i in range(0,n)]
client_ports_UDP_request = [13000+ 5*i for i in range(0,n)]
client_ports_for_reply = [13004+ 5*i for i in range(0,n)]
TCP_ports = [15003+ 5*i for i in range(0,n)]
TCP_dt = [14003+ 5*i for i in range(0,n)]


TCP_servers=[]
for i in range(0,n):
    #created socket for TCP ports
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    port = TCP_ports[i] #port of server
    print ("socket binded to %s" %(port))
    s.bind(('', port))
    s.listen(5)
    TCP_servers+=[s]

TCP_connected_servers=[]
TCP_conn_c=[]
while(len(TCP_connected_servers)<n):
    for s in TCP_servers:
        c, addr= s.accept()
        TCP_connected_servers+=[s]
        TCP_conn_c+= [c]
        
print("TCP connections running")


UDP_s= []
for i in range(0,n):

    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDPClientSocket.bind(("127.0.0.1",22000+5*i))
    UDP_s += [UDPClientSocket]

TCP_dts=[]
for i in range(0,n):
    TCPClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    TCP_dts+= [TCPClientSocket]

UDP_reply_sockets=[]
for i in range(0,n):
    U = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    U.bind(("127.0.0.1",client_ports_for_reply[i]))
    UDP_reply_sockets+= [U]

sleep(4)

for i in range(0,n):
    TCP_dts[i].connect(('',14003+5*i))

def listeningForBroadcasts(i):
    global client_data

    
    while True:
        bytesAddressPair = UDP_reply_sockets[i].recvfrom(100)
        missing = int(bytesAddressPair[0])
        client_address = bytesAddressPair[1]
        b="0"
        if client_data[i][missing] != b"":
            b= "1"
        b= b.encode()

        UDP_reply_sockets[i].sendto(b, client_address)
        #print("client" , i , "sent whether it has file or not")
        
        TCP_conn_c[i].send(client_data[i][missing])
    

 
for i in range(0,n):
    start_new_thread(listeningForBroadcasts, (i,))

print("Threads waiting for request asking for missing data")

def incomplete(i):
    global client_data, num_chunks
    out = []
    for j in range(0,num_chunks):
        if client_data[i][j] == b"":
            out+=[j]
    out+= [-1]
    return out

#boos=[False for i in range(0,n)]

#for j in range(0,n):
    

#def compl(j):
    #global UDP_s, server_ports_UDP_request, TCP_dts, client_data, boos
    
       

    #sleep(1)
    #boos[j]= True
    #print(boos)

'''
for j in range(0,n):
    start_new_thread(compl, (j,))
    
        #print(server_message)

lock= True
while lock:
    ut= True
    for i in range(0,n):
        if boos[i] == False:
            ut = False
    if ut:
        lock = False
'''


for j in range(0,n):
    for i in incomplete(j):
        miss = i
        Missing = str(miss).encode('utf-8')
        
        UDP_s[j].sendto(Missing, ("127.0.0.1", server_ports_UDP_request[j]))
        #missing data request sent

        server_message = TCP_dts[j].recv(1100)
        if miss!= -1:
            client_data[j][miss] = server_message
            #print("missing data ", "client " , j, i, " received")
    print("client j =", j, "has full data")


wow =[b""]*n
for j in range(0,n):
    for i in range(0,num_chunks):
        wow[j]+= client_data[j][i]
    wow[j]= wow[j].decode()
print("MD5 hash of input file is = ", md5checksum("A2_small_file.txt"))

for i in range(0,n):
    f= open("Client%d.txt"%(i),"w+")
    f.write(wow[i])

for i in range(0,n):
    print("MD5 hash of data with client ", i, " is = ", md5checksum("Client%d.txt"%(i)))

print("Simulation Ended, exiting")