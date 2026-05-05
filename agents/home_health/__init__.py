from dotenv import load_dotenv

load_dotenv(override=True)

from .agent import root_agent  # noqa: E402, F401

__all__ = ["root_agent"]
