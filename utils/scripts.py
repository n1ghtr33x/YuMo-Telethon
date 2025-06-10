import asyncio
import importlib
import os
import sys
from types import ModuleType
from typing import Optional

from telethon import TelegramClient, events
from telethon.tl.custom.message import Message as TelethonMessage

from .misc import modules_help, prefix, requirements_list

def command(command: str) -> events.NewMessage:
    return events.NewMessage(pattern=fr"^{prefix}{command}(?: (.+))?$")

def restart() -> None:
    os.execvp(sys.executable, [sys.executable, "main.py"])

def format_module_help(module_name: str, full=True):
    commands = modules_help[module_name]

    help_text = (
        f"<b>Помощь для [{module_name}]\n\nИспользование:</b>\n"
        if full
        else "<b>Использование:</b>\n"
    )

    for command, desc in commands.items():
        cmd = command.split(maxsplit=1)
        args = " <code>" + cmd[1] + "</code>" if len(cmd) > 1 else ""
        help_text += f"<code>{prefix}{cmd[0]}</code>{args} — <i>{desc}</i>\n"

    return help_text

def parse_meta_comments(code: str) -> dict:
    meta = {}
    for line in code.splitlines():
        if line.startswith("#") and ":" in line:
            key, value = line[1:].split(":", 1)
            meta[key.strip()] = value.strip()
    return meta

async def unload_module(module_name: str, client: TelegramClient) -> bool:
    path = "modules.custom_modules." + module_name

    if path not in sys.modules:
        return False

    try:
        module = importlib.import_module(path)
    except ImportError:
        return False

    for name, obj in vars(module).items():
        handlers = getattr(obj, "handlers", [])
        if isinstance(handlers, list):
            for handler, group in handlers:
                client.remove_event_handler(handler, group=group)

    if module_name in modules_help:
        del modules_help[module_name]

    if path in sys.modules:
        del sys.modules[path]

    return True

async def load_module(
        module_name: str,
        client: TelegramClient,
        message: Optional[TelethonMessage] = None,
        core: bool = False,
) -> ModuleType:
    if module_name in modules_help and not core:
        await unload_module(module_name, client)

    path = f"modules.{'' if core else 'custom_modules.'}{module_name}"
    file_path = f"{path.replace('.', os.sep)}.py"

    with open(file_path, encoding="utf-8") as f:
        code = f.read()
    meta = parse_meta_comments(code)

    packages = meta.get("requires", "").split()
    requirements_list.extend(packages)

    try:
        module = importlib.import_module(path)
    except ImportError as e:
        if core:
            raise

        if not packages:
            raise

        if message:
            await message.edit(
                f"<b>Installing requirements: {' '.join(packages)}</b>",
                parse_mode="html"
            )

        proc = await asyncio.create_subprocess_exec(
            sys.executable,
            "-m", "pip", "install", "-U", *packages,
        )
        try:
            await asyncio.wait_for(proc.wait(), timeout=120)
        except asyncio.TimeoutError:
            if message:
                await message.edit(
                    "<b>Timeout while installing requirements. Try to install them manually</b>",
                    parse_mode="html"
                )
            raise TimeoutError("timeout while installing requirements") from e

        if proc.returncode != 0:
            if message:
                await message.edit(
                    f"<b>Failed to install requirements (pip exited with code {proc.returncode}). "
                    f"Check logs for further info</b>",
                    parse_mode="html"
                )
            raise RuntimeError("failed to install requirements") from e

        module = importlib.import_module(path)

    if hasattr(module, "handlers"):
        for handler, event in module.handlers:
            client.add_event_handler(handler, event=event)

    if hasattr(module, "init"):
        await module.init(client)

    module.__meta__ = meta
    return module
