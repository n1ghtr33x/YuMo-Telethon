from telethon import events
import datetime
from utils.db import db
from utils.misc import modules_help, prefix
from utils.scripts import command

afk_info = db.get("core.afk", "afk_info", {
    "start": 0,
    "is_afk": False,
    "reason": "",
})

def is_afk_filter(event: events.NewMessage.Event) -> bool:
    return afk_info["is_afk"]

async def afk_handler(event: events.NewMessage.Event):
    if not is_afk_filter(event):
        return

    if not (event.is_private or (event.is_reply and (await event.get_reply_message()).out)):
        return


    start = datetime.datetime.fromtimestamp(afk_info["start"])
    afk_time = datetime.datetime.now().replace(microsecond=0) - start

    await event.reply(
        f"<b>Я в афк.. (уже {afk_time})</b>"
        + (f"\n<b>Сообщение:</b> <i>{afk_info['reason']}</i>" if afk_info["reason"] != "None" else ""),
        parse_mode="html"
    )

async def afk_command(event: events.NewMessage.Event):
    reason = event.pattern_match.group(1) or "None"
    afk_info.update({
        "start": int(datetime.datetime.now().timestamp()),
        "is_afk": True,
        "reason": reason,
    })
    await event.edit(
        f"<b>Я вошел в режим афк.</b>"
        + (f"\n<b>Сообщение:</b> <i>{reason}</i>" if reason != "None" else ""),
        parse_mode="html"
    )
    db.set("core.afk", "afk_info", afk_info)

async def unafk_command(event: events.NewMessage.Event):
    if afk_info["is_afk"]:
        start = datetime.datetime.fromtimestamp(afk_info["start"])
        afk_time = datetime.datetime.now().replace(microsecond=0) - start
        afk_info["is_afk"] = False
        await event.edit(
            f"<b>Я больше не в афк.</b>\n<b>Я был в афк {afk_time}</b>",
            parse_mode="html"
        )
    else:
        await event.edit("<b>Ты не в афк.</b>", parse_mode="html")

    db.set("core.afk", "afk_info", afk_info)

handlers = [
    (afk_handler, events.NewMessage(incoming=True)),
    (afk_command, command('afk')),
    (unafk_command, command('unafk')),
]

modules_help["afk"] = {
    "afk [сообщение]": "Войти в афк",
    "unafk": "Выйти из афк",
}
