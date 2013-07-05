from test import executeCommand

command_string = 'GetRam'
device_number = 1
memory_range = range(0,30)

#executeCommand(command_string,device_number,memory_range)


import redis
from rq import Connection, Queue


print "Starting Redis Server"
r_server = redis.StrictRedis(host='localhost', port=6379, db=0)


print "Setting queue"
kolejka = Queue('low', connection=r_server)

print "enq job"
job = kolejka.enqueue(executeCommand, command_string,device_number,memory_range)
command_string = 'GetEE'
device_number = 1
memory_range = range(0,30)

print "eng 2nd job"
job2 = kolejka.enqueue(executeCommand, command_string,device_number,memory_range)
