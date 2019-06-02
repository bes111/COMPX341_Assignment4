import time

import redis
from flask import Flask

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)


def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/isPrime/<number>')
def isPrime(number):
    num = int(number)
    for i in range(2, num):
        if(num % i == 0):
            return '{} is not prime\n'.format(num)

    return '{} is prime\n'.format(num)
    
@app.route('/hello')
def hello():
    count = get_hit_count()
    return 'Hello World! I have been seen {} times.\n'.format(count)
