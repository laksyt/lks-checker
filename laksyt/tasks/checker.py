import asyncio
import logging
from asyncio import TimeoutError

from aiohttp import ClientError, ClientSession, ClientTimeout, TraceConfig
from kafka import KafkaProducer
from kafka.errors import KafkaError

from laksyt.entities.http.schedule import Schedule
from laksyt.entities.http.timer import create_request_timer
from laksyt.entities.report import HealthReport, compose_failure_report, compose_success_report, compose_timeout_report
from laksyt.entities.target import TargetWrapper

logger = logging.getLogger(__name__)


class HealthChecker:
    """Main asynchronous workload

    Periodically launches a round of health checks against the configured
    targets, composes reports, and enqueues them onto a Kafka topic
    """

    def __init__(
            self,
            targets: tuple[TargetWrapper],
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
        """Repeatedly (with delay) performs rounds of health checks"""
        while True:
            await self.check_once()
            await asyncio.sleep(self._schedule.delay)

    async def check_once(self):
        """Performs single round of health checks against all targets"""
        async with self._create_session() as session:
            tasks = []
            for target in self._targets:
                tasks.append(
                    self._check_target(target, session)
                )
            await asyncio.gather(*tasks)

    def _create_session(self) -> ClientSession:
        """Instantiates an aiohttp client session"""
        return ClientSession(
            trace_configs=[self._request_timer],
            timeout=ClientTimeout(total=self._schedule.timeout)
        )

    async def _check_target(
            self,
            target: TargetWrapper,
            session: ClientSession
    ) -> None:
        """Performs health check against a single target and sends report to
        Kafka topic
        """
        report = await self._do_health_check(target, session)
        if report:
            await self._do_send(report)

    async def _do_health_check(
            self,
            target: TargetWrapper,
            session: ClientSession
    ) -> HealthReport:
        """Performs health check against a single target and returns report"""
        target, matcher = target.target, target.needle_is_in
        try:
            response = await session.request(method="GET", url=target.url)
            html = await response.text()
            report = compose_success_report(target, response, matcher(html))
        except ClientError as error:
            report = compose_failure_report(target, error)
        except TimeoutError:
            report = compose_timeout_report(target, self._schedule.timeout)
        logger.info(f"Health checked: {report.status:>12.12}, {report}")
        return report

    async def _do_send(self, report: HealthReport) -> bool:
        """Sends given health check report to Kafka topic, returns whether
        report was accepted by Kafka producer (does not guarantee sending and
        delivery)
        """
        enqueued = False
        try:
            self._kafka_producer.send(self._kafka_topic, report.serialize())
            enqueued = True
        except KafkaError:
            logger.exception(f"Failed to enqueue {report} due to Kafka error")
        return enqueued
