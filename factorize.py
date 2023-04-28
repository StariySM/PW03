import time
from multiprocessing import Pool, current_process, cpu_count
import concurrent.futures
import logging

logger = logging.getLogger()
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(threadName)s - %(message)s')
stream_handler.setFormatter(formatter)

def time_of_function(function):
    def wrapped(*args):
        start_time = time.perf_counter()
        res = function(*args)
        print(time.perf_counter() - start_time)
        return res
    return wrapped

# @time_of_function
def factorize(*number):
    name = current_process().name
    logging.debug(f'{name}start')
    start_time = time.perf_counter()
    result = []
    for num in number:
        el_res = []
        for i in range(1, num + 1):
            if not num % i:
                el_res.append(i)
        result.append(el_res)
    logging.debug(f'{name} finished')
    return result

def factorize(*number):
    name = current_process().name
    logging.debug(f'{name} start')
    start_time = time.perf_counter()
    result = []
    for num in number:
        el_res = []
        for i in range(1, num + 1):
            if not num % i:
                el_res.append(i)
        result.append(el_res)
    logging.debug(f'{name} finished')
    return result

def factorize_n(num):
    name = current_process().name
    logging.debug(f'{name} start')
    start_time = time.perf_counter()
    el_res = []
    for i in range(1, num + 1):
        if not num % i:
            el_res.append(i)
    logging.debug(f'{name} finished')
    return el_res

if __name__ == '__main__':
    n = cpu_count()
    number = (128, 255, 99999, 10651060)
    # logging.debug(f'start')
    start_time = time.perf_counter()
    a, b, c, d = factorize(*number)
    logging.debug(f'calculation finished for {time.perf_counter() - start_time} seconds')
    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106,
                 1521580, 2130212, 2662765, 5325530, 10651060]
    start_time = time.perf_counter()
    with Pool(processes=n) as pool:
        a, b, c, d = (pool.map(factorize_n, number))
    logging.debug(f'finished for {time.perf_counter() - start_time} seconds')
    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106,
                 1521580, 2130212, 2662765, 5325530, 10651060]
