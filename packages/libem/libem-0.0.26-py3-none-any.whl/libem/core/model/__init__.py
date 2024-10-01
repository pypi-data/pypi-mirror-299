from libem.core.model import (
    openai, llama, claude
)
from libem.core import exec
import libem

def call(*args, **kwargs) -> dict:
    return exec.run_async_task(
        async_call(*args, **kwargs)
    )


async def async_call(*args, **kwargs) -> dict:
    match kwargs.get("model", ""):
        case "llama3" | "llama3.1":
            return llama.call(*args, **kwargs)
        case "claude-3-5-sonnet-20240620":
            return await claude.call(*args, **kwargs)
        case _:
            return await openai.async_call(*args, **kwargs)


def reset():
    openai.reset()
    claude.reset()
    llama.reset()
