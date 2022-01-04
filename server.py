import time
from multiprocessing.connection import Listener, Client
from concurrent.futures import ThreadPoolExecutor, ALL_COMPLETED
from threading import Thread, Event
import concurrent
import services as services


shutdown_event = Event()
executor = ThreadPoolExecutor(5)
operators = []


def run_operator(connection):
    connection = connection
    while not shutdown_event.is_set():
        message = connection.recv()
        if shutdown_event.is_set():
            connection.send('end')
            return
        try:
            show_id, seats_count, seats_numbers = message
            print(f'selling seats: {message}')
            services.sell_seats(show_id, seats_count, seats_numbers)
            print('success')
            connection.send('success')
        except Exception as e:
            print(f'error: {str(e)}')
            connection.send(f'error: {str(e)}')


def run_dispatcher():
    while not shutdown_event.is_set():
        connection = listener.accept()
        operator = executor.submit(run_operator, connection)
        operators.append(operator)


def run_verification(seconds: int):
    open("sales.txt", "w").close()
    while not shutdown_event.is_set():
        time.sleep(seconds)
        services.verify_sells()


if __name__ == '__main__':
    listener = Listener(('localhost', 6000))
    thread = Thread(target=run_dispatcher)
    thread.start()
    verification_thread = Thread(target=run_verification, args=(5,))
    verification_thread.start()
    time.sleep(10)
    shutdown_event.set()
    Client(('localhost', 6000))
    listener.close()
    thread.join()
    verification_thread.join()
    concurrent.futures.wait(operators, timeout=None, return_when=ALL_COMPLETED)
    services.reset_database()
