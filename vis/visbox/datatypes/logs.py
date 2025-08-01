from typing import Any, TypedDict, TypeVar, Generic

class GenerationInput(TypedDict):
    question: str
    options: str

class GenerationIterationCriticResponse(TypedDict):
    response: str

class GenerationIterationOutput(TypedDict):
    critic_response: GenerationIterationCriticResponse
    refiner_response: str
    refiner_prediction: str
    critic_cost: float
    refiner_cost: float

class GenerationOutput(TypedDict):
    initial_response: str
    initial_prediction: str
    initial_cost: float
    iteration: list[GenerationIterationOutput]

class GenerationError(TypedDict):
    error: Any


_GenerationOutput = TypeVar("_GenerationOutput")

class Generation_[_GenerationOutput](TypedDict):
    input: GenerationInput
    label: str
    output: _GenerationOutput
    result: list[bool]
    cost: float

type GenerationRaw = Generation_[GenerationOutput | GenerationError]

class GenerationWithId_[_GenerationOutput](Generation_[_GenerationOutput]):
    id: int

type GenerationSuccess = GenerationWithId_[GenerationOutput]
type GenerationFailed = GenerationWithId_[GenerationError]
type Generation = GenerationSuccess | GenerationFailed


class ResultDict(TypedDict):
    config: dict
    final_score: list[float]
    total_cost: float
    generations: list[GenerationRaw]
