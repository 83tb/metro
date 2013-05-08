import serial
from metro import sendHex, constructRequest, sendBytes,HexToByte
from hexbyte import ByteToHex
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

#hexstr2 = constructRequest('GetEE',1023,1)

print "Constr"
#print ByteToHex(hexstr2)
print hexstr

print sendHex(hexstr, serObj)

#print sendBytes(hexstr2,serObj)


from bitstring import Bits
testBits = Bits(bytes=HexToByte(hexstr))
first,second,third,fourth = testBits.unpack('uint:5, uint:1, uint:10, uint:8, uint:8')

print first,second,third,fourth