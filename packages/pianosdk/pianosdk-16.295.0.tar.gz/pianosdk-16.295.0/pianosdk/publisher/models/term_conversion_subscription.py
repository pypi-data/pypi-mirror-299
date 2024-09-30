from datetime import date, datetime
from pydantic.main import BaseModel
from typing import Optional
from pianosdk.publisher.models.resource import Resource
from pianosdk.publisher.models.term import Term
from pianosdk.publisher.models.user import User
from pianosdk.publisher.models.user_address import UserAddress


class TermConversionSubscription(BaseModel):
    subscription_id: Optional[str] = None
    auto_renew: Optional[bool] = None
    next_bill_date: Optional[datetime] = None
    payment_method: Optional[str] = None
    billing_plan: Optional[str] = None
    user_payment_info_id: Optional[str] = None
    status: Optional[str] = None
    status_name: Optional[str] = None
    status_name_in_reports: Optional[str] = None
    term: Optional['Term'] = None
    resource: Optional['Resource'] = None
    user: Optional['User'] = None
    start_date: Optional[datetime] = None
    cancelable: Optional[bool] = None
    user_address: Optional['UserAddress'] = None
    psc_subscriber_number: Optional[str] = None
    external_api_name: Optional[str] = None
    conversion_result: Optional[str] = None
    is_in_trial: Optional[bool] = None
    trial_period_end_date: Optional[datetime] = None
    trial_amount: Optional[float] = None
    trial_currency: Optional[str] = None
    end_date: Optional[datetime] = None
    charge_count: Optional[int] = None
    upi_ext_customer_id: Optional[str] = None
    upi_ext_customer_id_label: Optional[str] = None


TermConversionSubscription.model_rebuild()
