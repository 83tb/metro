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


def sendHex(hexstr,serObj):
    """
    Sends string like "FF FE 00 01"
    Returns data dictionary
    """
    return sendBytes(HexToByte(hexstr),serObj)

def sendBytes(byteStr, serObj):
    """
    Sends string like this: string "\xFF\xFE\x00\x01"
    Returns data dictionary
    """
    serObj.write(byteStr)
    byte = serObj.read()
    if byte:
        message = byte + readbytes(4,serObj)

    # Interpret
    baseDict = getCommandAndAddress(message[0],message[1])

    data = {
            'command': baseDict['command'],
            'address': baseDict['address'],
            'parameter': ByteToHex(message[2]),
            'checksum': ByteToHex(message[3]),
    }

    #checksum check
    check = countCheckSum(message[0],message[1],message[2])
    assert str(check) == "0x"+str(data['checksum'])
    print check
    print data['checksum']

    return data

from bitstring import Bits
def getCommandAndAddress(byte1,byte2):
    """
    Gets Two First Bytes, and returns a dictionary with:
    Command
    SetGroup
    Address
    """

    bits16 = Bits(bytes=byte1+byte2)
    command,setGroup,address = bits16.unpack('uint:5,uint:1,uint:10')
    return dict(command=command,setGroup=setGroup,address=address)

def countCheckSum(byte1,byte2,byte3):
    """
    Counts checksum from 3 bytes, returns 4th byte
    """
    listOfBytes = [byte1,byte2,byte3]

    checksum = sum(map(ord, listOfBytes))
    if checksum>128: checksum = checksum - 128

    return hex(checksum)
