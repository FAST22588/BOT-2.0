import discord
from discord.ext import commands

# ✅ ใส่หลายห้องที่ต้องการให้ลบข้อความอัตโนมัติ
TARGET_CHANNEL_IDS = [
    1362327132663189525,  # ห้องที่ 1 มีห้องเเล้ว
    234567890123456789,  # ห้องที่ 2
    345678901234567890   # ห้องที่ 3
]

class AutoDelete(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        # ✅ เช็คว่าห้องนี้อยู่ในรายการห้องที่อนุญาต
        if message.channel.id in TARGET_CHANNEL_IDS:
            await message.delete(delay=10)

async def setup(bot):
    await bot.add_cog(AutoDelete(bot))
