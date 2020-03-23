from threading import *     # importing threading library             
from socket import *        # importing socket library
import fcntl, os            # importing fcntl and os library
import time                 # importing time library  
import struct               # importing struct library
import sys                  # importing sys library
import logging              # importing logging library    

serverPort = 5010           # port number(randomly chosen) which is port for listenig TCP packets from source
destPort   = 5011           # port number(randomly chosen) which is port for sending UDP packets to routers
bufferSize = 100            # 100 since source will send info of size 100

serverSocket = socket(AF_INET, SOCK_STREAM)             # TCP
serverSocket.bind(('', serverPort))                     # binding socket with port
serverSocket.listen(1)                                  # TCP server is listening...

print('The server is ready to receive...')              # just printing to check that broker is on and ready

dest1IP = "10.10.3.2"          # IP of router1 for sending
dest2IP = "10.10.5.2"          # IP of router2 for sending

destIP = "10.10.3.2"           # helper variable for our Dest_Chose() function(initialized as the IP of router1) 

isSent  = [0,0,0,0,0,0,0,0,0,0]        # helper array for checking whether the packets are sent or not(a 0 means not sent, a 1 means sent)
isAcked = [0,0,0,0,0,0,0,0,0,0]        # helper array for checking if the packets are ACKed(a 0 means not ACKed or NACKed yet, a 1 means ACKed, a -1 means NACKed)
TimeOut = [0,0,0,0,0,0,0,0,0,0]        # helper array for checking whether the packets are timed-out or not(a 1 means timed-out, a 0 means not timed-out)

Delay = [[0.0,0.0],[0.0,0.0],[0.0,0.0],[0.0,0.0],[0.0,0.0],[0.0,0.0],[0.0,0.0],[0.0,0.0],[0.0,0.0],[0.0,0.0]]   # helper array for holding start and end time information for packets
                                                                                                                # each element of array is again an array with two floating point numbers
                                                                                                                # first for the start time and the second for the arrival time

RDTRetransmission = ['','','','','','','','','','']         # helper array for holding the messages which must be RE-sent 

alpha = 0.125       # constant alpha value for estimated-rtt calculations
beta = 0.25         # constant beta value for dev-rtt calculations
SampleRTT = 1       # sample-rtt variable(initialized randomly as 1 ms)

maxInt=sys.maxint                                           # just a variable for holding the maximum integer value(representing infinity)   
EstimatedRTT=maxInt                                         # starting estimated-rtt as infinity
DevRTT=maxInt                                               # starting dev-rtt as infinity
TimeoutInterval=maxInt                                      # starting time-out interval as infinity
DevRTT=(1-beta)*DevRTT+beta*abs(SampleRTT - EstimatedRTT)   # dev-rtt formula

logging.basicConfig(filename='myapp.log', level=logging.INFO)   # just logging to log file
logging.info("EXPERIMENT START HERE")                           # some writing to the beginning of the log file

