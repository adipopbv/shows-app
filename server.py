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
            show_id, seats_count, seats = message
            services.sell_tickets(show_id, seats_count, seats)
            connection.send('success')
        except Exception:
            connection.send('failure')
        print(message)


def run_dispatcher():
    while not shutdown_event.is_set():
        connection = listener.accept()
        operator = executor.submit(run_operator, connection)
        operators.append(operator)


if __name__ == '__main__':
    listener = Listener(('localhost', 6000))
    thread = Thread(target=run_dispatcher)
    thread.start()
    time.sleep(10)
    shutdown_event.set()
    Client(('localhost', 6000))
    listener.close()
    thread.join()
    concurrent.futures.wait(operators, timeout=None, return_when=ALL_COMPLETED)
