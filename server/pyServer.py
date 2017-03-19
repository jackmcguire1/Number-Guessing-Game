import select 
import socket 
import sys
import random
import time
try:
    import ssl
except ImportError:
    pass
else:
 context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
 context.load_cert_chain(certfile="100249558.crt", keyfile="100249558.key")

 host = 'localhost'
 backlog = 5 
 size = 1024
 data1 = str('')
 #adminclient
 aport= 4001
 aserver= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 aserver.bind((host,aport))
 ts = ssl.wrap_socket(aserver,server_side=True, certfile="100249558.crt", keyfile="100249558.key")
 ts.listen(1)

 ainput = [ts,]
 aoutputsock = [ts,]
 #client declarations
 port = 4000 
 server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 server.bind((host,port)) 
 server.listen(backlog)
 randomnumbers = []
 initiatea = []
 playernum = []
 numofplayers = 0
 num = 1
 location = 0
 input = [server,]
 outputsocks = []
 outputsock = [server,]
 connectedclients = []

 running = 1

 def initiate(address):
    if(len(initiatea) >= 1):
      if initiatea[0] == str(address):
       del initiatea[0]
       return True
      else:
        return False
    else:
       return False

 def whichplayer(socket):
    i=0
    if(len(playernum) >= 1):
     while i <= numofplayers+1:
      if(playernum[i] == socket):
          return i
      i = i + 1
      
 while running: 
  inputready,outputready,exceptready = select.select(input + ainput,outputsock + aoutputsock,[]) 
  
  for s in inputready: 

    if s == server: 
      # handle the server socket 
      client, address = server.accept()
      input.append(client)
      #outputsocks.append(s)
      initiatea.append(str(address))
      connectedclients.append(str(address))
      randomnumbers.append(random.randrange(1,20+1))
      numofplayers = numofplayers + 1
      #print(randomnumbers)
      #print(playernum)
      
    elif s == ts:
       try:
           client, address = ts.accept()
           ainput.append(client)
           ts.setblocking(0)
           initiatea.append(str(address))
       except Exception:
               break


    elif(s in ainput):
      if(initiate(address)):
           data = s.read(80).decode('UTF-8')
           s.write("Welcome Admin, please enter a command!".encode())
          #playernum.append(s)
      data1 = s.read(size).decode('UTF-8')
      if not data1:
          ts.unwrap(s)
          ts.close()
          ainput.remove(s)
          s.close()
          
          continue
      outputsocks.append(int(data1))
      aoutputsock.append(s)
          
    else:
      if(initiate(str(address))):
           data = s.recv(80).decode('UTF-8')
           s.sendto("GREETINGS - please guess a number between 1-20".encode(),address)
           playernum.append(s)
      time.sleep(8)
      try:
       data1 = s.recv(size).decode('UTF-8')
      except Exception:
          #location = whichplayer(s)
          s.close() 
          input.remove(s)
          #del connectedclients[location]
          numofplayers = numofplayers - 1
          break
          
      if not data1:
         location = whichplayer(s)
         s.close() 
         input.remove(s)
         del connectedclients[location]
         numofplayers = numofplayers - 1
         
         continue
       #handle all other sockets
      outputsocks.append(int(data1))
      outputsock.append(s)

  for s in outputready:

      if s == server:
          #outputsock.remove(s)
         print(address)
         
      elif s in aoutputsock:
       whois = outputsocks[0]
       if(whois == 1):
        i = 1
        if(len(connectedclients) >= 1):
         while i <= len(connectedclients):
            s.write(str(connectedclients[i-1]).encode('UTF-8') + ".".encode('UTF-8'))
            i = i + 1
        else:

             s.write("No players Connected!".encode('UTF-8'))
        s.close()     
        del outputsocks[:]
        ainput.remove(s)
        aoutputsock.remove(s)
       else:
            s.write("Invalid Command!".encode('UTF-8'))
            s.close()     
            del outputsocks[:]
            ainput.remove(s)
            aoutputsock.remove(s)
            
      else:
        guessnumber = outputsocks[0]
        location = whichplayer(s)
        if not(guessnumber >= 1):
            break
        #print(playernum[numofplayers-1])
        #print(str(address))
        #print(location)
        if(guessnumber == randomnumbers[location]):
          s.send("correct".encode('UTF-8'))
          del connectedclients[location-1]
          s.close() 
          input.remove(s)
          del outputsocks[0]
          outputsock.remove(s)
          
          numofplayers = numofplayers - 1
        else:
          #s.send("Incorrect".encode())
          amountaway = abs(randomnumbers[location] - guessnumber)
          if(amountaway > 5):
            s.send("Incorrect.".encode('UTF-8'))
            s.send("Far\n".encode('UTF-8'))
          else:
            s.send("Incorrect.".encode('UTF-8'))
            s.send("close\n".encode('UTF-8'))
          s.send("\nPlease enter another number".encode())
          del outputsocks[0]
          outputsock.remove(s)
          #input.append(s)

     
 server.close()
 aserver.close()
