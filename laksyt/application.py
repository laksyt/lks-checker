import asyncio
import logging

from laksyt.config.config import Config
from laksyt.entities.http.schedule import get_schedule
from laksyt.entities.kafka.producer import get_kafka_producer
from laksyt.entities.kafka.topic import get_kafka_topic
from laksyt.entities.target import get_targets
from laksyt.logging import configure_logging
from laksyt.tasks.checker import HealthChecker
from laksyt.tasks.uptime import UptimeReporter


class Application:
    """Main entrypoint into the application

    Performs config duties, bootstraps the application, and exposes methods to
    launch the main process.
    """

    def __init__(self, config: Config):
        configure_logging(config)
        self.logger = logging.getLogger(__name__)
        self.config = config
        self.loop = asyncio.get_event_loop()

        self.uptime_reporter = UptimeReporter()
        self.health_checker = HealthChecker(
            get_targets(config),
            get_schedule(config),
            get_kafka_producer(config),
            get_kafka_topic(config)
        )

    def launch(self):
        self.loop.create_task(self._workload())
        try:
            self.loop.run_forever()
        except asyncio.CancelledError:
            self.logger.warning("Cancelling event loop")
        except KeyboardInterrupt:
            self.logger.warning("Interrupting event loop")

    async def _workload(self):
        await asyncio.gather(
            self.uptime_reporter.report_continuously(),
            self.health_checker.check_continuously()
        )
