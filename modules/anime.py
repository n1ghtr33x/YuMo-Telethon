import aiohttp
from telethon import events
from utils.misc import modules_help
from utils.scripts import command

async def anime(event: events.NewMessage.Event):
    query = event.pattern_match.group(1)

    await event.edit("🔍 Ищу аниме...")

    url = f"https://api.jikan.moe/v4/anime?q={query}&limit=1"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    await event.edit("❌ Ошибка при обращении к Jikan API.")
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
        synopsis = anime.get("synopsis", "нет описания")[:500] + "..."
        url = anime.get("url")
        image = anime.get("images", {}).get("jpg", {}).get("image_url")

        caption = (
            f"🎌 <b>{title}</b> ({title_jp})\n\n"
            f"📺 Эпизоды: {episodes}\n"
            f"⭐ Оценка: {score}\n"
            f"📡 Статус: {status}\n\n"
            f"📖 Описание:\n{synopsis}\n\n"
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