# SPDX-License-Identifier: GPL-2.0-or-later

from re import escape, search

from telethon import events


class CommandHandler():
    pattern_template = "(?is)^({0})({1}){2}(?: |$)(.*)"
    simple_pattern_template = "(?is)^({0}){1}(?: |$|_)(.*)"
    raw_pattern_template = "(?is){0}"

    outgoing_commands = []

    def __init__(self, client, settings):
        self.settings = settings
        client.add_event_handler(self.handle_outgoing, events.NewMessage(outgoing=True, func=lambda e: not e.via_bot_id))

    async def handle_outgoing(self, event):
        prefix = "|".join([escape(i) for i in (self.settings.get_list("cmd_prefix") or ['.'])])

        for value in self.outgoing_commands:
            if value["simple_pattern"]:
                pattern_match = search(self.simple_pattern_template.format(value["pattern"], value["pattern_extra"]), event.raw_text)
            elif value["raw_pattern"]:
                pattern_match = search(self.raw_pattern_template.format(value["pattern"] + value["pattern_extra"]), event.raw_text)
            else:
                pattern_match = search(self.pattern_template.format(prefix, value["pattern"], value["pattern_extra"]), event.raw_text)

            if pattern_match:
                event.pattern_match = pattern_match
                event.args = pattern_match.groups()[-1].strip()
                event.other_args = pattern_match.groups()[2:-1]
                event.command = pattern_match.groups()[1]
                event.extras = value["extras"]

                try:
                    await value["function"](event)
                except Exception as exception:
                    await event.reply(f"`An error occurred in {value['function'].__name__}: {exception}`")
                    raise exception
