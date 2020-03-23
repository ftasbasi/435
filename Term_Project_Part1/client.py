from socket import *								# importing socket library
import time											# importing time library

serverIP = '10.10.1.2'								# IP of destination node(B)
serverPort = 5010									# port number(randomly chosen)
bufferSize = 100									# we have randomly chosen 100 for the size of the message we want to send

in_file = open("file.txt", "rt")  					# open file file.txt for reading the byte stream message data
contents = in_file.read()         					# read the entire file into a string variable
in_file.close()                  				 	# close the file

print "sending whole data : " + contents			# printing the whole message that we want to send

f = open("delay_start.txt", "a")					# opening txt file for sending time info
f.write("---------------------------------\n")		# just printing -'s and a new line to separate datas

i=0													# just for loop constant
boundary_of_string=len(contents)					# just for the loop again
for i in range(0, boundary_of_string, 100):			# separate whole message 100 by 100
    clientSocket = socket(AF_INET, SOCK_STREAM)		# TCP
    clientSocket.connect((serverIP, serverPort))	# connecting
    clientSocket.send(contents[i:i+100])			# send 100 by 100 separately
    start = str(int(round(time.time() * 1000)))		# start time info
    f.write("start : "+start+"\n")					# write that starting time info to the file
    clientSocket.close()							# close the socket
    
f.close()											# close the time info file
		