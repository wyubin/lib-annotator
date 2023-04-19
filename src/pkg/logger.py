import logging
import sys
import uuid
from typing import Dict, List, Generator
import time


def new_logger(level: int = logging.INFO, name: str = None, handlers: List = [logging.StreamHandler(sys.stderr)], formatter_class=logging.Formatter('%(levelname)-8s %(message)s')):
    "return a logger"
    logger = logging.getLogger(name or str(uuid.uuid4()))
    logger.setLevel(level)
    for handler in handlers:
        handler.setFormatter(formatter_class)
        logger.addHandler(handler)

    return logger


# timer
class Timer():

    def __init__(self):
        self.name2timer: Dict[str, List[float]] = {}

    def start(self, name: str) -> float:
        current = time.time()
        self.name2timer[name] = [current]
        return current

    def stop(self, name: str) -> float:
        if len(self.name2timer[name]) == 0:
            return None
        current = time.time()
        self.name2timer[name] = [self.name2timer[name][0], current]
        return current

    def count(self, name: str) -> float:
        if len(self.name2timer[name]) != 2:
            self.stop(name)
        start, stop = self.name2timer[name]
        return stop - start

    def log(self, name: str, fmt: str = 'processed[%(tag)s] need time: %(time).2f min') -> str:
        interval = self.count(name)
        return fmt % {'tag': name, 'time': interval/60}


# log args
def args_format(args: Dict, fmt: str = '--%(key)s: %(val)s') -> Generator[str, None, None]:
    for key, val in args.items():
        if val is None:
            continue
        yield fmt % {'key': key, 'val': val}
