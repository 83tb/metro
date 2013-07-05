from rq import Connection, Queue
from redis import Redis


# Tell RQ what Redis connection to use
redis_conn = Redis()
q = Queue('low', connection=redis_conn)  # no args implies the default queue

# Delay calculation of the multiplication
job = q.enqueue(count_words_at_url, 'http://nvie.com')
