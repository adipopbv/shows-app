import sys
from time import sleep

if __name__ == '__main__':
    from multiprocessing.connection import Client

    connection = Client(('localhost', 6000))
    while True:
        connection.send('something')
        message = connection.recv()
        if message is True:
            connection.close()
            break
        sleep(int(sys.argv[1]))
