from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional

from aiohttp import ClientError, ClientResponse
from dataclasses_avroschema import AvroModel

from laksyt.entities.target import Target


def _utcnow_truncated():
    ts = datetime.now(tz=timezone.utc)
    return ts.replace(microsecond=int(f"{str(ts.microsecond)[:3]}000"))


@dataclass
class HealthReport(AvroModel):
    target: Target
    is_available: bool
    status: str
    status_code: Optional[int] = None
    response_time: Optional[float] = None
    needle_found: Optional[bool] = None
    checked_at: datetime = field(default_factory=_utcnow_truncated, init=False)


def compose_success_report(
        target: Target,
        response: ClientResponse,
        html: str
) -> HealthReport:
    return HealthReport(
        target=target,
        status=map_code_to_status(response.status),
        is_available=True,
        status_code=response.status,
        response_time=response.time,
        needle_found=target.needle in html if target.needle else None
    )


def compose_failure_report(
        target: Target,
        error: ClientError
) -> HealthReport:
    return HealthReport(
        target=target,
        status='UNAVAILABLE',
        is_available=False,
        response_time=error.time
    )


def compose_timeout_report(
        target: Target,
        timeout_secs: int
) -> HealthReport:
    return HealthReport(
        target=target,
        status='TIMEOUT',
        is_available=False,
        response_time=float(timeout_secs)
    )


def map_code_to_status(http_code: int):
    if 100 <= http_code <= 199:
        return 'INFO'
    elif 200 <= http_code <= 299:
        return 'SUCCESS'
    elif 300 <= http_code <= 399:
        return 'REDIRECT'
    elif 400 <= http_code <= 499:
        return 'CLIENT_ERROR'
    elif 500 <= http_code <= 599:
        return 'SERVER_ERROR'
    else:
        return 'OTHER'
