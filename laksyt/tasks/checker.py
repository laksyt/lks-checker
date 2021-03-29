import asyncio
import logging
from asyncio import TimeoutError

from aiohttp import ClientError, ClientSession, ClientTimeout, TraceConfig
from kafka import KafkaProducer
from kafka.errors import KafkaError

from laksyt.entities.http.schedule import Schedule
from laksyt.entities.http.timer import create_request_timer
from laksyt.entities.report import HealthReport, compose_failure_report, compose_success_report, compose_timeout_report
from laksyt.entities.target import Target

logger = logging.getLogger(__name__)


class HealthChecker:

    def __init__(
            self,
            targets: tuple[Target],
            schedule: Schedule,
            kafka_producer: KafkaProducer,
            kafka_topic: str
    ):
        self._targets = targets
        self._schedule = schedule
        self._kafka_producer = kafka_producer
        self._kafka_topic = kafka_topic
        self._request_timer: TraceConfig = create_request_timer()

    async def check_continuously(self):
        while True:
            await self._check()
            await asyncio.sleep(self._schedule.delay)

    async def _check(self):
        async with self._create_session() as session:
            tasks = []
            for target in self._targets:
                tasks.append(
                    self._check_target(target, session)
                )
            await asyncio.gather(*tasks)

    def _create_session(self) -> ClientSession:
        return ClientSession(
            trace_configs=[self._request_timer],
            timeout=ClientTimeout(total=self._schedule.timeout)
        )

    async def _check_target(self, target: Target, session: ClientSession):
        """Sends request to a given Target and generates HealthReport."""
        report = await self._do_health_check(target, session)
        if report:
            await self._do_send(report)

    async def _do_health_check(self, target: Target, session: ClientSession) \
            -> HealthReport:
        report = None
        try:
            response = await session.request(method="GET", url=target.url)
            html = await response.text()
            report = compose_success_report(target, response, html)
        except ClientError as error:
            report = compose_failure_report(target, error)
        except TimeoutError:
            report = compose_timeout_report(target, self._schedule.timeout)
        except BaseException:
            logger.exception(
                "Unexpected error occurred while performing health check"
                f" on {target}"
            )
        if report:
            logger.info(f"Health checked: {report.status:>12.12}, {report}")
        else:
            logger.error(f"Failed to generate health report for {target}")
        return report

    async def _do_send(self, report: HealthReport) -> bool:
        enqueued = False
        kafka_producer = self._kafka_producer
        kafka_topic = self._kafka_topic
        try:
            kafka_producer.send(kafka_topic, report.serialize())
            enqueued = True
        except KafkaError:
            logger.exception(
                f"Failed to enqueue {report} due to Kafka error"
            )
        except BaseException:
            logger.exception(
                f"Unexpected error occurred while sending {report}"
            )
        return enqueued
