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

from bitstring import pack

for i in range(1,10):
    #t0 = time()
    print
    print "###"
    print "ADRES: " + str(i)

    hexstr = makeCommand(getCommandNumber('GetEE'),0,9,20)
    #t1 = time()
    #print 'function vers1 takes %f' %(t1-t0)

    print "Sent HEX was:"
    print hexstr
    print "What we got was:"
    answer = sendHex(hexstr, serObj)
    print answer
    b2 = answer['secondByte']
    b3 = answer['thirdByte']
    bits = pack('hex:8', b2)
    print bits.unpack('uint:8')

    #t2 = time()
    #print 'function vers2 takes %f' %(t2-t1)