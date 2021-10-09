from jinja2 import FileSystemLoader, Environment
from openai import Completion
from openai.error import InvalidRequestError
from logging import debug


from .error import AcoderError


PATH_TO_PROMPTS = "solver/prompts"


class InputTooLongError(AcoderError):
    pass


class ContentFilterError(AcoderError):
    pass


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
        "temperature": 0,
        "logprobs": 2
    }
    parameters = {**default, **kwargs}
    try:
        response = Completion.create(**parameters)['choices'][0]
    except InvalidRequestError:
        raise InputTooLongError("The input is too long")
    debug(f"Prompt: {prompt_}")
    debug(f"Response: {response['text']}")
    if response['finish_reason'] == 'length':
        raise InputTooLongError("The input is too long")
    if response['finish_reason'] == 'content_filter':
        raise ContentFilterError("The content filter has been triggered")
    return response["text"]
