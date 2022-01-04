from datetime import datetime
from threading import Lock

from repositories import SqliteSalesRepository, SqliteShowsRepository, \
    SqliteSoldSeatsRepository, SqliteRepository

repo = SqliteRepository()
sales_repo = SqliteSalesRepository()
shows_repo = SqliteShowsRepository()
sold_seats_repo = SqliteSoldSeatsRepository()
lock = Lock()


def sell_seats(show_id: int, seats_count: int, seats_numbers: list) -> None:
    lock.acquire()

    show = shows_repo.get(show_id)
    sold_seats_to_show = sold_seats_repo.get_for_show(show_id)

    if show.room.seats_count < len(sold_seats_to_show):
        lock.release()
        raise Exception('all seats taken')
    if seats_count > show.room.seats_count - len(sold_seats_to_show):
        lock.release()
        raise Exception('not enough seats available')
    for wanted_seat_number in seats_numbers:
        for sold_seat in sold_seats_to_show:
            if wanted_seat_number == sold_seat.seat_number:
                lock.release()
                raise Exception('seat already taken')

    sale_id = sales_repo.add(datetime.now(), show)
    shows_repo.update(show_id, seats_count, seats_count * show.ticket_price)
    sale = sales_repo.get(sale_id)
    for wanted_seat_number in seats_numbers:
        sold_seats_repo.add(wanted_seat_number, sale)

    lock.release()


def verify_sells():
    file = open("sales.txt", "a")

    file.write("Date and time: " + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "\n")

    shows = shows_repo.get_all()
    for show in shows:
        correct_transactions = True
        file.write(f"Show: {show.show_id} {show.title}, price for one ticket: {show.ticket_price} \n")

        sold_seats = sold_seats_repo.get_for_show(show.show_id)
        nr_sold_seats = len(sold_seats)
        balance = nr_sold_seats * show.ticket_price
        file.write("Balance: " + str(balance) + "\n")

        file.write("Number of sold sets: " + str(nr_sold_seats) + "\n")
        file.write("Sold seats: ")
        for sold_seat in sold_seats:
            file.write(str(sold_seat.seat_number) + " ")

        if show.room.seats_count - nr_sold_seats != show.available_seats_count:
            correct_transactions = False

        if show.balance - balance != 0:
            correct_transactions = False

        if correct_transactions:
            file.write("\nCorrect\n")
        else:
            file.write("\nWrong\n")

        file.write("\n")

    file.close()


def reset_database():
    repo.reset_data()
    repo.close_connection()
