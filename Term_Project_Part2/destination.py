from socket import *        # importing socket library 
from threading import *     # importing threading library    
import sys                  # importing sys library
import fcntl, os            # importing fcntl and os library
import time                 # importing time library
import struct               # importing struct library

RDTPort=5020                # port number(randomly chosen) which is port for sending UDP packets to routers
serverPort = 5011           # port number(randomly chosen) which is port for listenig TCP packets from source

bufferSize = 12             # 12 is 10+1+1 and 10 for packet size, +1 for index numbers, +1 is for checksum
brokerIP1='10.10.2.1'       # IP of broker for sending through router1
brokerIP2='10.10.4.1'       # IP of broker for sending through router2
brokerIP ='10.10.2.1'       # helper variable for our Dest_Chose() function(initialized as the IP of broker through router1) 

serverSocket = socket(AF_INET,SOCK_DGRAM)               # UDP
serverSocket.bind(('', serverPort))                     # binding socket with related port

isAcked=[0,0,0,0,0,0,0,0,0,0]                           # helper array for checking if the packets are ACKed(a 0 means not ACKed, a 1 means ACKed, a -1 means NACKed)
ACKK='A'                                                # just a variable for the letter 'A' representing ACK's
NACKK='N'                                               # just a variable for the letter 'N' representing NACK'S

print('The destination is ready to receive...')         # printing just to see that the destination is on and ready to serve

f = open("delay_end.txt", "a")                          # opening txt file for arriving time info
f.write("---------------------------------\n")          # just printing -'s and a new line to separate data

def work():                                             # the major function                              
        array=[]                                        # empty helper array initialization
        array2=["","","","","","","","","",""]          # helper array initialization for collecting incoming messages together
        while True:                                     # loop forever             
            result=""                                   # empty helper string initialization to hold the resulting message string                 
            cnt=0                                       # helper integer initialization to hold the number of characters in the message( initialize with the value 0)   
            for x in array:                             # loop for each element in array
                if len(x)>10:                           # if the length of the current element is greater than 10
                    cnt+=1                              # increase the count by one

            result=""                                   # empty helper string initialization
            if cnt==10:                                 # if the count is 10
                for x in array:                         # for each element of array        
                    if len(x)>10:                       # if the length of the element is greater than 10
                        array2[int(x[10])]=x[0:10]      # update array2's related element with the element([0:10] part is for excluding the checksum and index info)
            for i in range(0,10):                       # loop 10 times
                result+=array2[i]                       # append array2's relevant element to the resulting string 
            if len(result)==100:                        # if the length of the resulting string is 100(means we've received the whole message)
                print result                            # print the resulting string
                break                                   # and then exit from the loop

            message, clientAddress = serverSocket.recvfrom(bufferSize)          # get datagram of the size "bufferSize" from Routers

            if message not in array:                                            # if the received message is not in the array yet
                array.append(message)                                           # append that message to the array
           
            if len(message)==12:                                                # if the length of the message is 12
                checksum=''                                                     # empty string initialization for checksum info    
                checksum=message[11]                                            # get the checksum(last character of the message)

                if chr((sum(map(ord,message[0:10])))%100) == checksum:          # if checksum matches 
                                                                    
                    index=''                                                    # empty string initialization for index info
                    index=message[10]                                           # get the index(one character before the last character of the message)
                    if isAcked[int(index)]!=1:                                  # if not ACKed
                        serverSocket.sendto(ACKK+index, (brokerIP, RDTPort))    # send the ACK info + the index info to broker on brokerIP (Dest_Chose() function will decide whether through r1 or r2)            
                        isAcked[int(index)]=1                                   # mark it as ACKed on the helper isAcked array by marking it with a +1
        
                else:                                                           # if checksum doesn't match
                    index=''                                                    # empty string initialization for index info
                    index=message[10]                                           # get the index(one character before the last character of the message)
                    isAcked[int(index)]=-1                                      # mark it as NACKed on the helper isAcked array by marking it with a -1
                    serverSocket.sendto(NACKK+index, (brokerIP, RDTPort))       # send the NACK info + the index info to broker on brokerIP (Dest_Chose() function will decide whether through r1 or r2)

def Dest_Chose():                   # helper function to alter between router1 or router2
    global brokerIP                 # just to be able to change the global variable inside the function
    while True:                     # loop forever
        if brokerIP==brokerIP1:     # if router1 is selected 
            brokerIP=brokerIP2      # change it and select router2
        else:                       # if router2 is selected
            brokerIP=brokerIP1      # change it and select router1

Thread(target=Dest_Chose).start()   # threading for function Dest_Chose()
Thread(target=work).start()         # threading for function work()