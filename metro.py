from bitstring import BitStream, Bits
packet_data = '13ff091b'

#zapalanie
#sciemnianie
#odczyt statusow

import serial
ser = serial.Serial('/dev/ttyUSB1',
                       baudrate=4800,
                       bytesize=serial.EIGHTBITS,
                       parity=serial.PARITY_NONE,
                       stopbits=serial.STOPBITS_ONE,
                       timeout=1,
                       xonxoff=0,
                       rtscts=0
                       )


from hexbyte import *

def readbytes(number):
    buf = ''
    for i in range(number):
        byte = ser.read()
        buf += byte

    return buf

# binarnego anda z maska 1111111, FFFFFFF

init1 = '10 09 09 22'
ser.write(HexToByte(init1))

# listen for the response string: FF 55 04 09 00 00 07 EC
#print readbytes(4)
response1 = ByteToHex(readbytes(4))
#assert response1 == 'FF 55 04 09 00 00 07 EC'
print response1

# send the second init string
#init2 = 'FF 55 02 09 05 F0'
#ser.write(HexToByte(init2))

# listen for the response string: FF 55 04 09 06 00 25 C8
#response2 = ByteToHex(readbytes(8))
#assert response2 == 'FF 55 04 09 06 00 25 C8'
print "and"

byte = ser.read()
    # if a byte is coming down the port,
if byte:
        # get the rest of the message (34 chars)
    message = byte + readbytes(4)
        # and decipher it
    print message
    data = {
            'command': ByteToHex(message[0]),
            'address': ByteToHex(message[1]),
            'parameter': ByteToHex(message[2]),
            'checksum': ByteToHex(message[3]),
            
    }    
    print data