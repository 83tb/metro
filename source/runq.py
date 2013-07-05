from test import executeCommand

command_string = 'GetRam'
device_number = 1
memory_range = range(0,30)

#executeCommand(command_string,device_number,memory_range)


import redis
from rq import Connection, Queue


r_server = redis.StrictRedis(host='localhost', port=6379, db=0)




kolejka = Queue('low', connection=r_server)
job = kolejka.enqueue(executeCommand, command_string,device_number,memory_range)

