import sqlite3
from datetime import datetime

from domain import Sale, Show, Room, SoldSeat


class SqliteRepository:
    def __init__(self):
        self._connection = sqlite3.connect('shows-app.db', check_same_thread=False)


class SqliteShowsRepository(SqliteRepository):
    def get(self, show_id: int) -> Show:
        try:
            row = self._connection.cursor().execute('''select * from shows sh
                                                       inner join rooms ro
                                                       on sh.room_id = ro.room_id
                                                       where sh.show_id = ?''',
                                                    (show_id,)).fetchone()
            return Show(
                row[0],
                row[1],
                row[2],
                row[3],
                Room(
                    row[5],
                    row[6]
                )
            )
        except Exception as e:
            raise Exception('error getting show')


class SqliteSalesRepository(SqliteRepository):
    def get(self, sale_id: int) -> Sale:
        try:
            row = self._connection.cursor().execute('''select * from sales sa
                                                       inner join shows sh
                                                       on sa.show_id = sh.show_id
                                                       inner join rooms ro
                                                       on sh.room_id = ro.room_id
                                                       where sa.sale_id = ?''',
                                                    (sale_id,)).fetchone()
            return Sale(
                row[0],
                row[1],
                Show(
                    row[3],
                    row[4],
                    row[5],
                    row[6],
                    Room(
                        row[7],
                        row[8]
                    )
                )
            )
        except Exception:
            raise Exception('error getting sale')

    def add(self, sale_date: datetime, show: Show) -> int:
        try:
            cursor = self._connection.cursor()
            cursor.execute(
                '''insert into sales(sale_date, show_id) values (?, ?)''',
                (sale_date, show.show_id)
            )
            self._connection.commit()
            return cursor.lastrowid
        except Exception:
            raise Exception('error adding sale')


class SqliteSoldSeatsRepository(SqliteRepository):
    def get_for_show(self, show_id: int) -> list:
        try:
            sold_seats = []
            for row in self._connection.cursor().execute('''select * from sold_seats so
                                                            inner join sales sa
                                                            on so.sale_id = sa.sale_id
                                                            inner join shows sh
                                                            on sa.show_id = sh.show_id
                                                            inner join rooms ro
                                                            on sh.room_id = ro.room_id
                                                            where sa.show_id = ?''',
                                                         (show_id,)).fetchall():
                sold_seats.append(
                    SoldSeat(
                        row[0],
                        row[1],
                        Sale(
                            row[3],
                            row[4],
                            Show(
                                row[6],
                                row[7],
                                row[8],
                                row[9],
                                Room(
                                    row[11],
                                    row[12]
                                )
                            )
                        )
                    )
                )
            return sold_seats
        except Exception:
            raise Exception(f'error getting sold seats for the ${show_id} show')

    def add(self, seat_number: int, sale: Sale) -> int:
        try:
            cursor = self._connection.cursor()
            cursor.execute(
                '''insert into sold_seats(seat_number, sale_id) values (?, ?)''',
                (seat_number, sale.sale_id)
            )
            self._connection.commit()
            return cursor.lastrowid
        except Exception:
            raise Exception('error adding sold seat')
