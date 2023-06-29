import socket

class cache(object):
    
    def __init__(self,n,arr,num_array, n_clients):
        self.size = n #max_size of cache
        self.storage = arr #array storing values of cache
        self.stor_num = num_array
        self.n_clients = n_clients

    def look_for_data(self, num_of_chunk, i, TCP_servers, UDP_server_sockets):
        if num_of_chunk == -1: return b""
        a = self.stor_num
        for k in range(0, len(a)):
            if a[k]== num_of_chunk:
                b= self.storage[k]
                self.stor_num.pop(k)
                self.storage.pop(k)
                self.stor_num = [num_of_chunk] + self.stor_num
                self.storage = [b] + self.storage
                return b

        n = self.n_clients
        file_received= False
        while(file_received==False): #UDP packet drop safe-keeping mechanism
            for d in range(0, self.n_clients):
                if file_received==False:
                    
                    TCP_servers[d].send((str(num_of_chunk) + "#" + str(i)).encode())
                    #server sent request for chunk it does not have
                    bytesAddressPair = TCP_servers[d].recv(100)
                    #print("client d = ", d, " responds whether it has missing chunk or not")
                    message = int(bytesAddressPair.decode())
                    
                    if (message == 1): #client has the file
                        f=True
                        while f:
                            b = UDP_server_sockets[i].recvfrom(1200)
                            b = b[0]
                            if b!=b"":
                                #client i has received correct
                                f=False
                                TCP_servers[d].send("OK".encode()) #send acknowdgement
                            else:
                                TCP_servers[d].send("NO".encode())
                        #print("client i" , i , "found the missing file")
                        file_received = True
                    
        
        if (len(self.stor_num)) == self.size:
            self.stor_num.pop(-1)
            self.storage.pop(-1)      
        self.stor_num = [num_of_chunk] + self.stor_num
        self.storage = [b] + self.storage
        return b       

    def ask_for_data(self, num_of_chunk, i,  TCP_servers, UDP_server_sockets):
        n = self.n_clients
        clients_UDP_ports = [13002+ 5*i for i in range(0,n)]

        b = self.look_for_data(num_of_chunk, i, TCP_servers, UDP_server_sockets)
        UDP_server_sockets[i].sendto(b, ("127.0.0.1", clients_UDP_ports[i]))
            

