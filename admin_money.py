import discord
import json
import os
from discord import app_commands
from discord.ext import commands

MONEY_FILE = 'money_data.json'
COMMAND_CHANNEL_ID = 1357385446359044208  # แก้เป็น ID ห้องที่อนุญาตให้ใช้

# โหลดหรือสร้างไฟล์เก็บเงิน
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

    @app_commands.command(name="us", description="เพิ่มเงินให้ผู้ใช้ (mention)")
    @app_commands.describe(member="ผู้ใช้ที่ต้องการเพิ่มเงิน", amount="จำนวนเงินที่ต้องการเพิ่ม")
    async def us_command(self, interaction: discord.Interaction, member: discord.Member, amount: int):
        if interaction.channel.id != COMMAND_CHANNEL_ID:
            return await interaction.response.send_message("Admin เท่านั้น !!!", ephemeral=True)

        user_data = get_user_data(str(member.id))
        user_data["balance"] += amount
        save_data()

        await interaction.response.send_message(
            f"เพิ่มเงิน {amount} ให้ {member.mention} เรียบร้อยแล้ว", ephemeral=True
        )

    @app_commands.command(name="delete", description="ลบเงินของผู้ใช้ (mention)")
    @app_commands.describe(member="ผู้ใช้ที่ต้องการลบเงิน", amount="จำนวนเงินที่ต้องการลบ")
    async def delete_command(self, interaction: discord.Interaction, member: discord.Member, amount: int):
        if interaction.channel.id != COMMAND_CHANNEL_ID:
            return await interaction.response.send_message("Admin เท่านั้น !!!", ephemeral=True)

        user_data = get_user_data(str(member.id))
        user_data["balance"] = max(0, user_data["balance"] - amount)
        save_data()

        await interaction.response.send_message(
            f"ลบเงิน {amount} จาก {member.mention} เรียบร้อยแล้ว", ephemeral=True
        )

async def setup(bot):
    await bot.add_cog(AdminMoney(bot))  # ไม่ต้อง add_command ซ้ำ
