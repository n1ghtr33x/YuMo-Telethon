import aiohttp
from telethon import events
from utils.misc import modules_help
from utils.scripts import command
from deep_translator import GoogleTranslator

async def anime(event: events.NewMessage.Event):
    query = event.pattern_match.group(1)
    await event.edit("🔍 Ищу аниме...")

    jikan_url = f"https://api.jikan.moe/v4/anime?q={query}&limit=1"

    try:
        async with aiohttp.ClientSession() as session:
            # Запрос к Jikan API
            async with session.get(jikan_url) as resp:
                if resp.status != 200:
                    await event.edit("❌ Ошибка при получении данных с Jikan API.")
                    return
                data = await resp.json()

            results = data.get("data")
            if not results:
                await event.edit("❌ Ничего не найдено.")
                return

            anime = results[0]
            title = anime.get("title")
            title_jp = anime.get("title_japanese", "")
            episodes = anime.get("episodes", "неизвестно")
            score = anime.get("score", "N/A")
            status = anime.get("status", "N/A")
            synopsis = anime.get("synopsis", "нет описания")[:1000]
            url = anime.get("url")
            image = anime.get("images", {}).get("jpg", {}).get("image_url")

            # Перевод через Google Translate
            if synopsis and synopsis != "нет описания":
                try:
                    translated_synopsis = GoogleTranslator(source='auto', target='ru').translate(synopsis)
                except Exception:
                    translated_synopsis = "❌ Не удалось перевести описание."
            else:
                translated_synopsis = "❌ Описание отсутствует."

        caption = (
            f"🎌 <b>{title}</b> ({title_jp})\n\n"
            f"📺 Эпизоды: {episodes}\n"
            f"⭐ Оценка: {score}\n"
            f"📡 Статус: {status}\n\n"
            f"📖 <b>Описание:</b>\n{translated_synopsis}\n\n"
        )

        MAX_CAPTION_LENGTH = 1024

        caption = caption[:MAX_CAPTION_LENGTH - 3] + '...' if len(caption) > MAX_CAPTION_LENGTH else caption

        try:
            await event.respond(caption, file=image, link_preview=False, parse_mode='html')
        except Exception as e:
            # fallback, если и отправка не сработала
            await event.reply(f"💥 Не удалось отправить сообщение: {e}")

        await event.delete()

    except Exception as e:
        await event.edit(f"💥 Ошибка: {e}")


handlers = [
    (anime, command('anime'))
]

modules_help['anime'] = {
    'anime [название]': 'Поиск аниме'
}