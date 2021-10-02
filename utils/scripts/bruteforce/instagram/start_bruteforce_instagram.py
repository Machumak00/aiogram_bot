import asyncio
import logging
import os.path

from aiogram.dispatcher.storage import FSMContextProxy

from utils.misc.files import delete_directory_files


async def start_bruteforce_instagram(bruteforce_data: FSMContextProxy):
    file_path_dict = {}
    for key in ['file1', 'file2']:
        if key in bruteforce_data.keys():
            file_path_dict[key] = bruteforce_data[key]
    if len(file_path_dict) == 1:
        await start_script(bruteforce_data, file_path_dict['file1'], 'file1.txt')
    else:
        await asyncio.gather(
            start_script(bruteforce_data, file_path_dict['file1'], 'file1.txt'),
            start_script(bruteforce_data, file_path_dict['file2'], 'file2.txt')
        )


async def start_script(bruteforce_data: FSMContextProxy, file_path: str, file: str):
    current_path = os.path.dirname(os.path.abspath(__file__))
    cmd = f"sh '{current_path}/bruteforce_instagram.sh' {current_path} {bruteforce_data['username']}  '{file_path + file}' " \
          f" {bruteforce_data['mode']}"
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
    delete_directory_files(file_path)
