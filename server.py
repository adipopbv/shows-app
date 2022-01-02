import time
from multiprocessing.connection import Listener, Client
from concurrent.futures import ThreadPoolExecutor, ALL_COMPLETED
from threading import Thread, Event
import concurrent


shutdown_event = Event()
executor = ThreadPoolExecutor(5)
operators = []


def run_operator(connection):
    connection = connection
    while not shutdown_event.is_set():
        message = connection.recv()
        connection.send(shutdown_event.is_set())
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
