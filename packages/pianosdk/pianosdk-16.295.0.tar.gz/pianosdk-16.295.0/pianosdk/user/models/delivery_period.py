from datetime import date, datetime
from pydantic.main import BaseModel
from typing import Optional


class DeliveryPeriod(BaseModel):
    _from: Optional[str] = None
    to: Optional[str] = None
    delivery_period_pub_id: Optional[str] = None
    address_pub_id: Optional[str] = None


DeliveryPeriod.model_rebuild()
