from socket import *         # importing socket library
import time                  # importing time library
from threading import *      # importing threading library

serverIP = '10.10.1.2'       # IP of destination node(B)
serverPort = 5010            # port number(randomly chosen)
bufferSize = 100             # we have randomly chosen 100 for the size of the message we want to send

print "sending whole data : \n"         # just to inform  
with open("file.txt", "r") as ins:      # open file named file.txt as "ins"
    array = []                          # empty helper array initialization
    for line in ins:                    # for each line in our file.txt
        array.append(line)              # append the line to array
        print(line)                     # print the line just to see
    ins.close()                         # close the file.txt

line_count=len(array)                   # hold the length of the array in a variable named "line_count"

for x in range(1,line_count):           # loop exactly "line_count" times
    print(array[x])                     # print each element of array 

def work():
        line_index=0

        f = open("delay_start.txt", "a")                       # opening txt file for sending time info
        f.write("---------------------------------\n")         # just printing -'s and a new line to separate data

        for i in range(0, line_count):                         # loop exactly "line_count" times
            clientSocket = socket(AF_INET, SOCK_STREAM)        # TCP
            clientSocket.connect((serverIP, serverPort))       # connecting
            clientSocket.send(array[i])                        # send 100 by 100 separately from the array's elements
            start = str(int(round(time.time() * 1000)))        # start time info
            f.write("start : " + start + "\n")                 # write that starting time info to the file
            clientSocket.close()                               # close the socket

        f.close()                                              # close the time info file

Thread(target=work).start()                                    # threading for function work()
