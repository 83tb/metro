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

def sendHex(hexstr,serObj):
    """
    Sends string like "FF FE 00 01"
    Returns data dictionary
    """
    return sendBytes(HexToByte(hexstr),serObj)

def validate(byteStr):
    bits32 = Bits(bytes=byteStr)
    first,second,third,fourth = bits32.unpack('bytes:1,bytes:1,bytes:1,bytes:1')
    check = countCheckSum(first,second,third)
    assert str(check) == "0x"+str(ByteToHex(fourth))

def sendBytes(byteStr, serObj):
    """
    Sends string like this: string "\xFF\xFE\x00\x01"
    Returns data dictionary
    """

    # we will send ONLY VALID string, with checksum which is ok
    validate(byteStr)

    serObj.write(byteStr)
    response1 = ByteToHex(readbytes(4,serObj))

    byte = serObj.read()

    if byte:
        message = byte + readbytes(4,serObj)

    # Interpret
    baseDict = getStatusByte(message[0])

    data = {


            'status1': baseDict['status1'],
            'status2': baseDict['status2'],


    }

    #checksum check
    #check = countCheckSum(message[0],message[1],message[2])
    # return only valid data
    #assert str(check) == "0x"+str(data['checksum'])

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

def getStatusByte(byte1):
    """
    Gets Two First Bytes, and returns a dictionary with:
    Command
    SetGroup
    Address
    """

    bits8 = Bits(bytes=byte1)
    status1,status2 = bits8.unpack('uint:4,uint:4')
    return dict(status1=status1,status2=status2)



def countCheckSum(byte1,byte2,byte3):
    """
    Counts checksum from 3 bytes, returns 4th byte
    """
    listOfBytes = [byte1,byte2,byte3]

    checksum = sum(map(ord, listOfBytes))
    if checksum>128: checksum = checksum - 128

    return hex(checksum)


def countCheckSumByte(byte1,byte2,byte3):
    """
    Counts checksum from 3 bytes, returns 4th byte
    """
    listOfBytes = [byte1,byte2,byte3]

    checksum = sum(map(ord, listOfBytes))
    if checksum>128: checksum = checksum - 128

    return HexToByte(hex(checksum)[2:3])





from libmadli import getCommandNumber

from bitstring import pack
def constructRequest(command, address, parameter):
    command_number = getCommandNumber(command)
    bits32 = pack('uint:5, uint:1, uint:10, uint:8, uint:8', command_number, 0, address, parameter, 0)
    first,second,third,fourth = bits32.unpack('bytes:1,bytes:1,bytes:1,bytes:1')
    check = countCheckSumByte(first,second,third)
    bits = pack('uint:5, uint:1, uint:10, uint:8, bytes:1', command_number, 0, address, parameter, check)


    return bits.bytes

