import os
import platform

from telethon import events
from utils.misc import modules_help, prefix, python_version, userbot_version
from utils.scripts import command

my_system = platform.uname()

async def info(event: events.NewMessage.Event):
    await event.edit("<emoji id='5435965782414602696'>🕊</emoji>"
                     "<a href=https://t.me/irisobote>-YuMo UserBot-</a>"
                     "<emoji id='5435965782414602696'>🕊</emoji>\n\n"
                     f"<b>| Версия [{userbot_version}]\n"
                     f"| Префикс [ {prefix} ]\n"
                     f"| Канал юзербота <a href='https://t.me/n1ghtr33x_channel'>{'{клик}'}</a>\n"
                     f"| Разработчик <a href='t.me/d08ee'>Чайна</a>\n"
                     f"| Версия Python: {python_version}\n"
                     f"| Система: {my_system.system}\n"
                     f"| Количество ядер CPU: {os.cpu_count()}</b>", parse_mode='html', link_preview=True)

handlers = [
    (info, command('info')),
]

modules_help['info'] = {
    'info': 'информация о юзерботе'
}