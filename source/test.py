
"""Testing File

Example of a Metro Daemon with 10 priority queues

"""



import serial
from source.metro import sendHex, makeCommand

from source.libmadli import getCommandNumber

serObj = serial.Serial('/dev/ttyUSB0',
                       baudrate=4800,
                       bytesize=serial.EIGHTBITS,
                       parity=serial.PARITY_NONE,
                       stopbits=serial.STOPBITS_ONE,
                       timeout=1,
                       xonxoff=0,
                       rtscts=0
                       )

def shx(arg):
    
    hexstr = arg
    return sendHex(hexstr, serObj) 


import redis
from rq import Connection, Queue


r_server = redis.StrictRedis(host='localhost', port=6379, db=0)
    
from time import time


def executeCommand(command_string, device_number, memory_range):

    time_debug = False

    print "METER 0.3.1"
    print
    print "GET RAM"
    print "-----------"
    print "[ LOGS ]"
    print
    t0 = time()



    command_number = getCommandNumber(command_string)


    for memory_address in memory_range:

        hexstr = makeCommand(command_number,0,device_number,memory_address)
        value =  shx(hexstr)

        if value:
            r_server.set("Warehouse:1:Device:" + str(device_number) + ":"+command_string+":" + str(memory_address), int("0x"+value[3:5],16))


    t1 = time()
    if time_debug: print '[ Generating command took %f sec ]' %(t1-t0)




    #print "[ " + shx(hexstr) + " ]"


    t2 = time()
    if time_debug: print '[ Getting response took %f sec ]' %(t2-t1)



command_string = 'GetRam'
device_number = 9
memory_range = range(0,30)

executeCommand(command_string,device_number,memory_range)




kolejka = Queue('low', connection=r_server)
job = q.enqueue(executeCommand, command_string,device_number,memory_range)




# this is going to be a part of command reader (text format)
    # when more commands
    #for i in iter(hexstr.splitlines()):
    #    print "[ " + shx(i) + " ]"