from pydantic import BaseModel, confloat


class AddressRequest(BaseModel):
    street: str
    city: str
    state: str
    country: str
    postal_code: str
    latitude: confloat(ge=-90, le=90)
    longitude: confloat(ge=-180, le=180)


class AddressResponse(AddressRequest):
    id: int
