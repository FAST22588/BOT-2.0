import discord
from discord.ext import commands

TARGET_CHANNEL_ID = 1362327132663189525  # ใส่ ID ห้องที่ต้องการให้ลบข้อความ

class AutoDelete(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        # ข้ามข้อความของบอทเอง
        if message.author.bot:
            return

        # ตรวจสอบว่าอยู่ในห้องที่กำหนด
        if message.channel.id == TARGET_CHANNEL_ID:
            await message.delete(delay=10)  # ลบหลัง 10 วินาที

async def setup(bot):
    await bot.add_cog(AutoDelete(bot))
