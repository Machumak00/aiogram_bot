import asyncio
import logging
import os.path

from aiogram.dispatcher.storage import FSMContextProxy


async def start_nmap(nmap_data: FSMContextProxy):
    current_path = os.path.dirname(os.path.abspath(__file__))
    if nmap_data['nmapscan'] == 'nmapcustom':
        cmd = f"sh '{current_path}/{nmap_data['nmapscan']}.sh' {nmap_data['custom_args']} {nmap_data['ip']}"
    else:
        cmd = f"sh '{current_path}/{nmap_data['nmapscan']}.sh' {nmap_data['ip']}"
    proc = await asyncio.create_subprocess_shell(
        cmd=cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await proc.communicate()
    logging.info(f'[{cmd!r} exited with {proc.returncode}]')
    if stdout:
        logging.info(f'[stdout]\n{stdout.decode()}')
    if stderr:
        logging.info(f'[stderr]\n{stderr.decode()}')
    return stdout