from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from aiohttp import ClientError, ClientResponse
from dataclasses_avroschema import AvroModel

from checker.entities.http.targets import Target


@dataclass
class HealthReport(AvroModel):
    target: Target
    status: str
    is_available: bool
    status_code: Optional[int] = None
    response_time: Optional[float] = None
    needle_found: Optional[bool] = None
    checked_at: datetime = field(default_factory=datetime.utcnow, init=False)


def compose_success_report(
        target: Target,
        response: ClientResponse,
        html: str
) -> HealthReport:
    return HealthReport(
        target=target,
        status=map_code_to_hr_status(response.status),
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


def map_code_to_hr_status(http_code: int):
    if 200 <= http_code <= 299:
        return 'SUCCESS'
    elif 400 <= http_code <= 599:
        return 'ERROR'
    else:
        return 'OTHER'
