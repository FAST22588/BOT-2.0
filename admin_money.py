import discord
from discord import app_commands
from discord.ext import commands
from money_utils import get_user_data, save_data


# ห้องที่อนุญาตให้ใช้คำสั่ง
COMMAND_CHANNEL_ID = 1357385446359044208

# ห้องที่ใช้ส่งแจ้งเตือน
ALERT_CHANNEL_US = 1362998867888443412       # แก้เป็นห้องสำหรับแจ้งเพิ่มเงิน
ALERT_CHANNEL_DELETE = 1362998867888443412   # แก้เป็นห้องสำหรับแจ้งลบเงิน

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

        # ส่งแจ้งเตือน
        alert_channel = self.bot.get_channel(ALERT_CHANNEL_US)
        if alert_channel:
            embed = discord.Embed(title="เพิ่มเงิน",
                                  description=f"{interaction.user.mention} เพิ่ม **{amount}** ให้ {member.mention}",
                                  color=discord.Color.green())
            await alert_channel.send(embed=embed)

        await interaction.response.send_message(
            f"เพิ่มเงินจำนวน {amount} บาทให้ {member.mention} เรียบร้อยแล้ว!!!", ephemeral=True
        )

    @app_commands.command(name="delete", description="ลบเงินของผู้ใช้ (mention)")
    @app_commands.describe(member="ผู้ใช้ที่ต้องการลบเงิน", amount="จำนวนเงินที่ต้องการลบ")
    async def delete_command(self, interaction: discord.Interaction, member: discord.Member, amount: int):
        if interaction.channel.id != COMMAND_CHANNEL_ID:
            return await interaction.response.send_message("Admin เท่านั้น !!!", ephemeral=True)

        user_data = get_user_data(str(member.id))
        user_data["balance"] = max(0, user_data["balance"] - amount)
        save_data()

        # ส่งแจ้งเตือน
        alert_channel = self.bot.get_channel(ALERT_CHANNEL_DELETE)
        if alert_channel:
            embed = discord.Embed(title="ลบเงิน",
                                  description=f"{interaction.user.mention} ลบ **{amount}** จาก {member.mention}",
                                  color=discord.Color.red())
            await alert_channel.send(embed=embed)

        await interaction.response.send_message(
            f"ลบเงิน {amount} จาก {member.mention} เรียบร้อยแล้ว", ephemeral=True
        )

async def setup(bot):
    await bot.add_cog(AdminMoney(bot))
