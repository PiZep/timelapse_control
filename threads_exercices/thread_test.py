#!/usr/bin/env python3

import threading
import concurrent.futures
import time
import logging


class FakeDB:
    def __init__(self):
        self.value = 0
        self._lock = threading.Lock()

    def locked_update(self, name):
        logging.info(f'Thread {name} starting update')
        logging.debug(f'Thread {name} about to lock')
        with self._lock:
            logging.debug(f'Thread {name} has lock')
            local_copy = self.value
            local_copy += 1
            time.sleep(0.1)
            self.value = local_copy
            logging.debug(f'Thread {name} about to release lock')
        logging.debug(f'Thread {name} after release')
        logging.info(f'Thread {name}: finishing update')

    # def update(self, name):
    #     logging.info(f'Thread {name} starting update')
    #     local_copy = self.value
    #     local_copy += 1
    #     time.sleep(0.1)
    #     self.value = local_copy
    #     logging.info(f'Thread {name}: finishing update')


def thread_function(name):
    logging.info(f'Thread {name}: starting')
    time.sleep(2)
    logging.info(f'Thread {name}: finishing')


if __name__ == '__main__':
    format = '%(asctime)s: %(message)s'
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt='%H:%M:%S')
    logging.getLogger().setLevel(logging.DEBUG)

    database = FakeDB()
    logging.info(f'Testind update. Starting value is {database.value}')
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        for index in range(2):
            executor.submit(database.locked_update, index)
    logging.info(f'Testing update. Ending value is {database.value}')

    # with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    #     executor.map(thread_function, range(3))

    # threads = list()
    # for index in range(3):
    #     logging.info(f'Main     : create and start thread {index}')
    #     x = threading.Thread(target=thread_function, args=(index,))
    #     threads.append(x)
    #     x.start()

    # for index, thread in enumerate(threads):
    #     logging.info(f'Main     : before joining thread {index}')
    #     thread.join()
    #     logging.info(f'Main     : thread {index} done')

