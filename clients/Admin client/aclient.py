import	socket
import random
import pprint
from decimal import *
import sys
try:
    import ssl
except ImportError:
    pass
else:


 read = []
 players = []
 location = 0
 s = socket.socket(socket.AF_INET,	socket.SOCK_STREAM)
 ssl_sock = ssl.wrap_socket(s,
                           ca_certs="5cc515_root_ca.crt")
 ssl_sock.connect(("localhost",	4001))
 #cert = conn.getpeercert()
 #ssl.match_hostname(cert, "100249558")
 ssl_sock.write("Hello\r\n".encode())
 print(ssl_sock.read(80).decode())
 #print("\n",s.recv(80).decode())
 ssl_sock.write(input().encode('UTF-8'))
 for i in range (1,200):
     data1 = ssl_sock.read(1024).decode('UTF-8')
     read.append(data1)
     if '.' in data1:
          players.append(str(read[0]))
          del read[0]
          print(data1)
          
     elif '!' in data1:
          players.append(read[0])
          print(data1)
          ssl_sock.close()
          break
     else:
      #print(data1)
      #print(players)
      break
 ssl_sock.close()
