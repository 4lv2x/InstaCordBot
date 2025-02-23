from typing import Final
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv
from discord import Intents, Client, Message
from responses import get_response
from storyloader import check_story, delete_old

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
    if story_loop(arg):
        for file in os.listdir("stories"):
            await ctx.send("Uploading...")
            await ctx.send(file=discord.File("stories/"+file))
    else :
        await ctx.send("No stories found")

def main() -> None:
    bot.run(TOKEN)

if __name__ == "__main__":
    main()