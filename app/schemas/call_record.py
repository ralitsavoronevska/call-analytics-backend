from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class CallRecordResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    caller_name: str
    caller_number: str
    receiver_number: str
    city: str
    call_direction: bool
    call_status: bool
    call_duration: int
    call_cost: Decimal
    call_start_time: datetime
    call_end_time: datetime


class PaginatedCallsResponse(BaseModel):
    items: list[CallRecordResponse]
    total: int
    page: int
    page_size: int
    total_pages: int