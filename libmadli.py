commands = {
    'On' : 0,
    'Off' : 1,
    'GetRam' : 2,
    'GetEE' : 3,
    'SetAddr' : 4,
    'SetGrp0' : 5,
    'SetGrp1' : 6,
    'SetGrp2' : 7,
    'SetGrp3' : 8,
    'Lock' : 9,
    'WriteAddr' : 10,
    'SetEEAddr' : 11,
    'SetEEData' : 12,
    'Test' : 13,
    'Prefix' : 14,
    }

def getCommandNumber(name):
    return commands[name]


