import discord
from discord import app_commands
from discord.ext import commands
import os

print(os.listdir())
TOKEN = os.getenv("TOKEN")

# Role được phép
ALLOWED_ROLES = ["Admin", "Helper",]

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# Check role
def has_permission(member: discord.Member):
    return discord.utils.get(member.roles, name="Helper") is not None

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

    if not has_permission(interaction.user):
        await interaction.response.send_message(
            "❌ Chỉ Helper mới dùng được!",
            ephemeral=True
        )
        return

    file = discord.File("qr.png")
    await interaction.response.send_message(
        content="💸 Quét mã để thanh toán",
        file=file
    )

bot.run(TOKEN)