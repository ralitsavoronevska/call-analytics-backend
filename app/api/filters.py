
from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import or_

from app.models.call_record import CallRecord


def build_call_filters(
    start_date: datetime | None = None,
    end_date: datetime | None = None,
    phone_number: str | None = None,
    city: str | None = None,
):
    if start_date and end_date and start_date > end_date:
        raise HTTPException(
            status_code=422,
            detail="start_date must be before or equal to end_date",
        )

    filters = []

    if start_date:
        filters.append(CallRecord.call_start_time >= start_date)

    if end_date:
        filters.append(CallRecord.call_start_time <= end_date)

    if phone_number:
        filters.append(
            or_(
                CallRecord.caller_number.contains(phone_number),
                CallRecord.receiver_number.contains(phone_number),
            )
        )

    if city:
        filters.append(CallRecord.city.ilike(f"%{city}%"))

    return filters
