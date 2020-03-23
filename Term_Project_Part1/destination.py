from socket import *											# importing socket library
import time														# importing time library

serverPort = 5011												# port number(randomly chosen)
bufferSize = 11													# 11 is 10+1 and 10 for packet size + 1 for index numbers

serverSocket = socket(AF_INET, 									# Internet					
SOCK_DGRAM) 													# UDP
serverSocket.bind(('', serverPort))								# binding socket with related port

print('The destination is ready to receive...')					# printing just to see that the destination is on and ready to serve 

f = open("delay_end.txt", "a")									# opening txt file for arriving time info
f.write("---------------------------------\n")					# just printing -'s and a new line to separate datas

array=[]														# empty array initialization for collecting the incoming messages together
while len(array)<10:											# iterate 10 times because client sends length of 100's and routers send them 10 by 10
    message, clientAddress = serverSocket.recvfrom(bufferSize)	# get datagram of the size "bufferSize" from Routers
    array.append(message)										# append each incoming message to the array

array2=["","","","","","","","","",""]							# empty array initialization for adding the indexes to the messages
for x in array:													# for each element in array
    index=x[10]													# these indexes will help to sort the incoming messages according to their coming time 
    array2[int(index)]=x[0:10]									# filling up the helper array

result=""														# empty string initialization for getting the messages sorted in it
for y in array2:												# for each element in array2
    result+=y													# fill the resulting string from helper array2
    if len(result)==100:										# it means we have got all the messages
        end = str(int(round(time.time() * 1000)))				# get the time
        f.write("end : "+end+"\n")								# write that time to the file
        break													# leave the loop since we have all the messages

print(result)													# print the resulting final string that is arrived
f.close()														# close the txt file
