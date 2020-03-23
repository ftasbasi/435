from socket import *                                                            # importing socket library
serverPort = 5010                                                               # port number(randomly chosen) which is port for listenig TCP packets from source
routerPort = 5011                                                               # port number(randomly chosen) which is port for sending UDP packets to routers
bufferSize = 100                                                                # 100 since source will send info of size 100

serverSocket = socket(AF_INET, SOCK_STREAM)                                     # TCP
serverSocket.bind(('', serverPort))                                             # binding socket with port
serverSocket.listen(1)                                                          # TCP server is listening...

print('The server is ready to receive...')                                      # just printing to check that broker is on and ready

router1IP = "10.10.2.2"                                                         # IP of router1 for sending
router2IP = "10.10.4.2"                                                         # IP of router2 for sending

while True:
    connectionSocket, addr = serverSocket.accept()                              # accepting socket for TCP server
    message = connectionSocket.recv(bufferSize)                                 # get TCP stream of the size "bufferSize" from broker
    if not message: break                                                       # leave the loop if message is over
    connectionSocket.send(message)                                              # echo

    array=[]                                                                    # empty array initialization for breaking up the incoming messages
    j=0                                                                         # loop constants
    boundary_of_string=len(message)                                             # loop constants
    for j in range(0, boundary_of_string, 10):                                  # break the message up 10 by 10 according to the size
        array.append(message[j:j+10])                                           # append all the broken parts to the helper array one by one

    i=0                                                                         # loop constant
    while i<len(array):                                                         # until the array is over 
        sending_packet=""                                                       # empty string initialization for the message to be sent       
        sending_packet+=array[i]                                                # append the message to be sent to the helper array
        sending_packet+=str(i)                                                  # add helper index at the end of the string(it will help to sort on destination)
        if i%2==0:                                                              # send the ones with EVEN index numbers to ROUTER1 (just to share between R1 and R2)
            clientUDPSocket = socket(AF_INET,                                   # Internet
            SOCK_DGRAM)                                                         # UDP
            clientUDPSocket.sendto(sending_packet, (router1IP, routerPort))     # send the prepared message to R1
            if len(sending_packet) == 11:                                       # just to make sure that the message size is 11(10 for message + 1 for helper index)
                print "Message sent from broker to R1:", sending_packet         # print the message sent to R1(with index info)
        else:                                                                   # send the ones with ODD index numbers to ROUTER2 (just to share between R1 and R2)
            clientUDPSocket = socket(AF_INET,                                   # Internet
            SOCK_DGRAM)                                                         # UDP
            clientUDPSocket.sendto(sending_packet, (router2IP, routerPort))     # send the prepared message to R2
            if len(sending_packet) == 11:                                       # just to make sure that the message size is 11(10 for message + 1 for helper index)
                print "Message sent from broker to R2:", sending_packet         # print the message sent to R2(with index info)

        i+=1                                                                    # for iteration to continue
    connectionSocket.close()                                                    # close TCP connection (at every turn) at the end
