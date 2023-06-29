import socket

class cache(object):
    
    def __init__(self,n,arr,num_array, n_clients):
        self.size = n #max_size of cache
        self.storage = arr #array storing values of cache
        self.stor_num = num_array
        self.n_clients = n_clients

    def look_for_data(self, num_of_chunk, TCP_ports, UDP_server_sockets):
        if num_of_chunk == -1: return b""
        a = self.stor_num

        for k in range(0, len(a)):
            if a[k]== num_of_chunk:
                #print(k)
                b= self.storage[k]
                self.stor_num.pop(k)
                self.storage.pop(k)
                self.stor_num = [num_of_chunk] + self.stor_num
                self.storage = [b] + self.storage
                #print("cache used!")
                return b
    
        client_ports_for_reply = [13004+ 5*i for i in range(0, self.n_clients)]
        file_received= False
        #b="transient"
        while(file_received==False): #UDP packet drop safe-keeping mechanism
            for i in range(0, self.n_clients):
                if file_received==False:
                    
                    c = UDP_server_sockets[i]
                    c.sendto(str(num_of_chunk).encode(), ("127.0.0.1", client_ports_for_reply[i]))
                    
                    bytesAddressPair = c.recvfrom(10)
                    message = int(bytesAddressPair[0])
                    
                    if (message == 1): #client has the file
                        #b = "found"
                        b = TCP_ports[i].recv(1050)
                        #print("client i" , i , "found the missing file")
                        #make TCP w client and get file
                        file_received = True
                    
        
        if (len(self.stor_num)) == self.size:
            self.stor_num.pop(-1)
            self.storage.pop(-1)      
        self.stor_num = [num_of_chunk] + self.stor_num
        self.storage = [b] + self.storage
        return b     

    def ask_for_data(self, num_of_chunk, TCP_socket,  TCP_servers, UDP_server_sockets):
        
            b = self.look_for_data(num_of_chunk, TCP_servers, UDP_server_sockets)
            TCP_socket.send(b)

            
            

