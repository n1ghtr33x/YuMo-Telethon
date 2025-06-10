import re

from telethon import events
from utils.misc import modules_help
from telethon.tl.functions.stories import GetStoriesByIDRequest
from telethon.tl.types import StoryItem

from utils.scripts import command


@events.register(events.NewMessage(pattern=r'^\.story (.+)'))
async def story(event: events.NewMessage.Event):
    url = event.pattern_match.group(1)
    try:
        match = re.match(r"https://t.me/([^/]+)/s/(\d+)", url)
        if not match:
            await event.edit("❌ Неверный формат URL. Пример: https://t.me/channel_username/s/story_id")
            return

        channel_username = match.group(1)
        story_id = int(match.group(2))

        entity = await event.client.get_entity(channel_username)

        stories_result = await event.client(GetStoriesByIDRequest(
            peer=entity,
            id=[story_id]
        ))

        found_stories = stories_result.stories

        if not found_stories:
            await event.edit(f"❌ Сторис с ID {story_id} не найдена в канале @{channel_username}.")
            return

        target_story: StoryItem = found_stories[0]

        if target_story.media:
            await event.edit("📥 Скачиваю и отправляю видео...")

            downloaded_file = await event.client.download_media(
                target_story.media
            )

            await event.respond(file=downloaded_file)
        else:
            await event.edit("❌ В этой сторис нет медиафайла.")

    except Exception as e:
        await event.edit(f"💥 Ошибка: {e}")

handlers = [
    (story, command('info')),
]

modules_help['story'] = {
    'story [url]': 'скачать сторис'
}
