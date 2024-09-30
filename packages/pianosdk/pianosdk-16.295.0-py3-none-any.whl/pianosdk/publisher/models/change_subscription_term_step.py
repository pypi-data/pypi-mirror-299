from datetime import date, datetime
from pydantic.main import BaseModel
from typing import Optional
from pianosdk.publisher.models.term_short import TermShort


class ChangeSubscriptionTermStep(BaseModel):
    from_term: Optional['TermShort'] = None
    to_term: Optional['TermShort'] = None
    optional: Optional[bool] = None
    enabled: Optional[bool] = None


ChangeSubscriptionTermStep.model_rebuild()
