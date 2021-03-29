import asyncio
import logging
from datetime import timedelta

logger = logging.getLogger(__name__)


class UptimeReporter:

    def __init__(self):
        self.seconds_up = 0.0
        self.uptime = timedelta(seconds=self.seconds_up)
        self.counter = 0

    async def report_continuously(self):
        while True:
            self.seconds_up = asyncio.get_event_loop().time()
            self.uptime = timedelta(seconds=self.seconds_up)
            self.counter += 1
            logger.info(f"Uptime report #{self.counter}: up for {self.uptime}")
            await asyncio.sleep(60)
