import os
import asyncio
import discord
from discord.ext import commands
from discord import app_commands
from myserver import server_on

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(f"Error syncing commands: {e}")

async def main():
    await bot.load_extension("money")
    await bot.load_extension("admin_money")
    server_on()
    await bot.start(os.getenv("TOKEN"))

# เรียกใช้ main
asyncio.run(main())
