from socket import * 											# importing socket library

serverPort = 5011 												# incoming port number(randomly chosen)
destPort=serverPort 											# outgoing port number(randomly chosen)
destIP='10.10.3.2' 												# IP of destination node(d)
bufferSize = 11 												# 11 is 10+1 and 10 for packet size + 1 for index numbers

serverSocket = socket(AF_INET, 									# Internet
SOCK_DGRAM) 													# UDP
serverSocket.bind(('', serverPort)) 							# binding socket with related port

print('The R2 is ready to receive...') 							# printing just to see that the router2 is on and ready to serve 

while True:
    message, clientAddress = serverSocket.recvfrom(bufferSize)  # get UDP datagram of the size "bufferSize" from broker
    clientUDPSocket = socket(AF_INET, 							# Internet
    SOCK_DGRAM) 												# UDP
    clientUDPSocket.sendto(message, (destIP, destPort)) 
    if len(message)==11:										# send the incoming datagram to destination
    	print "Message sent from R2 to Destination:", message 	# print the sent message
