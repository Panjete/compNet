from http import server
from random import randint
import socket
from _thread import *
import threading
import hashlib
from time import sleep
import time
from statistics import mean


n=5
print("Number of Clients = ", n)

def md5checksum(fname):

    md5 = hashlib.md5()
    f = open(fname, "rb")
    while chunk := f.read(4096):
        md5.update(chunk)
    return md5.hexdigest()
def md5checkstring(fname):   
    return hashlib.md5(fname).hexdigest()



arr_clients=[]
for i in range(0,n):
    #created socket for client i
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    port = 12000 + 20*i #port of server it will connect to
    s.connect(('', port))
    arr_clients+=[s]
    
    

num_chunks = int(arr_clients[0].recv(100).decode('utf-8')) #num_chunks received from server side
h=num_chunks//n


client_data= [ [b""]*num_chunks for i in range(0,n)]
for k in range(0,n):
    s= arr_clients[k]
    for i in range(0,h):  
        client_data[k][k*h+i] = s.recv(1049)    
    if (k==n-1):
        print("Clients receiving initial chunks from server...")
        if (num_chunks%n>0):
            for f in range(0, num_chunks%n): #confusion h or n
                client_data[n-1][n*h+f] = s.recv(1049)
    


print("Clients with seed Chunks Created")

server_UDP_ports = [13001+ 5*i for i in range(0,n)]
clients_UDP_ports = [13002+ 5*i for i in range(0,n)]
TCP_ports = [15003+ 5*i for i in range(0,n)] #for missing request, TCP_conn_c
TCP_dt = [14003+ 5*i for i in range(0,n)] #for confirming whether we have data or not, broadcast, TCP_dts


TCP_servers=[]
for i in range(0,n):
    #created socket for TCP ports
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    port = TCP_ports[i] #port of server
    print ("Client side of TCP binded to %s" %(port))
    s.bind(('', port))
    s.listen(5)
    TCP_servers+=[s]

print("Client side TCP_ports Up")    


UDP_client_sockets=[]
for i in range(0,n):
    U = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    U.bind(("127.0.0.1",clients_UDP_ports[i]))
    UDP_client_sockets+= [U]

sleep(4)

TCP_connected_servers=[]
TCP_conn_c=[]
while(len(TCP_connected_servers)<n):
    for s in TCP_servers:
        c, addr= s.accept()
        TCP_connected_servers+=[s]
        TCP_conn_c+= [c]
        
print("TCP_s servers connected and running")

TCP_dts=[]
for i in range(0,n):
    TCPClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    TCP_dts+= [TCPClientSocket]
    TCPClientSocket.connect(('',TCP_dt[i]))
print("TCP_dts connected and runnning")




def listeningForBroadcasts(i):
    global client_data, TCP_dts, TCP_conn_c, UDP_client_sockets, server_UDP_ports

    while True:
        bytesAddressPair = TCP_dts[i].recv(100)
        miss = str(bytesAddressPair.decode())
        if miss != "":
            ghj= miss.split("#")
            missing = int(ghj[0])
            missing_request_from= int(ghj[1])
            b="0"
            if client_data[i][missing] != b"": #client i has that chunk
                b= "1"
            TCP_dts[i].send(b.encode())
            #client i sends whether it has file or not

            if b== "1":
                ff= True
                while ff: #keep sending data via UDP until acknowledgeent received
                    UDP_client_sockets[i].sendto(client_data[i][missing], ("127.0.0.1", server_UDP_ports[missing_request_from]) )
                    gg= TCP_dts[i].recv(100)
                    if gg.decode() == "OK":
                        ff= False

 
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

for j in range(0,n):
    for i in incomplete(j):
        miss = i
        Missing = (str(miss)+ "#" + str(j)).encode('utf-8')
        
        TCP_conn_c[j].send(Missing)
        #missing data request sent

        server_message =  UDP_client_sockets[j].recvfrom(1200)
        #Requested chunk received from server
        
        if miss!= -1:
            if server_message[0]==b"":
                print("client i = ", j , "has received empty packet = ", i)
                #packet drop, won't execute ever though
            client_data[j][miss] = server_message[0]
        
        #print("missing data ", "client " , j, i, " received")
    print("client j =", j, "has full data")

#def compl(j):
    #global UDP_s, server_ports_UDP_request, TCP_dts, client_data, boos
    

    '''sleep(2)
    boos[j]= True
    print(boos)'''

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

print("Simulation for Part 2 ended, exiting")


