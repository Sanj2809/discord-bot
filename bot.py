import discord
from discord import app_commands
from discord.ext import commands
import os

TOKEN = os.getenv("TOKEN")

# Role được phép
ALLOWED_ROLES = ["Admin", "Helper",]

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# Check role
def has_permission(member: discord.Member):
    user_roles = [role.name for role in member.roles]
    return any(role in ALLOWED_ROLES for role in user_roles)

@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"Đã sync {len(synced)} lệnh")
    except Exception as e:
        print(e)

    print(f"Bot online: {bot.user}")

# Lệnh /stk
@bot.tree.command(name="stk", description="Gửi QR thanh toán")
async def stk(interaction: discord.Interaction):

    # Check quyền
    if not has_permission(interaction.user):
        await interaction.response.send_message(
            "❌ Bạn không có quyền dùng lệnh này!",
            ephemeral=True
        )
        return

    try:
        file = discord.File("qr.png")  # file ảnh trong thư mục
        await interaction.response.send_message(
            content="💸 Quét mã để thanh toán",
            file=file
        )
    except Exception as e:
        await interaction.response.send_message(
            f"❌ Lỗi gửi ảnh: {e}",
            ephemeral=True
        )

bot.run(TOKEN)