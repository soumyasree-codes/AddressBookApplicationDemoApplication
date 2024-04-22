from model.address import Address
from dao.address_dao import AddressDAO


class AddressService:
    def __init__(self, db_file):
        self.dao = AddressDAO(db_file)

    def add_address(self, address: Address):
        return self.dao.add_address(address)

    def update_address(self, address_id: int, address: Address):
        self.dao.update_address(address_id, address)

    def delete_address(self, address_id: int):
        self.dao.delete_address(address_id)

    def get_address_by_id(self, address_id: int) -> Address:
        return self.dao.get_address_by_id(address_id)

    def get_addresses_within_distance(self, latitude: float, longitude: float, distance: float):
        return self.dao.get_addresses_within_distance(latitude, longitude, distance)
