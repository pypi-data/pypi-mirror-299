import time
import platform

import libem

_model, _tokenizer = None, None

""" Llama """


def call(prompt: str | list | dict,
         tools: list[str] = None,
         context: list = None,
         model: str = "llama3",
         temperature: float = 0.0,
         seed: int = None,
         max_model_call: int = 3,
         ) -> dict:
    global _model, _tokenizer

    # format the prompt to messages
    match prompt:
        case list():
            messages = prompt
        case dict():
            messages = []
            for role, content in prompt.items():
                if content:
                    messages.append({"role": role, "content": content})
        case str():
            messages = [{"role": "user", "content": prompt}]
        case _:
            raise ValueError(f"Invalid prompt type: {type(prompt)}")
    message_openai = (messages or []) + (context or [])

    if model == "llama3" or model == "llama3.1":
        BOS = "<|begin_of_text|>"
        SYS = "<|start_header_id|>system<|end_header_id|>"
        USER = "<|start_header_id|>user<|end_header_id|>"
        ASSIS = "<|start_header_id|>assistant<|end_header_id|>"
        EOS = "<|eot_id|>"

        input_text = BOS
        for message in messages:
            if message['role'] == 'system':
                input_text = input_text + SYS + message['content'] + EOS
            elif message['role'] == 'user':
                input_text = input_text + USER + message['content'] + EOS
        input_text = input_text + ASSIS

    context = context or []
    messages = context + [input_text]

    # apple silicon
    if platform.machine() == "arm64" and platform.system() == "Darwin":
        # first check whether mlx_lm is installed
        try:
            from mlx_lm import load, generate
        except ImportError:
            raise ImportError("mlx_lm is not installed.")
    
        # Load the model using MLX for apple silicon device
        if model == "llama3":
            model_path = "mlx-community/Meta-Llama-3-8B-Instruct-8bit"
        elif model == "llama3.1":
            model_path = "mlx-community/Meta-Llama-3.1-8B-Instruct-8bit"
        else:
            raise ValueError(f"{model} is not supported.")

        if _model is None or _tokenizer is None:
            start = time.time()
            _model, _tokenizer = load(model_path)
            libem.debug(f"model loaded in {time.time() - start:.2f} seconds.")
        else:
            libem.debug("model loaded from cache")
        model, tokenizer = _model, _tokenizer

        if tools:
            raise libem.ToolUseUnsupported("Tool use is not supported")

        response = generate(model, tokenizer, prompt=messages[0], temp=temperature)
        response_message = "messages is not supported"

    else:
        try:
            from llama_cpp import Llama
        except ImportError:
            raise ImportError("llama.cpp is not installed.")
        if model == "llama3":
            model_path = "bartowski/Meta-Llama-3-8B-Instruct-GGUF"
            model_name = "Meta-Llama-3-8B-Instruct-Q5_K_S.gguf"
        elif model == "llama3.1":
            model_path = "bartowski/Meta-Llama-3.1-8B-Instruct-GGUF"
            model_name = "Meta-Llama-3.1-8B-Instruct-Q5_K_M.gguf"
        else:
            raise ValueError(f"{model} is not supported.")

        if _model is None or _tokenizer is None:
            start = time.time()
            _model = Llama.from_pretrained(
                repo_id=model_path,
                filename=model_name,
                temperature=temperature,
                seed=seed,
                verbose=True
            )
            libem.debug(f"model loaded in {time.time() - start:.2f} seconds.")
        else:
            libem.debug("model loaded from cache")
        model = _model

        if tools:
            raise libem.ToolUseUnsupported("Tool use is not supported")
        else:
            response = model.create_chat_completion(messages=message_openai)
            response_message = response['choices'][0]['message']
            response = response_message['content']

    # TBD: get input and output tokens count
    libem.trace.add({
        "model": {
            "messages": messages,
            "num_model_calls": 1,
            "num_input_tokens": -1,
            "num_output_tokens": -1,
            "model": model,
        }
    })

    return {
        "output": response,
        "messages": response_message,
        "tool_outputs": "Tool output is not supported",
        "stats": {
            "num_model_calls": 1,
            "num_input_tokens": -1,
            "num_output_tokens": -1,
        }
    }


def reset():
    global _model, _tokenizer
    _model, _tokenizer = None, None
