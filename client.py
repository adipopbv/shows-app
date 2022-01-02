import sys
from time import sleep

if __name__ == '__main__':
    from multiprocessing.connection import Client

    connection = Client(('localhost', 6000))
    while True:
        # [show_id, seats_count, [seat_1, ...]]
        connection.send('something')
        message = connection.recv()
        if message is 'end':
            connection.close()
            break
        sleep(int(sys.argv[1]))
