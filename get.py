#!/usr/bin/python
"""Testing File

Example of a Metro Daemon with 10 priority queues

"""

import serial
from metro import sendHex, sendHexNoReturn, makeCommand, readCommand

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
    #print "Sending: " + hexstr
    return sendHexNoReturn(hexstr, serObj) 
 

def shx(arg):
    
    hexstr = arg
    #print "Sending: " + hexstr
    return sendHex(hexstr, serObj) 


import redis
from rq import Connection, Queue


r_server = redis.StrictRedis(host='localhost', port=6379, db=0)
    
from time import time, sleep


def executeCommand(command_string, device_number, memory_range):

    time_debug = False

    #print "METER 0.3.1"
    #print
    #print command_string
    #print "-----------"
    #print "[ LOGS ]"
    #print
    t0 = time()



    command_number = getCommandNumber(command_string)


    for memory_address in memory_range:
        #print memory_address
        hexstr = makeCommand(command_number,0,device_number,memory_address)
        
        if command_string == "SetAddr" or command_string == "WriteAddr":
            value = shxNR(hexstr)
        else: 
            value =  shx(hexstr)
            #print readCommand(value)
            return readCommand(value)
        #print "Getting: " + value
    
        #print value
        #if value:
        #    r_server.set("Warehouse:1:Device:" + str(device_number) + ":"+command_string+":" + str(memory_address), int("0x"+value[3:5],16))


    t1 = time()
    if time_debug: print '[ Sending command took %f sec ]' %(t1-t0)

    t2 = time()
    if time_debug: print '[ Getting response took %f sec ]' %(t2-t1)

def turnOn(lamp_number):
    executeCommand('On',lamp_number,range(0,1))
    print executeCommand('On',lamp_number,range(0,1))


def turnOff(lamp_number):
    executeCommand('Off',lamp_number,range(0,1))
    executeCommand('Off',lamp_number,range(0,1))
    #sleep(1)
    
def setDim(lamp_number, dim_ad, dim_level):
    executeCommand('SetAddr',lamp_number,range(dim_ad,dim_ad+1))
    executeCommand('WriteAddr',lamp_number,range(dim_level,dim_level+1))
    executeCommand('WriteAddr',lamp_number,range(dim_level,dim_level+1))
    
def getRamValue(lamp_number, address):
    print executeCommand('GetRam',lamp_number,range(address,address+1))


lamp_num = 9

#turnOff(lamp_num)
#setDim(lamp_num, 0, 50)
#getRamValue(lamp_num,0)
getRamValue(lamp_num,0)

"""
sleep(1)

turnOn(lamp_num)
setDim(lamp_num, 0, 44)
getRamValue(lamp_num,0)

sleep(1)

turnOff(lamp_num)
setDim(lamp_num, 0, 254)
getRamValue(lamp_num,0)


"""
#sleep(10)

#setDim(lamp_num, 0, 82)
#getRamValue(lamp_num,0)

