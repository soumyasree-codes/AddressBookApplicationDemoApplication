from fastapi import FastAPI, HTTPException
from model.address import Address
from service.address_service import AddressService

app = FastAPI()
address_service = AddressService("address_book.db")


@app.post("/address/")
def create_address(address: Address):
    address_id = address_service.add_address(address)
    return {"id": address_id}


@app.put("/address/{address_id}")
def update_address(address_id: int, address: Address):
    if not address_service.get_address_by_id(address_id):
        raise HTTPException(status_code=404, detail="Address not found")
    address_service.update_address(address_id, address)
    return {"message": "Address updated successfully"}


@app.delete("/address/{address_id}")
def delete_address(address_id: int):
    if not address_service.get_address_by_id(address_id):
        raise HTTPException(status_code=404, detail="Address not found")
    address_service.delete_address(address_id)
    return {"message": "Address deleted successfully"}


@app.get("/address/{address_id}")
def get_address(address_id: int):
    address = address_service.get_address_by_id(address_id)
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")
    return address


@app.get("/addresses_within_distance/")
def get_addresses_within_distance(latitude: float, longitude: float, distance: float):
    addresses = address_service.get_addresses_within_distance(latitude, longitude, distance)
    return addresses