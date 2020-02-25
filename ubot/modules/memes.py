# SPDX-License-Identifier: GPL-2.0-or-later

from asyncio import sleep
from random import choice, randint

from ubot.micro_bot import micro_bot

ldr = micro_bot.loader

emoji = list("😂😝🤪🤩😤🥵🤯🥶😱🤔😩🙄💀👻🤡😹👀👁👌💦🔥🌚🌝🌞🔫💯")
b_emoji = "🅱️"
a_emoji = "🅰️"
i_emoji = "ℹ️"

owo_faces = "owo uwu owu uwo u-u o-o OwO UwU @-@ ;-; ;_; ._. (._.) (o-o) ('._.) (｡◕‿‿◕｡)" \
    " (｡◕‿◕｡) (─‿‿─) ◔⌣◔ ◉_◉".split(sep=" ")

vibe_checks = "Shitting pants…|Unshitting pants…|Checking for good vibes…|Checking for bad vibes…|" \
    "Analyzing wiggly air…|Sniffing for poopy pants…|Eating a Snickers…|Ripping paper with an eraser…|" \
    "Vibing…|Connecting to dial-up…|Writing stupid quotes…|Consuming carbohydrates…|Hydrating…|" \
    "Feeding the wolf…|OwO what's this?|Eating 3 week old pancakes…|Doing quick maths…|Squatting…|" \
    "Thinking real hard…|Making slime in science class…|Orang man bad…|Browsing 4chan…|Breathing…|" \
    "Uh oh, stinky…|Splitting strings…|Breaking pencils…|Yeeting…|Releasing Half-Life 3…|Failing…|" \
    "He do look kinda chill doe…|Cats are liquid…|Stay hydrated…|Using random.choice()…|Licking 9-volt batteries…|" \
    "Building vibecheck.exe…|Building vibecheck.so…|Flashing custom ROMs…|Suffocating my demons…|" \
    "Reticulating splines…|Drinking maple syrup…|Failing at life…|Calibrating battery…|Foraging…|" \
    "Show me how to lie, you're getting better all the time…|Becoming Pneuma…|Contracting AIDS…|" \
    "Checkra1n…|Checkm8 motherfucker…|Exploiting your denial…|Checking the door lights…|Flashing Bonnie…|" \
    "Opening loot-boxes…|Vibing…|Updating to Python 3.8.0…|Having information leading to the arrest of Hil-…|" \
    "Epstein didn't kill himself…|Cracking open the boys with a cold hatchet…|I'm gonna be sick…|" \
    "I can feel it in my blood and in my bones…|Writing commit messages…|Creating redsn0w…".split(sep="|")

zal_chars = " ̷̡̛̮͇̝͉̫̭͈͗͂̎͌̒̉̋́͜ ̵̠͕͍̩̟͚͍̞̳̌́̀̑̐̇̎̚͝ ̸̻̠̮̬̻͇͈̮̯̋̄͛̊͋̐̇͝͠ ̵̧̟͎͈̪̜̫̪͖̎͛̀͋͗́̍̊͠ ̵͍͉̟͕͇͎̖̹̔͌̊̏̌̽́̈́͊ͅ ̷̥͚̼̬̦͓͇̗͕͊̏͂͆̈̀̚͘̚ ̵̢̨̗̝̳͉̱̦͖̔̾͒͊͒̎̂̎͝ ̵̞̜̭̦̖̺͉̞̃͂͋̒̋͂̈́͘̕͜ ̶̢̢͇̲̥̗̟̏͛̇̏̊̑̌̔̚ͅͅ ̷̮͖͚̦̦̞̱̠̰̍̆̐͆͆͆̈̌́ ̶̲͚̪̪̪͍̹̜̬͊̆͋̄͒̾͆͝͝ ̴̨̛͍͖͎̞͍̞͕̟͑͊̉͗͑͆͘̕ ̶͕̪̞̲̘̬͖̙̞̽͌͗̽̒͋̾̍̀ ̵̨̧̡̧̖͔̞̠̝̌̂̐̉̊̈́́̑̓ ̶̛̱̼̗̱̙͖̳̬͇̽̈̀̀̎̋͌͝ ̷̧̺͈̫̖̖͈̱͎͋͌̆̈̃̐́̀̈".replace(" ", "")


