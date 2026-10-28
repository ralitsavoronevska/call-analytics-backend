from datetime import datetime
from math import ceil
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.api.filters import build_call_filters
from app.models.call_record import CallRecord
from app.schemas.call_record import PaginatedCallsResponse
from app.api.dependencies import get_current_user


router = APIRouter(prefix="/api/calls", tags=["Calls"], dependencies=[Depends(get_current_user)],)

DbSession = Annotated[Session, Depends(get_db)]


@router.get("", response_model=PaginatedCallsResponse)
def get_calls(
    db: DbSession,
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=100)] = 20,
    start_date: datetime | None = None,
    end_date: datetime | None = None,
    phone_number: str | None = None,
    city: str | None = None,
):
    
    filters = build_call_filters(
        start_date=start_date,
        end_date=end_date,
        phone_number=phone_number,
        city=city,
    )

    total = db.scalar(
        select(func.count())
        .select_from(CallRecord)
        .where(*filters)
    ) or 0

    records = db.scalars(
        select(CallRecord)
        .where(*filters)
        .order_by(CallRecord.call_start_time.desc(), CallRecord.id.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    ).all()

    return PaginatedCallsResponse(
        items=records,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=ceil(total / page_size),
    )