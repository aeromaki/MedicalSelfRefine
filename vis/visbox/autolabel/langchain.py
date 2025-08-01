import os

from visbox.utils import load_json

from langchain_core.prompts import (
    ChatPromptTemplate, 
    FewShotChatMessagePromptTemplate
    )
from langchain_core.runnables.base import Runnable
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv


ChatOpenAIConfig = dict


_PROMPT_PATH = os.path.join(
    os.path.abspath(os.path.dirname(__file__)),
    "prompt.json"
    )


def load_chat_prompt_template_json() -> ChatPromptTemplate:
    json_ = load_json(_PROMPT_PATH)

    example_prompt = ChatPromptTemplate.from_messages([
        ("user", json_["input_template"]),
        ("assistant", "{output}")
        ])
    few_shot_prompt = FewShotChatMessagePromptTemplate(
        example_prompt = example_prompt,
        examples=json_['examples']
        )

    return ChatPromptTemplate.from_messages([
        ("system", json_["system_prompt"]),
        few_shot_prompt,
        ("user", json_["input_template"])
        ])


def create_model(*args, **kwargs) -> Runnable:
    load_dotenv()
    prompt = load_chat_prompt_template_json()
    return prompt | ChatOpenAI(*args, **kwargs)
