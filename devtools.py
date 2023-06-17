# https://github.com/1Danish-00/CompressorQueue/blob/main/License> .

import sys
import io
import asyncio
import traceback
from .stuff import OWNER, DEV


async def eval_command(event):
    if str(event.sender_id) not in OWNER and event.sender_id != DEV:
        return await event.reply("**Sorry, you're not an authorized user!**")
    
    cmd = event.text.split(" ", maxsplit=1)[1]
    stdout, stderr, exc = await execute_code(cmd, event)
    evaluation = exc or stderr or stdout or "Success"
    
    final_output = f"**EVAL**: `{cmd}` \n\n **OUTPUT**: \n`{evaluation}` \n"
    
    if len(final_output) > 4095:
        with io.BytesIO(str.encode(final_output)) as out_file:
            out_file.name = "eval.txt"
            await event.client.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption=cmd,
            )
            await event.delete()
    else:
        await event.reply(final_output)


async def execute_code(code, event):
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None
    
    try:
        await aexec(code, event)
    except Exception:
        exc = traceback.format_exc()
    
    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    
    return stdout, stderr, exc


async def aexec(code, event):
    exec(f"async def __aexec(event): " + "".join(f"\n {l}" for l in code.split("\n")))
    return await locals()["__aexec"](event)


async def bash_command(event):
    if str(event.sender_id) not in OWNER and event.sender_id != DEV:
        return await event.reply("**Sorry, you're not an authorized user!**")
    
    cmd = event.text.split(" ", maxsplit=1)[1]
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    e = stderr.decode() or "No Error"
    o = stdout.decode() or "**Tip**: \n`If you want to see the results of your code, I suggest printing them to stdout.`"
    output = f"**QUERY:**\n__Command:__\n`{cmd}` \n__PID:__\n`{process.pid}`\n\n**stderr:** \n`{e}`\n**Output:**\n{o}"
    
    if len(output) > 4095:
        with io.BytesIO(str.encode(output)) as out_file:
            out_file.name = "exec.txt"
            await event.client.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption=cmd,
            )
            await event.delete()
    else:
        await event.reply(output)
