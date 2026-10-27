from decimal import Decimal

from pydantic import BaseModel


class CallSummaryResponse(BaseModel):
    total_calls: int
    total_duration_seconds: int
    total_cost: Decimal
    direction_true: int
    direction_false: int
    status_true: int
    status_false: int


class TopCallerItem(BaseModel):
    caller_number: str
    total_calls: int
    total_duration_seconds: int
    total_cost: Decimal


class TopCallersResponse(BaseModel):
    items: list[TopCallerItem]
