import random
from time import sleep

if __name__ == '__main__':
    from multiprocessing.connection import Client

    connection = Client(('localhost', 6000))
    while True:
        show_id = random.randint(1, 3)
        seats_count = random.randint(1, 100)
        seats_numbers = []
        for seat_number in random.sample(range(0, 100), seats_count):
            seats_numbers.append(seat_number)

        message = [show_id, seats_count, seats_numbers]
        print(f'sending: {message}')
        connection.send(message)
        message = connection.recv()
        print(message)
        if message == 'end':
            connection.close()
            break
        sleep(2)
