import os
from dotenv import load_dotenv
import discord
from discord.ext import commands

from cogs.craiyon import Craiyon

load_dotenv()

# ENV Vars
TOKEN = os.getenv("DISCORD_TOKEN")
DEBUG_GUILDS = [os.getenv("DEBUG_GUILDS")]
COMMAND_PREFIX = os.getenv("COMMAND_PREFIX", "c!")  # !craiyon

bot = commands.Bot(COMMAND_PREFIX, description='')
bot.add_cog(Craiyon(bot))


@bot.event
# this event pretty much just changes presence
async def on_ready():
    # waits for ready
    print(f"{bot.user} has connected to Discord!")
    await bot.change_presence(
        activity=discord.Activity(
            name=f"{COMMAND_PREFIX}help", type=discord.ActivityType.listening
            # name=f"kikilolohu is a nerd", type=discord.ActivityType.listening
        )
    )


@bot.slash_command(name="ping", description="Sends the bot's latency.", debug_guilds=DEBUG_GUILDS)
# this decorator makes a slash command
async def ping(ctx): # a slash command will be created with the name "ping"
    await ctx.respond(f"Pong! Latency is {bot.latency}")


bot.run(TOKEN)
