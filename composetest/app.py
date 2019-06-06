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
            if(in_list(num) == True):
                return
            cache.lpush('primelist',num)
            return
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

def convert_to_byte(bytearray):
    intarray = []
    for i in bytearray:
        intarray.append(int(i))
    return intarray

def in_list(number):
    num = number
    bytearray = cache.lrange('primelist', 0, -1)
    intarray = convert_to_byte(bytearray)
    for i in intarray:
        if(num == i):
            return True
    return False
    

def get_prime():
    retries = 5
    while True:
        try:
            bytearray = cache.lrange('primelist', 0, -1)            
            return convert_to_byte(bytearray)
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

def check_prime(number):
#https://stackoverflow.com/questions/46841968/fastest-way-of-testing-if-a-number-is-prime-with-python Was very helpful for speeding up the prime number checker Code was adapted from this website to help create prime number checker. Code is very similar except boolean was returned  
    num = int(number)
    if(num == 1):
        return False
    if(num == 2):
        return True
    if(num & 1 == 0):
        return False
    divisor = 3
    while divisor * divisor <= num:
        if(num % divisor == 0):
            return False
        divisor = divisor + 2
    return True

def run_tests():
    if(test_one() == True and test_two() == True and test_three() == True and test_four() == True and test_five() == True and test_six() == True ):
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
    if(check_prime(6878) == False):
        return True
    return False

def test_six():
    save_prime(67)
    if(in_list(67) == True):
        num = cache.lpop('primelist') 
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