def senderTh():                                                                     # the major function for sending the messages
    while True:                                                                     # loop forever
        connectionSocket, addr = serverSocket.accept()                              # accepting socket for TCP
        message = connectionSocket.recv(bufferSize)                                 # get message of the size "bufferSize" 

        connectionSocket.send(message)                                              # send the message back (echo)

        array=[]                                                                    # empty array initialization for breaking up the incoming messages
        j=0                                                                         # loop constant
        boundary_of_string=len(message)                                             # variable for the length of the message(will also be used in the loop)
        for j in range(0, boundary_of_string, 10):                                  # break the message up 10 by 10 according to the size
            array.append(message[j:j+10])                                           # append all the broken parts to the helper array one by one

        i=0                                                                         # loop constant
        checksum=0                                                                  # initializing checksum variable
        while i<len(array) and isAcked[i]!=1:                                       # until the array is over(for each not yet ACKed packets)
            sending_packet=""                                                       # empty helper string initialization for the message to be sent
            sending_packet+=array[i]                                                # append the message to be sent to the helper string
            sending_packet+=str(i)                                                  # add helper index at the end of the string
            sending_packet+=chr((sum(map(ord,array[i])))%100)                       # summing all ascii equals of characters then adding its modulo 100 result at the end of packet as a CHECKSUM character

            clientUDPSocket = socket(AF_INET,SOCK_DGRAM)                            # UDP
            clientUDPSocket.sendto(sending_packet, (destIP, destPort))              # send the prepared message to destIP(Dest_Chose() function will decide whether through r1 or r2)
            print('SENDING PACKET ' + sending_packet + ' via' + destIP)             # print the sending packet and also on whcih router it will pass(just to check)
            isSent[i]=1                                                             # mark that packet as sent on the helper isSent array by making the relevant element's value as 1    
            RDTRetransmission[i]=sending_packet                                     # update the relevant element on the helper retransmission array 
            Delay[i][0]=(time.time() * 1000)                                        # start time for sending packet

            logging.info("start of SeqNumber : "+str(i)+" is "+str(int(round(Delay[i][0])))+"\n")  # write the sequence number and the start time to the log file

            if len(sending_packet) == 12:                                           # just to make sure that the message size is 12(10 for message, +1 for helper index, +1 for checksum) 
                print "Message sent from broker to destination:", sending_packet    # print the message sent(just to check)

            i+=1                                                                    # for iteration to continue
        connectionSocket.close()                                                    # close connection (at every turn) at the end

