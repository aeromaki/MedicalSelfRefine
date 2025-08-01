from multiprocessing import Queue, Process
import json

from langchain_core.runnables.base import Runnable
from tqdm import tqdm

from visbox.datatypes import AutoLabelFormat, LabelResult
from visbox.utils import result_fmt, track_cost
from .results import gen_result_from_output
from .langchain import create_model


@track_cost
def batch(model: Runnable, data: list[AutoLabelFormat]) -> list[LabelResult]:
    return list(map(
                lambda x: gen_result_from_output(x[0], x[1].content), 
                zip(data, model.batch(data))
                ))


def autolabel(
        model: Runnable,
        tgt: str,
        logs: list[list[AutoLabelFormat]],
        ) -> float:
    b = []
    c = 0
    for i, l in enumerate(logs): #tqdm(logs):
        results, cost = batch(model, l)
        b.append(results)
        print(f"{tgt} {i} cost: {cost}")
        c += cost
    file_path = result_fmt(tgt)    
    json.dump(b, open(file_path, 'w'), indent=2)
    return c


def autolabel_all(
        model: Runnable,
        logs: dict[str, list[list[AutoLabelFormat]]],
        ) -> None:
    c = 0
    for tgt, l in tqdm(logs.items()):
        c += autolabel(model, tgt, l)
    print(f"total cost: {c}")


def autolabel_process(
        queue: Queue,
        model_config: dict,
        tgt: str,
        logs: list[list[AutoLabelFormat]],
        ) -> None:
    model = create_model(**model_config)
    cost = autolabel(
                model,
                tgt,
                logs
                )
    queue.put(cost)

def autolabel_all_multiprocessing(
        model_config: dict,
        logs: dict[str, list[list[AutoLabelFormat]]],
        ) -> None:
    queue = Queue()
    queue.cancel_join_thread()

    for tgt, l in logs.items():
        p = Process(
                target=autolabel_process, 
                args=(queue, model_config, 
                tgt, 
                l
                ))
        p.start()
    
    c = 0
    for _ in tqdm(range(len(logs))):
        c += queue.get()
    print(f"total cost: {c}")   
