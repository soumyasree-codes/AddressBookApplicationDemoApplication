import logging
from fastapi import FastAPI, HTTPException
from typing import List
from model.address import AddressRequest, AddressResponse
from service.address_service import AddressService

app = FastAPI()
address_service = AddressService("address_book.db")

logging.basicConfig(filename='app.log', level=logging.INFO)


@app.post("/address/", response_model=AddressResponse)
def create_address(address: AddressRequest):
    """
    Create a new address.

    Args:
        address (AddressRequest): Address data.

    Returns:
        AddressResponse: Created address data.
    """
    try:
        logging.info("Creating address.")
        created_address = address_service.add_address(address)
        logging.info(f"Address created: {created_address}")
        return created_address
    except Exception as e:
        logging.error(f"Error occurred while creating address: {str(e)}")
        raise HTTPException(status_code=500, detail="Error occurred while creating address")


@app.get("/addresses/", response_model=List[AddressResponse])
def get_all_addresses():
    """
    Get all addresses.

    Returns:
        List[AddressResponse]: List of all addresses.
    """
    try:
        logging.info("Fetching all addresses.")
        all_addresses = address_service.get_all_addresses()
        return all_addresses
    except Exception as e:
        logging.error(f"Error occurred while fetching all addresses: {str(e)}")
        raise HTTPException(status_code=500, detail="Error occurred while fetching all addresses")


@app.put("/address/{address_id}")
def update_address(address_id: int, address: AddressRequest):
    """
    Update an existing address by ID.

    Args:
        address_id (int): ID of the address to update.
        address (AddressRequest): Address data.

    Returns:
        dict: Success message.
    """
    try:
        logging.info(f"Updating address with ID {address_id}.")
        address_service.update_address(address_id, address)
        logging.info(f"Address with ID {address_id} updated successfully.")
        return {"message": "Address updated successfully"}
    except Exception as e:
        logging.error(f"Error occurred while updating address with ID {address_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Error occurred while updating address")


@app.delete("/address/{address_id}")
def delete_address(address_id: int):
    """
    Delete an address by ID.

    Args:
        address_id (int): ID of the address to delete.

    Returns:
        dict: Success message.
    """
    try:
        logging.info(f"Deleting address with ID {address_id}.")
        address_service.delete_address(address_id)
        logging.info(f"Address with ID {address_id} deleted successfully.")
        return {"message": "Address deleted successfully"}
    except Exception as e:
        logging.error(f"Error occurred while deleting address with ID {address_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Error occurred while deleting address")


@app.get("/address/{address_id}", response_model=AddressResponse)
def get_address(address_id: int):
    """
    Get an address by ID.

    Args:
        address_id (int): ID of the address to fetch.

    Returns:
        AddressResponse: Address data.
    """
    try:
        logging.info(f"Fetching address with ID {address_id}.")
        address = address_service.get_address_by_id(address_id)
        if not address:
            raise HTTPException(status_code=404, detail="Address not found")
        return address
    except Exception as e:
        logging.error(f"Error occurred while fetching address with ID {address_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Error occurred while fetching address")


@app.get("/addresses_within_distance/", response_model=List[AddressResponse])
def get_addresses_within_distance(latitude: float, longitude: float, distance: float):
    """
    Get addresses within a certain distance from a given location.

    Args:
        latitude (float): Latitude of the given location.
        longitude (float): Longitude of the given location.
        distance (float): Distance within which to search.

    Returns:
        List[AddressResponse]: List of addresses within the distance.
    """
    try:
        logging.info("Fetching addresses within distance.")
        addresses = address_service.get_addresses_within_distance(latitude, longitude, distance)
        return addresses
    except Exception as e:
        logging.error(f"Error occurred while fetching addresses within distance: {str(e)}")
        raise HTTPException(status_code=500, detail="Error occurred while fetching addresses within distance")

