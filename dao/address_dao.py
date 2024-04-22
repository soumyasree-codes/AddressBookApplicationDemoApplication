import sqlite3
from model.address import Address


class AddressDAO:
    def __init__(self, db_file):
        self.db_file = db_file
        self.create_table()

    def create_table(self):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS addresses (
                    id INTEGER PRIMARY KEY,
                    street TEXT,
                    city TEXT,
                    state TEXT,
                    country TEXT,
                    postal_code TEXT,
                    latitude REAL,
                    longitude REAL
                )
            """)
            conn.commit()

    def add_address(self, address: Address):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO addresses (street, city, state, country, postal_code, latitude, longitude)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (address.street, address.city, address.state, address.country, address.postal_code,
                  address.latitude, address.longitude))
            conn.commit()
            return cursor.lastrowid

    def update_address(self, address_id: int, address: Address):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE addresses
                SET street=?, city=?, state=?, country=?, postal_code=?, latitude=?, longitude=?
                WHERE id=?
            """, (address.street, address.city, address.state, address.country, address.postal_code,
                  address.latitude, address.longitude, address_id))
            conn.commit()

    def delete_address(self, address_id: int):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM addresses WHERE id=?", (address_id,))
            conn.commit()

    def get_address_by_id(self, address_id: int) -> Address:
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM addresses WHERE id=?", (address_id,))
            row = cursor.fetchone()
            if row:
                return Address(id=row[0], street=row[1], city=row[2], state=row[3], country=row[4],
                               postal_code=row[5], latitude=row[6], longitude=row[7])

    def get_addresses_within_distance(self, latitude: float, longitude: float, distance: float):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM addresses
                WHERE (latitude - ?) * (latitude - ?) + (longitude - ?) * (longitude - ?) < ? * ?
            """, (latitude, latitude, longitude, longitude, distance, distance))
            rows = cursor.fetchall()
            return [Address(id=row[0], street=row[1], city=row[2], state=row[3], country=row[4],
                            postal_code=row[5], latitude=row[6], longitude=row[7]) for row in rows]
