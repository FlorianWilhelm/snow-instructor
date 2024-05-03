import enum
import logging
import os
import sys
from typing import Annotated

import torch
import typer
from deepspeed.linear.config import QuantizationConfig
from transformers import AutoModelForCausalLM, AutoTokenizer

from snow_instructor import __version__

_logger = logging.getLogger(__name__)


class LogLevel(str, enum.Enum):
    CRITICAL = 'critical'
    ERROR = 'error'
    WARNING = 'warning'
    INFO = 'info'
    DEBUG = 'debug'


def setup_logging(log_level: LogLevel):
    """Setup basic logging"""
    log_format = '[%(asctime)s] %(levelname)s:%(name)s:%(message)s'
    numeric_level = getattr(logging, log_level.upper(), None)
    logging.basicConfig(level=numeric_level, stream=sys.stdout, format=log_format, datefmt='%Y-%m-%d %H:%M:%S')


def query_arctic(content: str, role: str = 'user') -> str:
    # enable hf_transfer for faster ckpt download
    os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "1"

    tokenizer = AutoTokenizer.from_pretrained(
        'Snowflake/snowflake-arctic-instruct',
        trust_remote_code=True
    )

    quant_config = QuantizationConfig(q_bits=8)

    # The 150GiB number is a workaround until we have HFQuantizer support, must be ~1.9x of the available GPU memory
    model = AutoModelForCausalLM.from_pretrained(
        "Snowflake/snowflake-arctic-instruct",
        low_cpu_mem_usage=True,
        trust_remote_code=True,
        device_map="auto",
        ds_quantization_config=quant_config,
        max_memory={i: "150GiB" for i in range(8)},
        torch_dtype=torch.bfloat16)

    messages = [{"role": "user", "content": "What is 1 + 1 "}]
    input_ids = tokenizer.apply_chat_template(messages, add_generation_prompt=True, return_tensors="pt").to("cuda")

    outputs = model.generate(input_ids=input_ids, max_new_tokens=20)
    return tokenizer.decode(outputs[0])


app = typer.Typer(
    name=f'Snow Instructor {__version__}',
    help="LLM instructor that teaches you about Snowflake's capabilities.",
)


@app.command()
def main(
    content: Annotated[str, typer.Argument(..., help='Query content')],
    log_level: Annotated[LogLevel, typer.Option(help='Log level')] = LogLevel.INFO,
):
    """Wrapper allowing :func:`fib` to be called with string arguments in a CLI fashion

    Instead of returning the value from :func:`fib`, it prints the result to the
    `stdout` in a nicely formatted message.
    """
    setup_logging(log_level)
    print(f'Arctic: {query_arctic(content=content)}')  # noqa: T201


if __name__ == '__main__':
    app()
