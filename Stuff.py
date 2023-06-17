from .worker import *

async def up(event):
    if not event.is_private:
        return
    stt = dt.now()
    ed = dt.now()
    v = ts(int((ed - uptime).seconds) * 1000)
    ms = (ed - stt).microseconds / 1000
    p = f"🌋Pɪɴɢ = {ms}ms"
    await event.reply(v + "\n" + p)

async def start(event):
    await event.reply(
        f"Hi `{event.sender.first_name}`\nThis is a CompressorQueue that can encode videos and reduce their size with negligible quality change.\nYou can also generate sample compressed videos.",
        buttons=[
            [Button.inline("HELP", data="ihelp")],
            [
                Button.url("SOURCE CODE", url="https://github.com/1Danish-00/CompressorQueue"),
                Button.url("DEVELOPER", url="https://t.me/danish_00"),
            ],
        ],
    )

async def help(event):
    await event.reply(
        "**🐠 A Quality CompressorQueue**\n\n+ This bot compresses videos with negligible quality change.\n+ It can generate sample compressed videos.\n+ Easy to use.\n\nPlease note that due to quality settings, the bot may take some time to compress videos. So, please be patient and send videos one by one.\n\nJust forward a video to get options."
    )

async def ihelp(event):
    await event.edit(
        "**🐠 A Quality CompressorQueue**\n\n+ This bot compresses videos with negligible quality change.\n+ It can generate sample compressed videos.\n+ It can also generate screenshots.\n+ Easy to use.\n\nPlease note that due to quality settings, the bot may take some time to compress videos. So, please be patient and send videos one by one.\n\nJust forward a video to get options.",
        buttons=[Button.inline("BACK", data="beck")],
    )

async def beck(event):
    await event.edit(
        f"Hi `{event.sender.first_name}`\nThis is a CompressorQueue that can encode videos and reduce their size with negligible quality change.\nYou can also generate sample compressed videos.",
        buttons=[
            [Button.inline("HELP", data="ihelp")],
            [
                Button.url("SOURCE CODE", url="https://github.com/Tobigod123/Maybeormaybenotbe/tree/main"),
                Button.url("DEVELOPER", url="https://github.com"),
            ],
        ],
    )
