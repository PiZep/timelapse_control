#!/usr/bin/env python3

import sys
from multiprocessing.pool import ThreadPool
from subprocess import check_output
import logging

TIMEOUT = 0
CONNECTIONS = 0


def main(argv):
    global CONNECTIONS
    if len(sys.argv) < 3 or len(sys.argv) > 5:
        print('Require 3 or 4 arguments')
        sys.exit(1)
    else:
        ip = argv[1]
        start, end, timeout = (int(i) for i in argv[2:])
    format = '%(asctime)s: %(message)s'
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt='%H:%M:%S')

    # logging.getLogger().setLevel(logging.DEBUG)
    ips = get_active_addresses(ip_list(ip, start, end), timeout=timeout)
    connected = is_connected(ips)
    while connected:
        connected = is_connected(ips)
        if len(ips) != CONNECTIONS:
            CONNECTIONS = len(ips)
            print(len(ips))


def ip_list(ip_base, start, end):
    ip_base = '.'.join(ip_base.split('.')[0:3])
    return ['.'.join((ip_base, str(n))) for n in range(start, (end + 1))]


def ping(ip):
    cmd = f"ping -c2 -n -w {TIMEOUT} {ip}"
    try:
        result = check_output(cmd.split())
        logging.info(f'ping ip {ip}')
    except Exception as e:
        logging.debug(f'ip {ip} raise exception {e}')
        return ip, None, str(e)
    else:
        return ip, result, None


def get_active_addresses(ip_list=['127.0.0.0'], timeout=4):
    global TIMEOUT
    end = int(ip_list[-1].split('.')[-1])
    start = int(ip_list[0].split('.')[-1])
    pool = ThreadPool(end - start + 1)
    logging.debug(f'')
    # active_addresses = []
    TIMEOUT = timeout
    logging.debug(f'TIMEOUT = {TIMEOUT}')

    return [ip for ip, _, error in pool.imap_unordered(ping, ip_list)
            if error is None]


def is_connected(ip_list):
    global CONNECTIONS
    CONNECTIONS = len(ip_list)
    end = int(ip_list[-1].split('.')[-1])
    start = int(ip_list[0].split('.')[-1])
    pool = ThreadPool(end - start + 1)
    for i, ip, _, error in enumerate(pool.imap_unordered(ping, ip_list)):
        if error:
            logging.info(f'Connection lost for {ip}')
            del ip_list[i]
    return len(ip_list)

if __name__ == '__main__':
    main(sys.argv)
