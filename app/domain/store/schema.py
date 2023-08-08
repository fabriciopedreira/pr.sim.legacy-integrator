from random import randint
from typing import Dict

from pydantic import BaseModel


class Product(BaseModel):
    sku: str
    amount: int
    price_raw: float
    price: float
    discount_rate: float
    discount_inove_amount: float
    discount_solfacil_plus_amount: float
    total: float
    status: str


class Address(BaseModel):
    zipcode: str
    street: str
    number: str
    complement: str
    district: str
    city: str
    state: str


class Shipping(BaseModel):
    type: str
    delivery_rural_area: bool
    address: Address


class KitsPurchase(BaseModel):
    order_id: int
    items: list[Product]
    shipping: Shipping
    subtotal: float
    total: float
    power: float
    financing_id: int

    class Config:
        schema_extra = {
            "example": {
                "order_id": 12345,
                "items": [
                    {
                        "sku": "ITEM_SKU",
                        "amount": 1,
                        "price_raw": 0.0,
                        "price": 0.0,
                        "discount_rate": 0.0,
                        "discount_inove_amount": 0.0,
                        "discount_solfacil_plus_amount": 0.0,
                        "total": 0.0,
                        "status": "OK",
                    }
                ],
                "shipping": {
                    "type": "SHIPPING_TYPE",
                    "delivery_rural_area": False,
                    "address": {
                        "zipcode": "ZIP_CODE",
                        "street": "STREET_ADDRESS",
                        "number": "NUMBER",
                        "complement": "ADDRESS_COMPLEMENT",
                        "district": "DISTRICT",
                        "city": "CITY",
                        "state": "STATE",
                    },
                },
                "subtotal": 0.0,
                "total": 0.0,
                "power": 0.0,
                "financing_id": 678477,
            }
        }


class StoreResponse(BaseModel):
    data: Dict[str, str]
    error: str
    code: int

    class Config:
        schema_extra = {
            "example": {
                "data": {
                    "mensage": f"Receipt created for financing: {randint(1000, 9999)}",
                    "code": 201,
                    "error": False,
                }
            }
        }
