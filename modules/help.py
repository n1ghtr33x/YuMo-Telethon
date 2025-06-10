from telethon import events
from utils.misc import modules_help, prefix
from utils.scripts import format_module_help, command


async def help_cmd(event: events.NewMessage.Event):
    cmd = event.message.message.split(' ')
    if len(cmd) == 1:
        msg_edited = False
        text = (
            "<b>Помощь для <emoji id='5435965782414602696'>🕊</emoji><a href=https://t.me/n1ghtr33x_channel>-YuMo "
            "UserBot-</a><emoji id='5435965782414602696'>🕊</emoji>\n"
            f"Для большей информации о модуле,\nпиши <code>{prefix}help</code> <code>[module]</code>\n\n"
            f"<emoji id='5188377234380954537'>🌘</emoji> {int(len(modules_help) / 1)} доступных модулей:</b>\n\n"
        )
        for module_name, module_commands in sorted(
            modules_help.items(), key=lambda x: x[0]
        ):
            text += "[<emoji id='6298505110779594363'>❤️</emoji>] • {}: {}\n".format(
                module_name.title(),
                " ".join(
                    [
                        f"<code>{prefix + cmd_name.split()[0]}</code>"
                        for cmd_name in module_commands.keys()
                    ]
                ),
            )
            if len(text) >= 2048:
                text += "</b>"
                if msg_edited:
                    await event.reply(text, link_preview=True, parse_mode='html')
                else:
                    await event.edit(text, link_preview=True, parse_mode='html')
                    msg_edited = True
        if msg_edited:
            await event.reply(text, link_preview=True, parse_mode='html')
        else:
            await event.edit(text, link_preview=True, parse_mode='html')
    elif cmd[1].lower() in modules_help:
        await event.edit(format_module_help(cmd[1].lower()), parse_mode='html')
    else:
        command_name = cmd[1].lower()
        for name, commands in modules_help.items():
            for command in commands.keys():
                if command.split()[0] == command_name:
                    cmd1 = command.split(maxsplit=1)
                    cmd_desc = commands[command]
                    return await event.edit(
                        f"<b>Help for command <code>{prefix}{command_name}</code>\n"
                        f"Module: {name} (<code>{prefix}help {name}</code>)</b>\n\n"
                        f"<code>{prefix}{cmd1[0]}</code>"
                        f"{' <code>' + cmd1[1] + '</code>' if len(cmd1) > 1 else ''}"
                        f" — <i>{cmd_desc}</i>",
                        parse_mode='html'
                    )
        await event.edit(f"<b>Module {command_name} not found</b>", parse_mode='html')

handlers = [
    (help_cmd, command('help')),
]

modules_help['help'] = {
    'help [module/command name]': 'Get common/module/command help'
}