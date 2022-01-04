from datetime import datetime


class Room:
    def __init__(self, room_id: int, seats_count: int):
        self.room_id = room_id
        self.seats_count = seats_count


class Show:
    def __init__(self, show_id: int, show_date: datetime, title: str, ticket_price: int,
                 room: Room, available_seats_count: int, balance: int):
        self.show_id = show_id
        self.show_date = show_date
        self.title = title
        self.ticket_price = ticket_price
        self.room = room
        self.available_seats_count = available_seats_count
        self.balance = balance


class Sale:
    def __init__(self, sale_id: int, sale_date: datetime, show: Show):
        self.sale_id = sale_id
        self.sale_date = sale_date
        self.show = show


class SoldSeat:
    def __init__(self, sold_seat_id: int, seat_number: int, sale: Sale):
        self.sold_seat_id = sold_seat_id
        self.seat_number = seat_number
        self.sale = sale
