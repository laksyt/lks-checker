import asyncio
from asyncio import Future
from asyncio.events import AbstractEventLoop

from checker.logging import configure_logging
from checker.startup.config import Config


class Application:
    """Main entrypoint into the application

    Performs startup duties, bootstraps the application, and exposes methods to
    launch the main process.
    """

    config: Config = None
    _event_loop: AbstractEventLoop = None
    _task: Future = None
    counter = 0

    def __init__(self, config: Config):
        configure_logging(config)
        self.config = config
        self._event_loop = asyncio.get_event_loop()

    def launch(self):
        print(self.config["test"]["message"])
        loop = self._event_loop
        loop.call_later(5, self.stop)
        self._task = loop.create_task(self.periodic())
        try:
            loop.run_until_complete(self._task)
        except asyncio.CancelledError:
            print("Cancelling")
        except KeyboardInterrupt:
            print("Interrupting")

    async def periodic(self):
        while True:
            self.counter += 1
            print(f"Counting {self.counter}")
            await asyncio.sleep(1)

    def stop(self):
        self._task.cancel()
