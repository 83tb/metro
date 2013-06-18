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


for i in range(1,13):
    #t0 = time()

    #hexstr = makeCommand(getCommandNumber('GetRam'),0,1,i)

    hexstr = "10 08 09 21"
    #t1 = time()
    #print 'function vers1 takes %f' %(t1-t0)

    print "Sent HEX was:"
    print hexstr
    print "What we got was:"
    print sendHex(hexstr, serObj)

    #t2 = time()
    #print 'function vers2 takes %f' %(t2-t1)
