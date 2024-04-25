import logging
from fastapi import HTTPException
from model.address import AddressRequest, AddressResponse
from dao.address_dao import AddressDAO
from pydantic import ValidationError
from typing import List

logging.basicConfig(filename='app.log', level=logging.INFO)


class AddressService:
    def __init__(self, db_file):
        self.dao = AddressDAO(db_file)

    def add_address(self, address: AddressRequest) -> AddressResponse:
        try:
            logging.info(f"Entered in add_address function service layer!")
            new_address = self.dao.add_address(address)
            return new_address
        except ValidationError as e:
            raise HTTPException(status_code=422, detail=e.errors())

    def get_all_addresses(self) -> List[AddressResponse]:
        try:
            logging.info(f"Entered in get_all_addresses function service layer!")
            return self.dao.get_all_addresses()
        except ValidationError as e:
            raise HTTPException(status_code=422, detail=e.errors())

    def update_address(self, address_id: int, address: AddressRequest) -> None:
        try:
            logging.info(f"Entered in update_address function service layer!")
            self.dao.update_address(address_id, address)
        except ValidationError as e:
            raise HTTPException(status_code=422, detail=e.errors())

    def delete_address(self, address_id: int) -> None:
        try:
            self.dao.delete_address(address_id)
        except ValidationError as e:
            raise HTTPException(status_code=422, detail=e.errors())

    def get_address_by_id(self, address_id: int) -> AddressResponse:
        try:
            logging.info(f"Entered in fetching address with ID {address_id} in service layer")
            address = self.dao.get_address_by_id(address_id)
            if not address:
                return None
            return address
        except ValidationError as e:
            raise HTTPException(status_code=422, detail=e.errors())

    def get_addresses_within_distance(self, latitude: float, longitude: float, distance: float) -> List[
        AddressResponse]:
        try:
            logging.info(f"Entered in fetching address with distance latitude: {latitude}. longitude: {longitude}, "
                         f"distance: {distance} in service layer")
            addresses = self.dao.get_addresses_within_distance(latitude, longitude, distance)
            return addresses
        except ValidationError as e:
            raise HTTPException(status_code=422, detail=e.errors())
