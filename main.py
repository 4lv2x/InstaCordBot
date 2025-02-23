from typing import Final
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv
from discord import Intents, Client, Message

from ascii import get_ascii
from responses import get_response
from storyloader import check_story, delete_old, download, fix_duplicates

load_dotenv()
TOKEN: Final[str] = os.getenv("DISCORD_TOKEN")

intents: Intents = discord.Intents.default()
intents.message_content = True #NOQA

bot = commands.Bot(command_prefix="$", intents=intents)

def story_loop(username) -> bool:
    print("Deleting old stories...")
    delete_old()
    return check_story(username)

@bot.event
async def on_ready() -> None:
    print(f"{bot.user} has connected to Discord!")

@bot.command(name="image")
async def upload_image(ctx, arg) -> None:
    if not arg or arg not in ["lol", "eduroam"]:
        ctx.send("Invalid image")
        return

    image_path: str = f"images/{arg}.jpg"

    await ctx.send(file = discord.File(image_path))

@bot.command()
async def say(ctx, arg) -> None:
    await ctx.message.delete()
    await ctx.send(arg)

@bot.command()
async def chat(ctx, arg) -> None:
    await ctx.send(get_response(arg))

@bot.command(name="watch")
async def watch_stories(ctx, arg) -> None:
    #bot.loop.create_task(check_story(arg))
    await ctx.send("Stories are being downloaded...")
    download(arg)
    if len(os.listdir("stories")) > 0:
        print("Stories downloaded")
        fix_duplicates()
        print("Duplicates fixed")
        await ctx.send("Uploading...")
        for file in os.listdir("stories"):
            if file.endswith(".jpg") or file.endswith(".mp4"):
                await ctx.send(file=discord.File("stories/"+file))
                print("Story uploaded correctly to Discord")
    else :
        await ctx.send("No stories found")

@bot.command(name="ascii")
async def ascii_art(ctx, arg) -> None:
    await ctx.message.delete()
    await ctx.send(
        f"```{get_ascii(arg)}```"
    )


@bot.command(name="help")
async def help_command(ctx) -> None:
    await ctx.send("Comandos disponibles:\n"
                   "$image <lol/eduroam> - Prueba de subida de imágenes.\n"
                   "$say <message> - Repite tu mensaje.\n"
                   "$chat <message> - Prueba de envío de imágenes (solo responde a ciertas prompts).\n"
                   "$watch <username> - Descarga y resube historias de IG de un usuario.\n"
                   "$help - Muestra este mensaje.")


def main() -> None:
    bot.run(TOKEN)

if __name__ == "__main__":
    main()