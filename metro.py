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

    data = {
            'command': ByteToHex(message[0]),
            'address': ByteToHex(message[1]),
            'parameter': ByteToHex(message[2]),
            'checksum': ByteToHex(message[3]),

    }

    return data


