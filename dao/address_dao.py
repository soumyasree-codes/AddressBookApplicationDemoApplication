import sqlite3
from model.address import AddressRequest, AddressResponse
from typing import List


class AddressDAO:
    def __init__(self, db_file):
        self.db_file = db_file
        self.create_table()

    def execute_query(self, query, values=None, commit=False):
        with sqlite3.connect(self.db_file) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            if values:
                cursor.execute(query, values)
            else:
                cursor.execute(query)
            if commit:
                conn.commit()
                return cursor.lastrowid
            else:
                return cursor

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

    def get_all_addresses(self) -> List[AddressResponse]:
        query = "SELECT * FROM addresses"
        rows = self.execute_query(query).fetchall()
        addresses = []
        for row in rows:
            address = AddressResponse(
                id=row[0], street=row[1], city=row[2], state=row[3], country=row[4],
                postal_code=row[5], latitude=row[6], longitude=row[7]
            )
            addresses.append(address)
        return addresses

    def add_address(self, address: AddressRequest) -> AddressResponse:
        query = """
            INSERT INTO addresses (street, city, state, country, postal_code, latitude, longitude)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        values = (address.street, address.city, address.state, address.country,
                  address.postal_code, address.latitude, address.longitude)
        address_id = self.execute_query(query, values, commit=True)
        return AddressResponse(id=address_id, **address.dict())

    def update_address(self, address_id: int, address: AddressRequest):
        query = """
            UPDATE addresses
            SET street=?, city=?, state=?, country=?, postal_code=?, latitude=?, longitude=?
            WHERE id=?
        """
        values = (address.street, address.city, address.state, address.country,
                  address.postal_code, address.latitude, address.longitude, address_id)
        self.execute_query(query, values, commit=True)

    def delete_address(self, address_id: int):
        query = "DELETE FROM addresses WHERE id=?"
        self.execute_query(query, (address_id,), commit=True)

    def get_address_by_id(self, address_id: int) -> AddressResponse:
        query = "SELECT * FROM addresses WHERE id=?"
        row = self.execute_query(query, (address_id,)).fetchone()
        if row:
            return AddressResponse(id=row[0], street=row[1], city=row[2], state=row[3], country=row[4],
                                   postal_code=row[5], latitude=row[6], longitude=row[7])

    def get_addresses_within_distance(self, latitude: float,
                                      longitude: float, distance: float) -> List[AddressResponse]:
        query = """
            SELECT * FROM addresses
            WHERE (latitude - ?) * (latitude - ?) + (longitude - ?) * (longitude - ?) < ? * ?
        """
        values = (latitude, latitude, longitude, longitude, distance, distance)
        rows = self.execute_query(query, values).fetchall()
        addresses = []
        for row in rows:
            address = AddressResponse(
                id=row[0], street=row[1], city=row[2], state=row[3], country=row[4],
                postal_code=row[5], latitude=row[6], longitude=row[7]
            )
            addresses.append(address)
        return addresses
