from hexbyte import *
from bitstring import Bits, pack
from libmadli import getSt3st0,getSt7st4


def readbytes(number,serObj):
    """
    Read bytes from serial port
    """
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

def validateOutgoing(byteStr):
    bits32 = Bits(bytes=byteStr)
    first,second,third,fourth = bits32.unpack('bytes:1,bytes:1,bytes:1,bytes:1')
    check = countCheckSumOutgoing(first,second,third)

    assert str(check) == "0x"+str(ByteToHex(fourth))



def validateIncoming(byteStr):
    bits32 = Bits(bytes=byteStr)
    first,second,third,fourth = bits32.unpack('bytes:1,bytes:1,bytes:1,bytes:1')
    check = countCheckSumIncoming(first,second,third)
    assert str(check) == "0x"+str(ByteToHex(fourth)).lower()

from time import time

def sendBytes(byteStr, serObj):
    """
    Sends string like this: string "\xFF\xFE\x00\x01"
    Returns data dictionary
    """

    # we will send ONLY VALID string, with checksum which is ok
    #validateOutgoing(byteStr)
    t0 = time()

    serObj.write(byteStr)
    t1 = time()


    response1 = ByteToHex(readbytes(4,serObj))
    t2 = time()


    byte = serObj.read()
    t3 = time()


    if byte:
        message = byte + readbytes(4,serObj)
    t4 = time()

    # Interpret
    #baseDict = getStatusByte(message[0])

    data = {


            #'status1': baseDict['status1'],
            #'status2': baseDict['status2'],
            'firstByte': ByteToHex(message[0]),
            'secondByte': ByteToHex(message[1]),
            'thirdByte': ByteToHex(message[2]),


            'checksum': message[3]


    }

    print 'Write takes %f' %(t1-t0)
    print 'First takes %f' %(t2-t1)
    print 'Second takes %f' %(t3-t2)
    print 'Third takes %f' %(t4-t3)



    # return only valid data
    #validateIncoming(message)

    return data



def getStatusByte(byte1):
    """
    Gets Two First Bytes, and returns a dictionary with:
    Command
    SetGroup
    Address
    """

    bits8 = Bits(bytes=byte1)
    status1,status2 = bits8.unpack('uint:4,uint:4')
    return dict(status1=getSt3st0(status1),status2=getSt7st4(status2))


def makeCommand(command,setgroup,address,parameter):
    """
    Construct command to be send
    Takes integers
    Returns HEX in a format: 10 09 09 22
    """

    # we pack the data so we can count checksum
    bits = pack('uint:5, uint:1, uint:10, uint:8',
                command,setgroup,address,parameter)

    byte1,byte2,byte3  = bits.unpack('bytes:1,bytes:1,bytes:1')


    #this code should be replaced with countChecksumOutgoing function call
    listOfBytes = [byte1,byte2,byte3]

    checksum = sum(map(ord, listOfBytes))
    if checksum>128: checksum = checksum - 128
    ###


    bits = pack('uint:5, uint:1, uint:10, uint:8, uint:8',
                command,setgroup,address,parameter,checksum)

    return ByteToHex(bits.bytes)



def countCheckSumOutgoing(byte1,byte2,byte3):
    """
    Counts checksum from 3 bytes, returns the checksum byte
    """
    listOfBytes = [byte1,byte2,byte3]

    checksum = sum(map(ord, listOfBytes))
    if checksum>128: checksum = checksum - 128

    return hex(checksum)


def countCheckSumIncoming(byte1,byte2,byte3):
    """
    Counts checksum from 3 bytes, returns the checksum byte
    """
    listOfBytes = [byte1,byte2,byte3]

    checksum = sum(map(ord, listOfBytes))
    if checksum<128: checksum = checksum + 128

    return hex(checksum)





