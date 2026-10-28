from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy import case, func, select
from sqlalchemy.orm import Session

from datetime import datetime
from app.db.session import get_db
from app.api.filters import build_call_filters
from app.models.call_record import CallRecord
from app.schemas.analytics import CallSummaryResponse, TopCallerItem, TopCallersResponse
from app.api.dependencies import get_current_user


router = APIRouter(prefix="/api/analytics", tags=["Analytics"], dependencies=[Depends(get_current_user)],)

DbSession = Annotated[Session, Depends(get_db)]


@router.get("/summary", response_model=CallSummaryResponse)
def get_call_summary(
    db: DbSession,
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
    statement = select(
        func.count(CallRecord.id).label("total_calls"),
        func.coalesce(
            func.sum(CallRecord.call_duration), 0
        ).label("total_duration_seconds"),
        func.coalesce(
            func.sum(CallRecord.call_cost), 0
        ).label("total_cost"),
        func.count(
            case((CallRecord.call_direction.is_(True), 1))
        ).label("direction_true"),
        func.count(
            case((CallRecord.call_direction.is_(False), 1))
        ).label("direction_false"),
        func.count(
            case((CallRecord.call_status.is_(True), 1))
        ).label("status_true"),
        func.count(
            case((CallRecord.call_status.is_(False), 1))
        ).label("status_false"),
    ).where(*filters)

    result = db.execute(statement).one()

    return CallSummaryResponse(
        total_calls=result.total_calls,
        total_duration_seconds=result.total_duration_seconds,
        total_cost=result.total_cost,
        direction_true=result.direction_true,
        direction_false=result.direction_false,
        status_true=result.status_true,
        status_false=result.status_false,
    )


@router.get("/top-callers", response_model=TopCallersResponse)
def get_top_callers(
    db: DbSession,
    limit: Annotated[int, Query(ge=1, le=100)] = 10,
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

    statement = (
        select(
            CallRecord.caller_number.label("caller_number"),
            func.count(CallRecord.id).label("total_calls"),
            func.coalesce(
                func.sum(CallRecord.call_duration), 0
            ).label("total_duration_seconds"),
            func.coalesce(
                func.sum(CallRecord.call_cost), 0
            ).label("total_cost"),
        )
        .where(*filters)
        .group_by(CallRecord.caller_number)
        .order_by(
            func.count(CallRecord.id).desc(),
            CallRecord.caller_number.asc(),
        )
        .limit(limit)
    )

    results = db.execute(statement).all()

    return TopCallersResponse(
        items=[
            TopCallerItem(
                caller_number=row.caller_number,
                total_calls=row.total_calls,
                total_duration_seconds=row.total_duration_seconds,
                total_cost=row.total_cost,
            )
            for row in results
        ]
    )
