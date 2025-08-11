import logging, threading
from typing import List, ClassVar

logger = logging.getLogger()

class JobRegistry:
    _jobs: ClassVar[List['Job']] = []

    @classmethod
    def start_all(cls) -> None:
        logger.info(f'Starting all jobs: {len(cls._jobs)}')
        for job in cls._jobs:
            logger.info(f'Starting: {job.__class__.__name__}')
            job.start()

    @classmethod
    def stop_all(cls) -> None:
        logger.info(f'Stopping all jobs: {len(cls._jobs)}')
        for job in cls._jobs:
            logger.info(f'Stopping: {job.__class__.__name__}')
            job.stop()


class Job:
    def __init__(self, interval: float = 300, timeout: float = 3) -> None:
        """
        :param interval: Time in seconds between runs.
        :param timeout: Max time to wait for thread to join on stop.
        """
        self.interval = interval
        self.timeout = timeout

        self._sleeping = False
        self._active = False
        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self._thread = threading.Thread(target=self._loop, daemon=True)

        JobRegistry._jobs.append(self)

    def run(self) -> None:
        """Override this method with the job's task."""
        raise NotImplementedError

    def _loop(self) -> None:
        while not self._stop_event.is_set():
            try:
                self._sleeping = False
                self.run()
            except Exception as e:
                # Optionally log exceptions here
                logger.error(f'Error executing job({self.__class__.__name__}): {repr(e)}')
            finally:
                if self._stop_event.is_set():
                    break
                self._sleeping = True
                self._stop_event.wait(self.interval)  # sleep but wake early if stopped

    def start(self) -> None:
        with self._lock:
            if self._active:
                return
            self._active = True
            self._stop_event.clear()
            if not self._thread.is_alive():
                self._thread = threading.Thread(target=self._loop, daemon=True)
                self._thread.start()

    def stop(self) -> None:
        with self._lock:
            if not self._active:
                return
            self._active = False
            self._stop_event.set()
        self._thread.join(timeout=self.timeout)
