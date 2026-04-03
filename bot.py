import discord
from discord import app_commands
from discord.ext import commands
import os

# ====== TOKEN từ Railway ======
TOKEN = os.getenv("TOKEN")

# ====== CONFIG ======
BANK_ID = "970436"        # Vietcombank
ACCOUNT_NO = "123456789"  # STK của bạn
ACCOUNT_NAME = "NGUYEN VAN A"

# Các role được phép dùng
ALLOWED_ROLES = ["Admin", "Helper", "Mod"]

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# ====== Check role ======
def has_permission(member: discord.Member):
    user_roles = [role.name for role in member.roles]
    return any(role in ALLOWED_ROLES for role in user_roles)

# ====== Khi bot online ======
@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"Đã sync {len(synced)} lệnh")
    except Exception as e:
        print(e)

    print(f"Bot online: {bot.user}")

# ====== Slash command /stk ======
@bot.tree.command(name="stk", description="Gửi QR thanh toán")
async def stk(interaction: discord.Interaction):

    # Check quyền
    if not has_permission(interaction.user):
        await interaction.response.send_message(
            "❌ Bạn không có quyền dùng lệnh này!",
            ephemeral=True
        )
        return

    # Link QR cố định
    qr_url = f"https://img.vietqr.io/image/{BANK_ID}-{ACCOUNT_NO}-compact2.png?addInfo=Thanh%20toan&accountName={ACCOUNT_NAME}"

    embed = discord.Embed(
        title="💸 Thanh toán",
        description="Quét mã để chuyển khoản",
        color=0x00ff99
    )

    embed.set_image(url=qr_url)
    embed.add_field(name="Ngân hàng", value="Vietcombank", inline=True)
    embed.add_field(name="STK", value=ACCOUNT_NO, inline=True)
    embed.set_footer(text="Vui lòng kiểm tra thông tin trước khi chuyển")

    await interaction.response.send_message(embed=embed)

# ====== RUN BOT ======
bot.run(TOKEN)