from pydantic import BaseModel


class Address(BaseModel):
    id: int
    street: str
    city: str
    state: str
    country: str
    postal_code: str
    latitude: float
    longitude: float
