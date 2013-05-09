import serial
from metro import sendHex, constructRequest, sendBytes,HexToByte
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


from bitstring import Bits, pack

def makeCommand(command,setgroup,address,parameter):
    bits = pack('uint:5, uint:1, uint:10, uint:8, uint:8',
                command,setgroup,address,parameter,34)

    byte1,byte2,byte3,byte4  = bits.unpack('bytes:1,bytes:1,bytes:1,bytes:1')
    listOfBytes = [byte1,byte2,byte3]

    checksum = sum(map(ord, listOfBytes))
    if checksum>128: checksum = checksum - 128

    bits = pack('uint:5, uint:1, uint:10, uint:8, uint:8',
                command,setgroup,address,parameter,checksum)

    return ByteToHex(bits.bytes)

hexstr = makeCommand(getCommandNumber('GetRam'),0,9,9)

print hexstr
print sendHex(hexstr, serObj)
