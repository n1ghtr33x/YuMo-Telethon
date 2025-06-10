from telethon import events

from utils.db import db
from utils.misc import modules_help, prefix

from utils.scripts import restart, command

async def restart_cmd(event: events.NewMessage.Event):
    db.set(
        "core.updater",
        "restart_info",
        {
            "type": "restart",
            "chat_id": event.chat_id,
            "message_id": event.message.id
        }
    )
    await event.edit("<b>Перезагрузка...</b>", parse_mode='html')
    restart()

handlers = [
    (restart_cmd, command('restart')),
]

modules_help["restart"] = {
    'restart': 'перезагрузить YuMo'
}