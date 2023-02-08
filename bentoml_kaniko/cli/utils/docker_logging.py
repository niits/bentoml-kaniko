"""
This module contains function which logs the output of a subprocess
"""
import typer


def log_subprocess_output(pipe):
    """
    This function logs the output of a subprocess. It takes a pipe as an argument
    and iterates over each line of the pipe, stripping it of whitespace and echoing
    it using typer.

    Args:
        pipe (_type_): _description_
    """    
    for line in iter(pipe.readline, b""):  # b'\n'-separated lines
        typer.echo(line.strip())
