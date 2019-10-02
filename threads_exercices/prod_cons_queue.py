#!/usr/bin/env python3

import logging
import time
import concurrent.futures
import threading
import random
import queue


SENTINEL = object()


class Pipeline(queue.Queue):
    """
    Class to allow a single element pipeline between producer and consumer
    """

    def __init__(self):
        super().__init__(maxsize=10)

    def get_message(self, name):
        logging.debug(f'{name}: about to get from queue')
        value = self.get()
        logging.debug(f'{name}: got {value} from queue')
        return value

    def set_message(self, value, name):
        logging.debug(f'{name}: about to add {value} to queue')
        self.put(value)
        logging.debug(f'{name}: added {value} to queue')


def producer(pipeline, event):
    """Simulate a message from the network"""
    while not event.is_set():
        message = random.randint(1, 101)
        logging.info(f'Producer got message: {message}')
        pipeline.set_message(message, 'Producer')

    # Send a setinel message tot tell consumer we're done
    logging.info("Producer received EXIT event. Exiting")


def consumer(pipeline, event):
    """Simulate saving a number in the database"""
    message = 0
    while not event.is_set() or not pipeline.empty():
        message = pipeline.get_message('Consumer')
        logging.info(
            'Consumer storing message: %s (queue size=%s)',
            message,
            pipeline.qsize()
        )

    logging.info("Consumer received EXIT event. Exiting")


if __name__ == '__main__':
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M!%S")
    logging.getLogger().setLevel(logging.DEBUG)

    pipeline = Pipeline()
    event = threading.Event()
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(producer, pipeline, event)
        executor.submit(consumer, pipeline, event)

        time.sleep(0.1)
        logging.info("Main: about to set event")
        event.set()

