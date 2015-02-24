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

import logging
logging.basicConfig(filename='lampy.log', level=logging.INFO)


def turnOn(lamp_number):
    executeCommand('On',lamp_number,range(0,1))
    logging.info(executeCommand('On',lamp_number,range(0,1)))


def turnOff(lamp_number):
    executeCommand('Off',lamp_number,range(0,1))
    executeCommand('Off',lamp_number,range(0,1))
    #sleep(1)

def setDim(lamp_number, dim_level):
    executeCommand('On',lamp_number,range(dim_level,dim_level+1))
    executeCommand('On',lamp_number,range(dim_level,dim_level+1))


import logging
logging.basicConfig(filename='lampy.log', level=logging.INFO)

def getRamValue(lamp_number, address):
    prefix = "Numer lampy: " + str(lamp_num) + " Status: "# + datetime.datetime()           
    output = executeCommand('GetRam',lamp_number,range(address,address+1))
    logging.info(prefix + str(output))


lamp_nums = [845,126,846,19]

for lamp_num in lamp_nums:
    turnOn(lamp_num)
    setDim(lamp_num, 255)


import sys
counter = 102

import datetime
while True:
    if counter == 120:
        for lamp_num in lamp_nums:
            turnOff(lamp_num)
                   
    if counter == 240:
        for lamp_num in lamp_nums:
            turnOn(lamp_num)
            counter = 0
    
    counter = counter + 1
    
    info =  "## Minute " + str(counter)
    logging.info(info)
        
    for lamp_num in lamp_nums:
        try:
            getRamValue(lamp_num, 0)
        except:
            logging.error("Error reading: " + str(lamp_num))
    sleep(60)
