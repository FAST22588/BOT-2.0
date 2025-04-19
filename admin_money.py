import discord
import json
import os
from discord import app_commands
from discord.ext import commands

MONEY_FILE = 'money_data.json'
COMMAND_CHANNEL_ID = 1357385446359044208

if os.path.exists(MONEY_FILE):
    with open(MONEY_FILE, 'r') as f:
        money_data = json.load(f)
else:
    money_data = {}

def save_data():
    with open(MONEY_FILE, 'w') as f:
        json.dump(money_data, f, indent=4)

def get_user_data(user_id: str):
    if user_id not in money_data:
        money_data[user_id] = {"balance": 0, "last_daily": None}
    return money_data[user_id]

class AdminMoney(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="us", description="เพิ่มเงินให้ผู้ใช้ตาม ID")
    @app_commands.describe(user_id="ID ของผู้ใช้", amount="จำนวนเงิน")
    async def us_command(self, interaction: discord.Interaction, user_id: str, amount: int):
        if interaction.channel.id != COMMAND_CHANNEL_ID:
            return await interaction.response.send_message("Admin", ephemeral=True)

        user_data = get_user_data(user_id)
        user_data["balance"] += amount
        save_data()
        await interaction.response.send_message(f"เพิ่มเงิน {amount} ให้ `{user_id}` แล้ว", ephemeral=True)

    @app_commands.command(name="delete", description="ลบเงินจากผู้ใช้ตาม ID")
    @app_commands.describe(user_id="ID ของผู้ใช้", amount="จำนวนเงิน")
    async def delete_command(self, interaction: discord.Interaction, user_id: str, amount: int):
        if interaction.channel.id != COMMAND_CHANNEL_ID:
            return await interaction.response.send_message("Admin", ephemeral=True)

        user_data = get_user_data(user_id)
        user_data["balance"] = max(0, user_data["balance"] - amount)
        save_data()
        await interaction.response.send_message(f"ลบเงิน {amount} จาก `{user_id}` แล้ว", ephemeral=True)

async def setup(bot):
    await bot.add_cog(AdminMoney(bot))  # ✅ ไม่ต้อง .add_command ซ้ำอีก
