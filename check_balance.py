import discord
from discord import app_commands
from discord.ext import commands
from money_utils import get_user_data  # ใช้ฐานข้อมูลร่วมกับระบบหลัก

COMMAND_CHANNEL_ID = 1357385446359044208  # ห้องที่อนุญาตให้ใช้คำสั่งนี้
CHECK_ALL_CHANNEL_ID = 1357385446359044208  # ห้องที่อนุญาตให้ใช้ /check all (แยกห้องได้)

class CheckBalance(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # /check @user
    @app_commands.command(name="check", description="ตรวจสอบยอดเงินของผู้ใช้ (Admin เท่านั้นน!)")
    @app_commands.describe(member="ผู้ใช้ที่ต้องการตรวจสอบยอดเงิน")
    async def check_command(self, interaction: discord.Interaction, member: discord.Member):
        if interaction.channel.id != COMMAND_CHANNEL_ID:
            return await interaction.response.send_message("Admin เท่านั้น !!!", ephemeral=True)

        user_data = get_user_data(str(member.id))
        balance = user_data["balance"]

        await interaction.response.send_message(
            f'{member.mention} มีเงินคงเหลืออยู่ {balance} บาท', ephemeral=True
        )

       # /check_all
    @app_commands.command(name="check_all", description="จัดอันดับสมาชิกที่มีเงินเยอะที่สุด 10 อันดับเเรกก")
    async def check_all_command(self, interaction: discord.Interaction):
        if interaction.channel.id != CHECK_ALL_CHANNEL_ID:
            return await interaction.response.send_message("Admin เท่านั้น !!!", ephemeral=True)

        members = interaction.guild.members
        leaderboard = []

        for member in members:
            if member.bot:
                continue
            data = get_user_data(str(member.id))
            leaderboard.append((member.mention, data["balance"]))  # ใช้ mention แทน display_name

        top10 = sorted(leaderboard, key=lambda x: x[1], reverse=True)[:10]

        if not top10:
            return await interaction.response.send_message("ไม่มีข้อมูลสมาชิก", ephemeral=True)

        result = "**อันดับ 10 สมาชิกที่มีเงินเยอะที่สุด:**\n"
        for i, (mention, balance) in enumerate(top10, start=1):
            result += f"#{i}. {mention} - {balance} บาท\n"

        await interaction.response.send_message(result, ephemeral=True)


async def setup(bot):
    await bot.add_cog(CheckBalance(bot))
