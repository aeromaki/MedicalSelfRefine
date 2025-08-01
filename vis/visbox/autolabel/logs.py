from typing import cast, Callable, Iterable

from visbox.datatypes import *
from visbox.utils import load_json, log_fmt


def conv_gen_to_autofmt(generation: GenerationSuccess, n: int)\
        -> AutoLabelFormat:
    output = generation['output']
    if n > 0:
        response = output['iteration'][n - 1]['refiner_response']
        prediction = output['iteration'][n - 1]['refiner_prediction']
    else:
        response = output['initial_response']
        prediction = output['initial_prediction']
    
    return {
        "id": generation['id'],
        "question": generation['input']['question'],
        "options": generation['input']['options'],
        "response": response,
        "prediction": prediction,
        "label": generation['label']
        }


def conv_gens_to_autofmt(generations: list[Generation], n: int)\
        -> list[AutoLabelFormat]:
    _f_filter: Callable[[Generation], bool]\
            = lambda x: not x['result'][n]\
            and 'initial_response' in x['output']
    
    if n > 0:
        f_filter = lambda x: _f_filter(x)\
                and (len(
                    cast(GenerationSuccess, x)
                    ['output']['iteration'][n - 1]['refiner_response']) > 1)
    else:
        f_filter = _f_filter
    
    f = cast(Iterable[GenerationSuccess], filter(f_filter, generations))
    return list(map(lambda x: conv_gen_to_autofmt(x, n), f))


def insert_ids(log_dict: list[GenerationRaw]) -> list[Generation]:
    return [cast(Generation, { "id": i, **d }) for i, d in enumerate(log_dict)]


def get_autofmts(result_dict: ResultDict, n_iter: int = 2)\
        -> list[list[AutoLabelFormat]]:
    generations = insert_ids(result_dict['generations'])
    return [conv_gens_to_autofmt(generations, i) for i in range(n_iter + 1)]


def load_model_logs(
        model_list: list[str], 
        ) -> dict[str, list[list[AutoLabelFormat]]]:
    logs = {}
    for m in model_list:
        file_path = log_fmt(m)
        result_dict = load_json(file_path)
        autofmts = get_autofmts(result_dict)
        logs[m] = autofmts
    return logs
