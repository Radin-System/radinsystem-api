import logging
from ._base import Job

logger = logging.getLogger(__name__)

class AMIToCTI(Job):
    def run(self) -> None:
        ...