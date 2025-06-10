import aiohttp
from telethon import events
from utils.misc import modules_help
from utils.scripts import command

async def anime(event: events.NewMessage.Event):
    query = event.pattern_match.group(1)

    await event.edit("🔍 Ищу аниме...")

    jikan_url = f"https://api.jikan.moe/v4/anime?q={query}&limit=1"
    translate_url = "https://libretranslate.de/translate"

    try:
        async with aiohttp.ClientSession() as session:
            # Получаем аниме
            async with session.get(jikan_url) as resp:
                if resp.status != 200:
                    await event.edit("❌ Не удалось получить данные с Jikan API.")
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

            # Переводим описание
            translated_synopsis = "❌ Перевод недоступен."
            if synopsis and synopsis != "нет описания":
                translate_payload = {
                    "q": synopsis,
                    "source": "en",
                    "target": "ru",
                    "format": "text"
                }
                async with session.post(translate_url, json=translate_payload) as resp:
                    if resp.status == 200:
                        translated = await resp.json()
                        translated_synopsis = translated.get("translatedText", translated_synopsis)

        caption = (
            f"🎌 <b>{title}</b> ({title_jp})\n\n"
            f"📺 Эпизоды: {episodes}\n"
            f"⭐ Оценка: {score}\n"
            f"📡 Статус: {status}\n\n"
            f"📖 <b>Описание:</b>\n{translated_synopsis}\n\n"
            f"🔗 <a href='{url}'>MyAnimeList</a>"
        )

        await event.delete()
        await event.respond(caption, file=image, link_preview=False)

    except Exception as e:
        await event.edit(f"💥 Ошибка: {e}")


handlers = [
    (anime, command('anime'))
]

modules_help['anime'] = {
    'anime [название]': 'Поиск аниме'
}