@ldr.add(pattern="cp")
async def copypasta(event):
    text_arg = await get_text_arg(event)

    text_arg = await shitpostify(text_arg)
    text_arg = await mockify(text_arg)
    text_arg = await emojify(text_arg)
    cp_text = await vaporize(text_arg)

    await event.edit(cp_text)


@ldr.add(pattern="mock")
async def mock(event):
    text_arg = await get_text_arg(event)

    mock_text = await mockify(text_arg)

    await event.edit(mock_text)


@ldr.add(pattern="vap")
async def vapor(event):
    text_arg = await get_text_arg(event)

    vapor_text = await vaporize(text_arg)

    await event.edit(vapor_text)


@ldr.add(pattern="zal")
async def zalgo(event):
    text_arg = await get_text_arg(event)

    zalgo_text = await zalgofy(text_arg)

    await event.edit(zalgo_text)


@ldr.add(pattern="owo")
async def owo(event):
    text_arg = await get_text_arg(event)

    owo_text = await owoify(text_arg)

    await event.edit(owo_text)


@ldr.add(pattern="vibecheck")
async def vibecheck(event):
    if event.is_reply:
        await event.edit("`Performing vibe check…`")
    else:
        await event.edit("`Performing self vibe check…`")

    for _ in range(7):
        await sleep(4)
        try:
            await event.edit(f"`{choice(vibe_checks)}`")
        except:
            pass

    await sleep(4)
    if choice([True, False]):
        await event.edit("`Vibe check passed!`")
    else:
        await event.edit("`Vibe check failed!`")


async def get_text_arg(event):
    text_arg = event.pattern_match.group(1)

    if text_arg:
        pass
    elif event.is_reply:
        reply = await event.get_reply_message()
        text_arg = reply.text
    else:
        text_arg = "Give me some text to fuck it up!"

    return text_arg


async def shitpostify(text):
    text = text.replace("dick", "peepee")
    text = text.replace("ck", "cc")
    text = text.replace("lol", "honk honk")
    text = text.replace("though", "tho")
    text = text.replace("cat", "pussy")
    text = text.replace("dark", "dank")

    return text


async def mockify(text):
    mock_text = ""

    for letter in text:
        if len(mock_text) >= 2:
            if ''.join(mock_text[-2:-1]).islower():
                mock_text += letter.upper()
                continue

            if ''.join(mock_text[-2:-1]).isupper():
                mock_text += letter.lower()
                continue

        if randint(1, 2) == randint(1, 2):
            mock_text += letter.lower()
        else:
            mock_text += letter.upper()

    return mock_text


async def emojify(text):
    text = text.replace("ab", "🆎")
    text = text.replace("cl", "🆑")
    text = text.replace("b", "🅱️")
    text = text.replace("a", "🅰️")
    text = text.replace("i", "ℹ️")
    text = text.replace("AB", "🆎")
    text = text.replace("CL", "🆑")
    text = text.replace("B", "🅱️")
    text = text.replace("A", "🅰️")
    text = text.replace("I", "ℹ️")

    emoji_text = ""

    for letter in text:
        if letter == " ":
            emoji_text += choice(emoji)
        else:
            emoji_text += letter

    return emoji_text


async def vaporize(text):
    vapor_text = ""
    char_distance = 65248

    for letter in text:
        ord_letter = ord(letter)
        if ord('!') <= ord_letter <= ord('~'):
            letter = chr(ord_letter + char_distance)
        vapor_text += letter

    return vapor_text


async def owoify(text):
    text = text.replace("r", "w")
    text = text.replace("R", "W")
    text = text.replace("n", "ny")
    text = text.replace("N", "NY")
    text = text.replace("ll", "w")
    text = text.replace("LL", "W")
    text = text.replace("l", "w")
    text = text.replace("L", "W")

    text += f" {choice(owo_faces)}"

    return text


async def zalgofy(text):
    zalgo_text = ""

    for letter in text:
        if letter == " ":
            zalgo_text += letter
            continue

        letter += choice(zal_chars)
        letter += choice(zal_chars)
        letter += choice(zal_chars)
        zalgo_text += letter

    return zalgo_text
