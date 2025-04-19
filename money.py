import discord
import json
import os
from discord import app_commands
from discord.ext import commands
from datetime import datetime, timedelta
from money_utils import get_user_data, save_data


MONEY_FILE = 'money_data.json'

# ห้องที่อนุญาตให้ใช้คำสั่ง
COMMAND_CHANNEL_ID = 1362327132663189525  # ห้องที่ 4 ใช้คำสั่ง

# ห้องที่แสดงผลลัพธ์
RESULT_CHANNEL_MONEY = 1362684552879014000  # ห้องที่ 1 แสดงยอดเงิน
RESULT_CHANNEL_DAILY = 1362684614875021423  # ห้องที่ 2 แสดงรับรายวัน
RESULT_CHANNEL_PAY   = 1362684496767352933  # ห้องที่ 3 แสดงโอนเงิน

# โหลดหรือสร้างไฟล์เก็บเงิน
if os.path.exists(MONEY_FILE):
    with open(MONEY_FILE, 'r') as f:
        money_data = json.load(f)
else:
    money_data = {}

class Money(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="money", description="เช็คจำนวนเงินของคุณ")
    async def money_slash(self, interaction: discord.Interaction):
        if interaction.channel.id != COMMAND_CHANNEL_ID:
            return await interaction.response.send_message("ไม่สามารถใช้คำสั่งในห้องนี้ได้", ephemeral=True)

        user_data = get_user_data(str(interaction.user.id))
        result_channel = self.bot.get_channel(RESULT_CHANNEL_MONEY)

        await result_channel.send(f'{interaction.user.mention} มีเงิน {user_data["balance"]} บาท')
        await interaction.response.send_message(f'คุณมีเงิน {user_data["balance"]} บาท', ephemeral=True)

    @app_commands.command(name="daily", description="รับเงินรายวัน (100000 เหรียญ)")
    async def daily_slash(self, interaction: discord.Interaction):
        if interaction.channel.id != COMMAND_CHANNEL_ID:
            return await interaction.response.send_message("ไม่สามารถใช้คำสั่งในห้องนี้ได้", ephemeral=True)

        user_id = str(interaction.user.id)
        user_data = get_user_data(user_id)
        now = datetime.utcnow()
        result_channel = self.bot.get_channel(RESULT_CHANNEL_DAILY)

        last_daily_str = user_data.get("last_daily")
        if last_daily_str:
            last_daily = datetime.fromisoformat(last_daily_str)
            if now - last_daily < timedelta(hours=24):
                remaining = timedelta(hours=24) - (now - last_daily)
                hours_left = remaining.seconds // 3600
                await result_channel.send(f'{interaction.user.mention} กรุณารออีก {hours_left} ชั่วโมง')
                return await interaction.response.send_message("คุณรับเงินรายวันของวันนี้ไปแล้ว", ephemeral=True)

        user_data["balance"] += 100000
        user_data["last_daily"] = now.isoformat()
        save_data()

        await result_channel.send(f'{interaction.user.mention} รับเงินรายวัน 100000 เหรียญเรียบร้อย!')
        await interaction.response.send_message("รับเงินรายวันสำเร็จ", ephemeral=True)

    @app_commands.command(name="pay", description="โอนเงินให้ผู้อื่น")
    @app_commands.describe(member="ผู้รับ", amount="จำนวนเงินที่ต้องการโอน")
    async def pay_slash(self, interaction: discord.Interaction, member: discord.Member, amount: int):
        if interaction.channel.id != COMMAND_CHANNEL_ID:
            return await interaction.response.send_message("ไม่สามารถใช้คำสั่งในห้องนี้ได้", ephemeral=True)

        result_channel = self.bot.get_channel(RESULT_CHANNEL_PAY)

        if member.id == interaction.user.id or amount <= 0:
            await result_channel.send("คำสั่งไม่ถูกต้อง")
            return await interaction.response.send_message("ไม่สามารถโอนเงินได้", ephemeral=True)

        sender = get_user_data(str(interaction.user.id))
        receiver = get_user_data(str(member.id))

        if sender["balance"] < amount:
            await result_channel.send("คุณมีเงินไม่พอ")
            return await interaction.response.send_message("ยอดเงินไม่เพียงพอ", ephemeral=True)

        sender["balance"] -= amount
        receiver["balance"] += amount
        save_data()

        await result_channel.send(f'{interaction.user.mention} โอน {amount} บาทให้ {member.mention} เรียบร้อยแล้ว!')
        await interaction.response.send_message(f'โอนเงินให้ {member.mention} จำนวน {amount} บาทแล้ว', ephemeral=True)

async def setup(bot):
    await bot.add_cog(Money(bot))
