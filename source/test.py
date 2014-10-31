#!/usr/bin/python
"""Testing File

Example of a Metro Daemon with 10 priority queues

"""

import serial
from metro import sendHex, sendHexNoReturn, makeCommand

from libmadli import getCommandNumber

serObj = serial.Serial('/dev/ttyUSB1',
                       baudrate=4800,
                       bytesize=serial.EIGHTBITS,
                       parity=serial.PARITY_NONE,
                       stopbits=serial.STOPBITS_ONE,
                       timeout=1,
                       xonxoff=0,
                       rtscts=0
                       )


def shxNR(arg):
    hexstr = arg
    print "Sending: " + hexstr
    return sendHexNoReturn(hexstr, serObj) 
 

def shx(arg):
    
    hexstr = arg
    print "Sending: " + hexstr
    return sendHex(hexstr, serObj) 


import redis
from rq import Connection, Queue


r_server = redis.StrictRedis(host='localhost', port=6379, db=0)
    
from time import time


def executeCommand(command_string, device_number, memory_range):

    time_debug = True

    #print "METER 0.3.1"
    print
    print command_string
    print "-----------"
    print "[ LOGS ]"
    print
    t0 = time()



    command_number = getCommandNumber(command_string)


    for memory_address in memory_range:
        print memory_address
        hexstr = makeCommand(command_number,0,device_number,memory_address)
        
        if command_string == "WriteAddr" or command_string == "SetAddr":
            value = shxNR(hexstr)
        else: 
            value =  shx(hexstr)
        print "Getting: " + value
    
        #print value
        #if value:
        #    r_server.set("Warehouse:1:Device:" + str(device_number) + ":"+command_string+":" + str(memory_address), int("0x"+value[3:5],16))


    t1 = time()
    if time_debug: print '[ Sending command took %f sec ]' %(t1-t0)

    t2 = time()
    if time_debug: print '[ Getting response took %f sec ]' %(t2-t1)


#"""
#command_string = 'On'
#device_number = 195
#Bmemory_range = range(0,1)

#executeCommand(command_string,device_number,memory_range)

executeCommand('On',464,range(0,1))
executeCommand('On',464,range(0,1))
executeCommand('SetAddr',464,range(0,1))


executeCommand('WriteAddr',464,range(91,92))
executeCommand('GetRam',464,range(0,1))


#"""


#kolejka = Queue('low', connection=r_server)
#job = kolejka.enqueue(executeCommand, command_string,device_number,memory_range)

# this is going to be a part of command reader (text format)
    # when more commands
    #for i in iter(hexstr.splitlines()):
    #    print "[ " + shx(i) + " ]"