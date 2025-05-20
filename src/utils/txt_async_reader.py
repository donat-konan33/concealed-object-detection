
import asyncio
from pathlib import Path
import aiofiles
# This script reads the first value from all .txt files in a given folder asynchronously.

async def read_first_value_from_txt(file_path):
    async with aiofiles.open(file_path, mode='r') as f:
        line = await f.readline()
        if line:
            return line.strip().split()[0]  # fisrt value
        return None

async def read_all_first_values(folder_path):
    txt_files = list(Path(folder_path).glob("*.txt"))
    tasks = [read_first_value_from_txt(f) for f in txt_files]
    return await asyncio.gather(*tasks)
