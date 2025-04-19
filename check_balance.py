import discord
from discord import app_commands
from discord.ext import commands
from money_utils import get_user_data  # ใช้ฐานข้อมูลร่วมกับระบบหลัก

COMMAND_CHANNEL_ID = 1357385446359044208  # ห้องที่อนุญาตให้ใช้คำสั่งนี้

class CheckBalance(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="check", description="ตรวจสอบยอดเงินของผู้ใช้ (mention)")
    @app_commands.describe(member="ผู้ใช้ที่ต้องการตรวจสอบยอดเงิน")
    async def check_command(self, interaction: discord.Interaction, member: discord.Member):
        if interaction.channel.id != COMMAND_CHANNEL_ID:
            return await interaction.response.send_message("Admin เท่านั้น !!!", ephemeral=True)

        user_data = get_user_data(str(member.id))
        balance = user_data["balance"]

        await interaction.response.send_message(
            f'{member.mention} มีเงินคงเหลืออยู่ {balance} บาท', ephemeral=True
        )

async def setup(bot):
    await bot.add_cog(CheckBalance(bot))
