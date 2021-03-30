import asyncio
import logging
from datetime import timedelta

logger = logging.getLogger(__name__)


class UptimeReporter:
    """Asynchronous workload to periodically report uptime into log"""

    def __init__(self, period: int = 60):
        """Sets up uptime reporting period in seconds"""
        self.period = period
        self.seconds_up = 0.0
        self.uptime = timedelta(seconds=self.seconds_up)
        self.counter = 0

    async def report_continuously(self):
        while True:
            await self.report_once()
            await asyncio.sleep(self.period)

    async def report_once(self):
        self.seconds_up = asyncio.get_event_loop().time()
        self.uptime = timedelta(seconds=self.seconds_up)
        self.counter += 1
        logger.info(f"Uptime report #{self.counter}: up for {self.uptime}")
