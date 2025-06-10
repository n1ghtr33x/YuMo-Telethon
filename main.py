import asyncio
import platform
from pathlib import Path

from telethon import errors, events
from telethon.sync import TelegramClient

from utils.db import db
from utils.config import api_id, api_hash
from utils.misc import prefix
from utils.scripts import restart, load_module
import logging

client = TelegramClient('YuMo Telethon',
                        api_id,
                        api_hash,
                        device_model=f"YuMo UserBot",
                        system_version=f"{platform.version()} {platform.machine()}",
                        app_version="0.0.1",
                        lang_code='en'
                        )

async def main():
    logging.basicConfig(level=logging.INFO)

    try:
        await client.start()
    except errors.RPCError as e:
        print(f"YuMo error: {e}")
        restart()  # если restart() тоже асинхронная — не забудь await

    success_modules = 0
    failed_modules = 0

    for path in Path("modules").rglob("*.py"):
        try:
            await load_module(
                path.stem,
                client,
                core=("custom_modules" not in path.parents)
            )
        except Exception:
            logging.warning(f"Can't import module {path.stem}", exc_info=True)
            failed_modules += 1
        else:
            success_modules += 1

    logging.info(f"Modules loaded: ✅ {success_modules} | ❌ {failed_modules}")
    await client.send_message('me', f"<b>Modules loaded: ✅ {success_modules} | ❌ {failed_modules}</b>", parse_mode='html')
    await client.send_message('me', f"Для помощи пиши <code>{prefix}help</code>", parse_mode='html')

    if info := db.get("core.updater", "restart_info"):
        text = {
            "restart": "<b>Успешная перезагрузка!</b>",
            "update": "<b>Update process completed!</b>",
            "loadmodule": "<b>Модуль успешно загружен!</b>",
            "dellmodule": "<b>Все модули успешно удалены!</b>"
        }[info["type"]]
        try:
            await client.edit_message(info["chat_id"], info['message_id'], text, parse_mode='html')
        except errors.RPCError:
            pass
        db.remove("core.updater", "restart_info")


    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())