import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

from myserver import server_on

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
   # await bot.load_extension("shop")  # ถ้ายังไม่มี shop.py ก็แค่คอมเมนต์บรรทัดนี้ไว้ก่อน
    await bot.start('TOKEN')

import asyncio
asyncio.run(main())
