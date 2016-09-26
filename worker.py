import os
import redis
from rq import Worker, Queue, Connection

listen = ['high', 'default', 'low']
redist_url = os.getenv('REDISGOTO_URL', 'redis://localhost:6379')

conn = redis.from_url(redist_url)

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(map(Queue, listen))
        worker.work();
