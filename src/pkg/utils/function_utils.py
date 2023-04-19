from typing import List, Callable, Dict


def call_queue(func_queue: List[Callable] = [], args_init: Dict = {}) -> Dict:
    input_curr = args_init.copy()
    for _callable in func_queue:
        output_curr = _callable(**input_curr)
        input_curr = output_curr or {}
    
    return input_curr
