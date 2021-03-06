# SPDX-License-Identifier: GPL-2.0-or-later

import io

from PIL import Image

from ubot.micro_bot import ldr

NEKO_URL = "https://nekos.life/api/v2/img/"
NEKO_TYPES = ['neko', 'lewd', 'smug', 'tits', 'trap', 'anal', 'cuddle', 'hug', 'goose', 'waifu', 'gasm', 'slap', 'spank', 'pat', 'feet', 'woof', 'baka', 'blowjob']
REPLY_TYPES = ['cuddle', 'hug', 'slap', 'spank', 'pat', 'baka', 'blowjob']


@ldr.add_list(NEKO_TYPES, pattern_extra="(f|)")
async def supernekoatsume(event):
    await event.edit(f"`Processing…`")
    nekotype = event.command
    as_file = bool(event.other_args[0])

    if nekotype in REPLY_TYPES:
        reply_to = await event.get_reply_message()
    else:
        reply_to = None

    async with ldr.aioclient.get(NEKO_URL + nekotype) as response:
        if response.status == 200:
            image_url = (await response.json())["url"]
        else:
            await event.edit(f"`An error occurred, response code: `**{response.status}**")
            return

    try:
        await event.client.send_file(event.chat_id, file=image_url, force_document=as_file, reply_to=reply_to)
        await event.delete()
    except:
        await event.edit(f"`Failed to fetch media for query: `**{nekotype}**")


@ldr.add("8ball")
async def eightball(event):
    await event.edit(f"`Processing…`")

    async with ldr.aioclient.get(NEKO_URL + "8ball") as response:
        if response.status == 200:
            image_url = (await response.json())["url"]
        else:
            await event.edit(f"`An error occurred, response code: `**{response.status}**")
            return

    async with ldr.aioclient.get(image_url) as response:
        if response.status == 200:
            image_data = await response.read()
        else:
            await event.edit(f"`An error occurred, response code: `**{response.status}**")
            return

    sticker_image = Image.open(io.BytesIO(image_data))
    sticker_io = io.BytesIO()
    sticker_image.save(sticker_io, "WebP", quality=99)
    sticker_io.seek(0)
    sticker_io.name = "sticker.webp"

    try:
        await event.client.send_file(event.chat_id, file=sticker_io)
        await event.delete()
    except:
        await event.edit(f"`Failed to send 8ball! :(`")
