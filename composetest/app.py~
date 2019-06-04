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

def save_prime(number):
    num = int(number)
    retries = 5
    while True:
        try:
            cache.lpush('primelist',num)
            return
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

def get_prime():
    retries = 5
    while True:
        try:
            return cache.lrange('primelist', 0, -1)
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

def check_prime(number):
    num = int(number)
    for i in range(2, num):
        if(num % i == 0):
            return False
    return True

def run_tests():
    if(test_one() == True and test_two() == True and test_three() == True and test_four() == True and test_five() == True):
        print()
        return 'TESTS PASSED!'
    return 'TESTS FAILED!'

def test_one():
    if(check_prime(67) == True):
        return True
    return False

def test_two():
    if(check_prime(48) == False):
        return True
    return False

def test_three():
    if(check_prime(2) == True):
        return True
    return False

def test_four():
    if(check_prime(5521) == True):
        return True
    return False

def test_five():
    save_prime(67)
    num = cache.lpop('primelist') 
    if(num == b'67'):
        return True
    return False
		            
@app.route('/isPrime/<number>')
def isPrime(number):
    num = int(number)
    if(check_prime(num) == False):
        return '{} is not prime\n'.format(num)
    
    save_prime(num)
    return '{} is prime\n'.format(num)
    
@app.route('/primesStored')
def primesStored():
    primelist = get_prime()
    return '{}\n'.format(primelist)
	    

@app.route('/hello')
def hello():
    count = get_hit_count()
    return 'Hello World! I have been seen {} times.\n'.format(count)

@app.route('/tests')
def tests():
    result = run_tests()		     	
    return '{}\n'.format(result)

