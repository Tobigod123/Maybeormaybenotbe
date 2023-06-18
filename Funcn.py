import os
import subprocess
import math
import time
import asyncio
import aiohttp
from datetime import datetime as dt
import psutil
import signal
from telegraph import TelegraphPoster

from . import *
from .config import *

WORKING = []
QUEUE = {}
OK = {}

uptime = dt.now()
os.system(f"wget {THUMB} -O thumb.jpg")

if not os.path.isdir("downloads/"):
    os.mkdir("downloads/")
if not os.path.isdir("encode/"):
    os.mkdir("encode/")
if not os.path.isdir("thumb/"):
    os.mkdir("thumb/")

def stdr(seconds: int) -> str:
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

def ts(milliseconds: int) -> str:
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    return f"{days}d, {hours}h, {minutes}m, {seconds}s, {milliseconds}ms"

def hbs(size: int) -> str:
    if not size:
        return ""
    power = 2 ** 10
    raised_to_pow = 0
    dict_power_n = {0: "B", 1: "K", 2: "M", 3: "G", 4: "T", 5: "P"}
    while size > power:
        size /= power
        raised_to_pow += 1
    return f"{round(size, 2)} {dict_power_n[raised_to_pow]}B"

No_Flood = {}

async def progress(current: int, total: int, event, start: float, type_of_ps: str, file=None):
    now = time.time()
    if No_Flood.get(event.chat_id):
        if No_Flood[event.chat_id].get(event.id):
            if (now - No_Flood[event.chat_id][event.id]) < 1.1:
                return
        else:
            No_Flood[event.chat_id].update({event.id: now})
    else:
        No_Flood.update({event.chat_id: {event.id: now}})
    diff = time.time() - start
    if round(diff % 10.00) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff
        time_to_completion = round((total - current) / speed) * 1000
        progress_str = f"[{'●' * math.floor(percentage / 5)}{'○' * (20 - math.floor(percentage / 5))}] {percentage:.2f}%\n\n"
        progress_str += f"Processed: {hbs(current)} / {hbs(total)}\n"
        progress_str += f"Speed: {hbs(speed)}/s\n"
        progress_str += f"ETA: {ts(time_to_completion)}\n"
        progress_str += f"Elapsed Time: {stdr(int(diff))}\n"
        if type_of_ps == "uploading..":
            progress_str += "Uploading..."
        elif type_of_ps == "compressing..":
            progress_str += "Compressing..."
        await event.edit(progress_str)

async def download_file(client: TelegramClient, location: TypeLocation, out: BinaryIO
