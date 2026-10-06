import os

from dotenv import load_dotenv
from openrouter import OpenRouter

DOTENV_PLACEHOLDER_KEY = "replace-with-your-key"


def read_openrouter_api_key() -> str:
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY", "")
    if api_key in ("", DOTENV_PLACEHOLDER_KEY):
        raise RuntimeError(
            "OPENROUTER_API_KEY is unset or still the placeholder: "
            "put your key in .env at the repository root"
        )
    return api_key


def make_client() -> OpenRouter:
    return OpenRouter(api_key=read_openrouter_api_key())