def RDT_Receiver_Sender():                                              # the major function for getting the acknowledgements
    global SampleRTT                                                    # just to be able to change the global variable inside the function
    global DevRTT                                                       # just to be able to change the global variable inside the function
    global EstimatedRTT                                                 # just to be able to change the global variable inside the function

    RDTListenPort=5020                                                  # port number(randomly chosen) which is port for listening for acknowledgements
    RDTSocket = socket(AF_INET,SOCK_DGRAM)                              # UDP
    RDTSocket.bind(('', RDTListenPort))                                 # binding relevant socket        
    while True:                                                         # loop forever
            RDTMessage, clientAddress = RDTSocket.recvfrom(2)           # get rdt message(acknowledgement + sequence number)
            SeqNumber=(int)(RDTMessage[1])                              # get the sequence number from the rdt message
            print(RDTMessage)                                           # ack or nack received is printed here just to see

            if RDTMessage[0]=='A':                                      # if acknowledgement is ACK
                    isAcked[SeqNumber]=1                                # mark it as ACKed by making the relevant element 1 in the helper isAcked array
                    Delay[SeqNumber][1]=(time.time() * 1000)            # update arrival time info of the relevant packet in the helper Delay array(later will be used for calculating RTT)
                    logging.info("end of SeqNumber : "+str(SeqNumber)+" is "+str(int(round(Delay[SeqNumber][1])))+"\n")   # write the sequence number and the end time to the log file
                    TMPEstimatedRTT=maxInt                              # temporary variable for RTT(initialized as infinity)
                    for i in range(1,10):                               # loop ten times                              
                        tmp=0.0                                         # temporary float variable initialized as 0.0
                        tmp=Delay[i][1]-Delay[i][0]                     # make the temporary float variable as the difference between end(arrival) and start(sent) times
                        tmp=round(tmp)                                  # round the temporary float variable
                        tmp=int(tmp)                                    # convert it to integer to be able to compare with other helper variables
                        if tmp<maxInt and tmp<TMPEstimatedRTT:          # if tmp variable is less than both infinity and temporary estimated RTT
                            TMPEstimatedRTT=tmp                         # update temporary estimated RTT with the value of the temporary float variable
                    EstimatedRTT=TMPEstimatedRTT                        # update global variable EstimatedRTT with the value of temporary estimated RTT

            elif RDTMessage[0]=='N':                                    # if acknowledgement is NACK
                    isAcked[SeqNumber]=-1                               # mark it as NACKed by making the relevant element -1 in the helper isAcked array
                    TMPEstimatedRTT=maxInt                              # temporary variable for RTT(initialized as infinity)
                    for i in range(1,10):                               # loop ten times
                        tmp=0.0                                         # temporary float variable initialized as 0.0
                        tmp=Delay[i][1]-Delay[i][0]                     # make the temporary float variable as the difference between end(arrival) and start(sent) times
                        tmp=round(tmp)                                  # round the temporary float variable
                        tmp=int(tmp)                                    # convert it to integer to be able to compare with other helper variables
                        if tmp<maxInt and tmp<TMPEstimatedRTT:          # if tmp variable is less than both infinity and temporary estimated RTT
                            TMPEstimatedRTT=tmp                         # update temporary estimated RTT with the value of the temporary float variable
                    EstimatedRTT=TMPEstimatedRTT                        # update global variable EstimatedRTT with the value of temporary estimated RTT

            EstimatedRTT=(1-alpha)*EstimatedRTT+alpha*SampleRTT         # estimated RTT formula
            DevRTT=(1-beta)*DevRTT+beta*abs(SampleRTT - EstimatedRTT)   # dev RTT formula
            TimeoutInterval=EstimatedRTT+4*DevRTT                       # time-out interval formula(in terms of estimated RTT and dev RTT)
            TimeoutInterval/=(10**18)                                   # since the values of time variables contain "10**18" multipliers in them, in order not to see "e+18"s time-out interval is divided by 10**18
            SampleRTT=EstimatedRTT                                      # update global variable sample RTT with the value of estimated RTT
            print(str(TimeoutInterval))                                 # just printing the time-out interval as a string
            for i in range(1,10):                                       # loop ten times

                if isSent[i]==1 and isAcked[i]==0 and int(round(time.time() * 1000)-round(Delay[i][0]))>TimeoutInterval:     # if packet is sent and not acknowledgemented yet and also time passed is more than the time-out interval
                        TimeOut[i]=1                                                                                         # mark that relevant packet as timed-out by making the relevant element 1 in the helper TimeOut array

                if (TimeOut[i]==1 and isAcked[i]==0) or (TimeOut[i]==1 and isAcked[i]==-1):    # if packet is timed-out and not ACKed yet(can be NACKed or not acknowledgemented at all)
                        print('resending because of timeout with index number : '+ str(i))     # print resending text with index information of the relevant packet
                        clientUDPSocket = socket(AF_INET,SOCK_DGRAM)                           # UDP
                        clientUDPSocket.sendto(RDTRetransmission[i], (destIP, destPort))       # resend the prepared message from helper retransmissin array on destIP(Dest_Chose() function will decide whether through r1 or r2)

                elif isSent[i]==1 and isAcked[i]==-1:                                          # if packet is sent but NACKed 
                        print('resending because of NACK with index number : '+str(i))         # print resending text with index information of the relevant packet
                        clientUDPSocket = socket(AF_INET,SOCK_DGRAM)                           # UDP
                        clientUDPSocket.sendto(RDTRetransmission[i], (destIP, destPort))       # resend the prepared message from helper retransmissin array on destIP(Dest_Chose() function will decide whether through r1 or r2)

def Dest_Chose():               # helper function to alter between router1 or router2
    global destIP               # just to be able to change the global variable inside the function
    while True:                 # loop forever 
        if destIP==dest1IP:     # if router1 is selected
            destIP=dest2IP      # change it and select router2
        else:                   # if router2 is selected
            destIP=dest1IP      # change it and select router1

Thread(target=Dest_Chose).start()           # threading for function Dest_Chose()
Thread(target=senderTh).start()             # threading for function senderTh()
Thread(target=RDT_Receiver_Sender).start()  # threading for function RDT_Receiver_Sender()