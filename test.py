import serial
from metro import sendHex, constructRequest
serObj = serial.Serial('/dev/ttyUSB1',
                       baudrate=4800,
                       bytesize=serial.EIGHTBITS,
                       parity=serial.PARITY_NONE,
                       stopbits=serial.STOPBITS_ONE,
                       timeout=1,
                       xonxoff=0,
                       rtscts=0
                       )


hexstr = '10 09 09 22'

hexstr2 = constructRequest('GetEE',1023,1)

print "Constructed: " + hexstr2

print sendHex(hexstr, serObj)
