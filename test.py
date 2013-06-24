import serial
from metro import sendHex, makeCommand

from libmadli import getCommandNumber

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
r_server = redis.StrictRedis(host='localhost', port=6379, db=0)
    

from time import time

for i in range(1,2):
 
    time_debug = False
    
    print "METER 0.3.1"
    print
    print "-----------"
    print "[ LOGS ]"
    print     
    t0 = time()


    command_string = 'GetRam'
    device_number = 9
    command_number = getCommandNumber(command_string)
    #memory_address = 13
    
    #r_server.sadd("RAM MAP:" + str(device_number), "value" + memory_address )
    
    
    # RUNNING MEMORY SCAN :)
    # GetEE - eeprom scan, 220 adresses
    # GetRam - ram scan, 16 adresses
    
    
    
    for memory_address in range(0,1):
    
        hexstr = makeCommand(command_number,0,device_number,memory_address)
    
        #print "[ Command: " + command_string + " built, group=False, device_no = " + str(device_number) + " memory address: " + str(memory_address) + " ]"
        
     
        value =  shx(hexstr)
        print value[3:5]
        
        r_server.set("Warehouse:1:Device:" + str(device_number) + ":"+command_string+":" + str(memory_address), int("0x"+value[3:5],16))
     
        
    #hexstr = ""
    #10 09 00 19"""
    
    #hexstr = makeCommand(0,0,device_number,0)
    
    
    t1 = time()
    if time_debug: print '[ Generating command took %f sec ]' %(t1-t0)

   
    
    # when more commands
    #for i in iter(hexstr.splitlines()):
    #    print "[ " + shx(i) + " ]"
    
    print "[ " + shx(hexstr) + " ]"
    
    
    t2 = time()
    if time_debug: print '[ Getting response took %f sec ]' %(t2-t1)
