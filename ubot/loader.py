# SPDX-License-Identifier: GPL-2.0-or-later

import glob
from concurrent.futures import ThreadPoolExecutor
from importlib import import_module, reload
from os.path import basename, dirname, isfile

from aiohttp import ClientSession
from telethon.tl.types import DocumentAttributeFilename

from .command_handler import CommandHandler


class Loader():
    aioclient = ClientSession()
    thread_pool = ThreadPoolExecutor()

    help_dict = {}
    loaded_modules = []
    all_modules = []

    def __init__(self, client, logger, settings):
        self.client = client
        self.logger = logger
        self.settings = settings
        self.command_handler = CommandHandler(client, settings)

    def load_all_modules(self):
        self._find_all_modules()

        for module_name in self.all_modules:
            try:
                self.loaded_modules.append(import_module("ubot.modules." + module_name))
            except Exception as exception:
                self.logger.error(f"Error while loading {module_name}: {exception}")

    def reload_all_modules(self):
        self.command_handler.outgoing_commands = []
        self.help_dict = {}

        errors = ""

        for module in self.loaded_modules:
            try:
                reload(module)
            except ModuleNotFoundError:
                pass
            except Exception as exception:
                errors += f"`Error while reloading {module.__name__} -> {exception}\n\n`"
                raise exception

        return errors or None

    def add(self, pattern=None, **args):
        pattern = args.get("pattern", pattern)
        pattern_extra = args.get("pattern_extra", "")

        def decorator(func):
            if func.__module__.split(".")[-1] in self.help_dict:
                self.help_dict[func.__module__.split(".")[-1]] += [[pattern, args.get('help', None)]]
            else:
                self.help_dict[func.__module__.split(".")[-1]] = [[pattern, args.get('help', None)]]

            self.command_handler.outgoing_commands.append({
                "pattern": pattern,
                "pattern_extra": pattern_extra,
                "function": func,
                "simple_pattern": args.get('simple_pattern', False),
                "raw_pattern": args.get('raw_pattern', False),
                "extras": args.get('extras', pattern)
            })

            return func

        return decorator

    def add_list(self, pattern=None, **args):
        pattern_list = args.get("pattern", pattern)
        pattern_extra = args.get("pattern_extra", "")

        def decorator(func):
            for pattern in pattern_list:
                if func.__module__.split(".")[-1] in self.help_dict:
                    self.help_dict[func.__module__.split(".")[-1]] += [[pattern, args.get('help', None)]]
                else:
                    self.help_dict[func.__module__.split(".")[-1]] = [[pattern, args.get('help', None)]]

                self.command_handler.outgoing_commands.append({
                    "pattern": pattern,
                    "pattern_extra": pattern_extra,
                    "function": func,
                    "simple_pattern": args.get('simple_pattern', False),
                    "raw_pattern": args.get('raw_pattern', False),
                    "extras": args.get('extras', pattern)
                })

            return func

        return decorator

    async def get_text(self, event, with_reply=True, return_msg=False, default=None):
        if event.args:
            if return_msg:
                if event.is_reply:
                    return event.args, await event.get_reply_message()

                return event.args, None

            return event.args
        elif event.is_reply and with_reply:
            reply = await event.get_reply_message()

            if return_msg:
                return reply.text, reply

            return reply.text
        else:
            if return_msg:
                return default, None

            return default

    async def get_image(self, event):
        if event and event.media:
            if event.photo:
                return event.photo
            elif event.document:
                if DocumentAttributeFilename(file_name='AnimatedSticker.tgs') in event.media.document.attributes:
                    return None
                if event.gif or event.video or event.audio or event.voice:
                    return None

                return event.media.document
            else:
                return None
        else:
            return None

    def prefix(self):
        return (self.settings.get_list('cmd_prefix') or ['.'])[0]

    def _find_all_modules(self):
        module_paths = glob.glob(dirname(__file__) + "/modules/*.py")

        self.all_modules = sorted([
            basename(f)[:-3] for f in module_paths
            if isfile(f) and f.endswith(".py")
        ])
