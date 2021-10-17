import asyncio
import logging
from asyncio.subprocess import Process


async def start_script(cmd: str):
    proc = await asyncio.create_subprocess_shell(
        cmd=cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    return proc


async def communicate_script(cmd: str, proc: Process):
    stdout, stderr = await proc.communicate()
    stdout_decoded = stdout.decode()
    stderr_decoded = stderr.decode()
    logging.info(f'[{cmd!r} exited with {proc.returncode}]')
    if stdout:
        logging.info(f'[stdout]\n{stdout_decoded}')
    if stderr:
        logging.info(f'[stderr]\n{stderr_decoded}')
    return stdout, stderr
