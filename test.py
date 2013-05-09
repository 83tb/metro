import serial
from metro import sendHex, makeCommand, sendBytes,HexToByte
from hexbyte import ByteToHex
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




hexstr = makeCommand(getCommandNumber('GetRam'),0,9,9)

print "Sent HEX was:"
print hexstr
print "What we got was:"
print sendHex(hexstr, serObj)
