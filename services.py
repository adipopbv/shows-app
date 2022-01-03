from datetime import datetime
from threading import Lock

from repositories import SqliteSalesRepository, SqliteShowsRepository, \
    SqliteSoldSeatsRepository

sales_repo = SqliteSalesRepository()
shows_repo = SqliteShowsRepository()
sold_seats_repo = SqliteSoldSeatsRepository()
lock = Lock()


def sell_seats(show_id: int, seats_count: int, seats_numbers: list) -> None:
    lock.acquire()

    show = shows_repo.get(show_id)
    sold_seats_to_show = sold_seats_repo.get_for_show(show_id)

    if show.room.seats_count < len(sold_seats_to_show):
        raise Exception('all seats taken')
    if seats_count > show.room.seats_count - len(sold_seats_to_show):
        raise Exception('not enough seats available')
    for wanted_seat_number in seats_numbers:
        for sold_seat in sold_seats_to_show:
            if wanted_seat_number == sold_seat.seat_number:
                raise Exception('seat already taken')

    sale_id = sales_repo.add(datetime.now(), show)
    sale = sales_repo.get(sale_id)
    for wanted_seat_number in seats_numbers:
        sold_seats_repo.add(wanted_seat_number, sale)

    lock.release()
