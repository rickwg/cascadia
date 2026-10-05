# Written by Claude Code on 2026-10-02: wiring around LOOP 1, not the lesson (the SDK is taken as given).
"""The OpenRouter client, keyed from the environment or from .env."""

import os

from dotenv import load_dotenv
from openrouter import OpenRouter

PLACEHOLDER_KEY = "replace-with-your-key"  # the value Claude wrote into .env


def make_client() -> OpenRouter:
    """Return an OpenRouter client keyed from OPENROUTER_API_KEY.

    load_dotenv() reads the repository's .env, searching upward from this file, or
    from the working directory when there is no script file (python -c, a REPL, a
    notebook) or a debugger is attached. A key already exported in the shell wins
    over the one in .env.
    """
    load_dotenv()
    key = os.environ.get("OPENROUTER_API_KEY", "")
    if key in ("", PLACEHOLDER_KEY):
        raise RuntimeError(
            "OPENROUTER_API_KEY is unset or still the placeholder: "
            "put your key in .env at the repository root"
        )
    return OpenRouter(api_key=key)
