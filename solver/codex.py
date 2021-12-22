from jinja2 import FileSystemLoader, Environment
from openai import Completion
from openai.error import InvalidRequestError
from logging import debug


from .errors import InputTooLongError, OutputTooLongError, ContentFilterError

PATH_TO_PROMPTS = "solver/prompts"


def prompt(prompt_template: str, **kwargs):
    template_loader = FileSystemLoader(searchpath=PATH_TO_PROMPTS)
    template_env = Environment(loader=template_loader)
    template = template_env.get_template(prompt_template)
    return template.render(**kwargs)


def codex(prompt_: str, **kwargs) -> str:
    default = {
        "engine": "davinci-codex",
        "prompt": prompt_,
        "max_tokens": 2000,
        "temperature": 0
    }
    parameters = {**default, **kwargs}
    try:
        response = Completion.create(**parameters)['choices'][0]
    except InvalidRequestError as error:
        if str(error).startswith("This model\'s maximum"):
            raise InputTooLongError("Input too long")
        raise error
    debug(f"Prompt: {prompt_}")
    debug(f"Response: {response['text']}")
    validate_finish_reason(response)
    return response["text"]


def validate_finish_reason(response):
    if response['finish_reason'] == 'length':
        raise OutputTooLongError("Output too long")
    if response['finish_reason'] == 'content_filter':
        raise ContentFilterError("Content filter triggered")
