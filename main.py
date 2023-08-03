import re
import shlex

from typing import Callable

from pyrogram import Client, filters
from pyrogram.types.messages_and_media.message import Message
from pyrogram import enums

from link_downloader import LinkDownloader


def getLinkType(link: str) -> str | bool:
    pairs = [
        {
            'pattern': r'https:\/\/[\w]+\.tiktok\.+[^ ]+',
            'link_type': 'tiktok'
        },
        {
            'pattern': r'https?:\/\/(?:www\.)?(?:music\.)?youtube\.com\/watch\?v=[\w-]+(?:&list=[\w-]+)?(?:&ab_channel=[\w%]+)?',
            'link_type': 'youtube'
        }
    ]

    for pair in pairs:
        if re.match(pair['pattern'], link):
            return pair['link_type']

    return False


async def command_handler(client: Client, message: Message, command_handlers: dict[str, Callable]):
    tokens = shlex.split(message.text)[1:]
    command: str = None
    value: str = None
    flags: list[str] = list()
    arguments: dict[str, str] = dict()

    i = 0
    while i < len((tokens)):
        token = tokens[i]

        if i == 0:
            if re.match('^[a-zA-Z]+$', token):
                command = token.lower()
            else:
                command = 'error'
        elif i == 1 and not token.startswith('-'):
            value = token
        elif token.startswith('--'):
            key, val = token[2:], tokens[i+1]
            if not val.startswith('--'):
                arguments[key] = val
            i += 1
        elif token.startswith('-'):
            flags.append(token[1:])

        i += 1

    args = {'client': client, 'message': message,
            'value': value, 'flags': flags, 'arguments': arguments}
    await command_handlers[command](**args)


async def download_handler(client: Client, message: Message, value: str | None, flags: list[str], arguments: dict[str, str]):
    result = message.reply_to_message.text
    link_type = getLinkType(result)

    if not link_type:
        return

    result = await LinkDownloader().get_download_link(result, link_type)

    print(result)
    
    if not result:
        return
    
    await client.send_audio('me', result, file_name='.mp3')


app = Client('my_account', api_id=0, api_hash='')

command_handlers = {
    'download': download_handler
}


@app.on_message(filters.regex(r'^@eagold\s.*'))
async def _(client: Client, message: Message):
    await command_handler(client, message, command_handlers)


app.run()
