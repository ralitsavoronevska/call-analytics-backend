from datetime import timezone
from decimal import Decimal
from pathlib import Path

import pandas as pd
from sqlalchemy import select, func

from app.db.session import engine
from app.models.call_record import CallRecord
from sqlalchemy.orm import Session


DATASET_PATH = Path("data/mock_call_records_10000.xlsx")

COLUMN_MAP = {
    "id": "id",
    "callerName": "caller_name",
    "callerNumber": "caller_number",
    "receiverNumber": "receiver_number",
    "city": "city",
    "callDirection": "call_direction",
    "callStatus": "call_status",
    "callDuration": "call_duration",
    "callCost": "call_cost",
    "callStartTime": "call_start_time",
    "callEndTime": "call_end_time",
}


def to_utc(value):
    timestamp = pd.Timestamp(value)

    if timestamp.tzinfo is None:
        # The source timestamps use the UTC "Z" convention.
        return timestamp.to_pydatetime().replace(tzinfo=timezone.utc)

    return timestamp.tz_convert("UTC").to_pydatetime()


def main():
    if not DATASET_PATH.is_file():
        raise FileNotFoundError(DATASET_PATH)

    df = pd.read_excel(
        DATASET_PATH,
        dtype={
            "callerNumber": str,
            "receiverNumber": str,
        },
    )

    missing = set(COLUMN_MAP) - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")

    if df[list(COLUMN_MAP)].isna().any().any():
        raise ValueError("Dataset contains missing values")

    if df["id"].duplicated().any():
        raise ValueError("Dataset contains duplicate IDs")

    if len(df) != 10_000:
        raise ValueError(f"Expected 10000 rows, got {len(df)}")

    records = []

    for row in df.to_dict(orient="records"):
        record = {
            target: row[source]
            for source, target in COLUMN_MAP.items()
        }

        record["id"] = int(record["id"])
        record["call_duration"] = int(record["call_duration"])
        record["call_cost"] = Decimal(str(record["call_cost"]))

        for field in ("call_direction", "call_status"):
            value = record[field]
            if not isinstance(value, bool):
                raise ValueError(f"Invalid boolean: {field}={value!r}")

        record["call_start_time"] = to_utc(
            record["call_start_time"]
        )
        record["call_end_time"] = to_utc(
            record["call_end_time"]
        )

        records.append(record)

    with Session(engine) as session:
        existing_ids = set(
            session.scalars(select(CallRecord.id)).all()
        )

        new_records = [
            record
            for record in records
            if record["id"] not in existing_ids
        ]

        if new_records:
            session.bulk_insert_mappings(CallRecord, new_records)
            session.commit()

        total = session.scalar(
            select(func.count()).select_from(CallRecord)
        )

    print(f"Dataset rows: {len(records)}")
    print(f"New records imported: {len(new_records)}")
    print(f"Records already present: {len(records) - len(new_records)}")
    print(f"Total database records: {total}")


if __name__ == "__main__":
    main()