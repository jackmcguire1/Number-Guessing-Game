import	socket
import random
from decimal import *
import sys
clientnum = random.randrange(1,200+1)
read = []
location = 0
s	=	socket.socket(socket.AF_INET,	
socket.SOCK_STREAM)
s.connect(("localhost",	4000))
s.send("Hello\r\n".encode())
print(s.recv(80).decode())
#print("\n",s.recv(80).decode())
s.send(input().encode('UTF-8'))
for i in range (1,10):
     data1 = s.recv(1024).decode('UTF-8')
     read.append(data1)
     if '.' in read[location]:
       print(read[location])
       print("\n",s.recv(1024).decode('UTF-8'))
       s.send(input().encode('UTF-8'))
       location = location + 1
     else:
     #guessnumber = str(data1)
     #if(guessnumber == "correct"):
           #print(guessnumber)
           #break
      print(data1)
      break
     
s.close()
