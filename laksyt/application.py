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
    """Main class of the application

    With a given configuration, sets up logging, retrieves event loop, and
    deploys long-running tasks into it.
    """

    def __init__(self, config: Config):
        """Configures application, prepares tasks"""
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
        """Kicks off the main workload"""
        workload = self.loop.create_task(self._workload())
        try:
            self.loop.run_until_complete(workload)
        except asyncio.CancelledError:
            self.logger.exception("Workload was unexpectedly cancelled")
        except KeyboardInterrupt:
            self.logger.warning("Interrupting workload")
        except BaseException:
            self.logger.exception("Shutting down workload due to exception")
        finally:
            self._clean_up()

    async def _workload(self):
        """Groups long-running asynchronous tasks into a single workload"""
        await asyncio.gather(
            self.uptime_reporter.report_continuously(),
            self.health_checker.check_continuously()
        )

    def _clean_up(self):
        """Gracefully shut down asynchronous activity"""
        try:
            self._cancel_tasks()
            self.loop.run_until_complete(self.loop.shutdown_asyncgens())
            self.loop.run_until_complete(self.loop.shutdown_default_executor())
        finally:
            self.logger.info("Closing event loop")
            self.loop.close()

    def _cancel_tasks(self):
        """Make sure all asynchronous tasks that are still running are
        cancelled and know about it
        """
        tasks = asyncio.all_tasks(self.loop)
        if not tasks:
            self.logger.info("All tasks completed")
            return
        self.logger.info("Cancelling remaining tasks")
        for task in tasks:
            self.logger.info(f"Cancelling {task.get_coro()}")
            task.cancel()
        try:
            self.loop.run_until_complete(
                asyncio.gather(*tasks, return_exceptions=True)
            )
        except KeyboardInterrupt:
            pass
        for task in tasks:
            if task.cancelled() or task.exception() is not None:
                continue
