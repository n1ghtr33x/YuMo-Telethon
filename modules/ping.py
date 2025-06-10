from telethon import events
from utils.misc import modules_help, prefix
from time import time
from utils.scripts import command

async def ping(event: events.NewMessage.Event):
    t1 = time()
    await event.edit('<emoji id="6255963511252322252">✔️</emoji> пинг..', parse_mode='html')
    t2 = time()
    await event.edit(f'<emoji id="6255963511252322252">✔️</emoji> понг.. (0.{int((t2-t1)*1000)} ms)', parse_mode='html')

handlers = [
    (ping, command('ping')),
]

modules_help['ping'] = {
    'ping': 'проверить скорость отклика Telegram.'
}