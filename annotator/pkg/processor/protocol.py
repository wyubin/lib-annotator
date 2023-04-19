from typing import List, Dict, Generator, Callable
import sys
from pathlib import Path

path_script = Path(__file__)
sys.path.append(path_script.parent.parent.parent.__str__())

from pkg.utils.function_utils import call_queue


class Protocol_processor:
    def __init__(self, **kwargs):
        # init var
        self.protocol2info: Dict = {}
        # prepare list
        self.queue_setUp,  self.queue_run = [], []
        self.init_args(kwargs)

    def init_args(self, kwargs: Dict):
        for _key, _val in kwargs.items():
            setattr(self, _key, _val)

    def setUp(self, **kwargs):
        return call_queue(self.queue_setUp, kwargs)

    def append_setUp(self, *funcs: List[Callable]):
        for func in funcs:
            if callable(func):
                self.queue_setUp.append(func)

    def run(self, **kwargs):
        return call_queue(self.queue_run, kwargs)

    def append_run(self, *funcs: List[Callable]):
        for func in funcs:
            if callable(func):
                self.queue_run.append(func)

    def prepare_generator(self, **kwargs: Dict):
        return kwargs

    def output_processor(self, **kwargs: Dict) -> (List[str], Generator):
        return self.prepare_generator(**kwargs)
