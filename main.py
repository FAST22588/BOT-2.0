import os
import discord
from discord.ext import commands
from discord import app_commands
from myserver import server_on

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print("Bot Online!")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(f"Error syncing commands: {e}")

# ตัวอย่าง Slash Command
@bot.tree.command(name='ping', description='เช็คว่าบอทออนไลน์ไหม')
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("pong!")

# Keep alive สำหรับ Render
server_on()

# ใช้ TOKEN จาก environment variable
bot.run(os.getenv("TOKEN"))
