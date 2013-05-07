from bitstring import BitStream, Bits
packet_data = '13ff091b'

#zapalanie
#sciemnianie
#odczyt statusow

import serial
serObj = serial.Serial('/dev/ttyUSB1',
                       baudrate=4800,
                       bytesize=serial.EIGHTBITS,
                       parity=serial.PARITY_NONE,
                       stopbits=serial.STOPBITS_ONE,
                       timeout=1,
                       xonxoff=0,
                       rtscts=0
                       )


from hexbyte import *

def readbytes(number,serObj):
    buf = ''
    for i in range(number):
        byte = serObj.read()
        buf += byte

    return buf

# binarnego anda z maska 1111111, FFFFFFF

hexstr = '10 09 09 22'


def send(hexstr, serObj):
    serObj.write(HexToByte(hexstr))
    byte = serObj.read()
    if byte:
        message = byte + readbytes(4,serObj)

    data = {
            'command': ByteToHex(message[0]),
            'address': ByteToHex(message[1]),
            'parameter': ByteToHex(message[2]),
            'checksum': ByteToHex(message[3]),

    }

    return data

print send(hexstr, serObj)
