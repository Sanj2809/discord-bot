import discord
from discord import app_commands
from discord.ext import commands

TOKEN = "MTQ4OTY0NDYwMDM4ODc1MTUwMA.G-0xKD.dxwDxtdhM5hf0PFSdyMOdx_H5Lp0gatDneFHF0"

# ====== CONFIG ======
BANK_ID = "970436"
ACCOUNT_NO = "123456789"
ACCOUNT_NAME = "NGUYEN VAN A"

# Danh sách role được phép dùng
ALLOWED_ROLES = ["Admin", "Helper", "Mod"]

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# ====== Check nhiều role ======
def has_permission(member: discord.Member):
    user_roles = [role.name for role in member.roles]
    return any(role in ALLOWED_ROLES for role in user_roles)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Bot online: {bot.user}")

# ====== LỆNH /stk ======
@bot.tree.command(name="stk", description="Gửi QR thanh toán")
async def stk(interaction: discord.Interaction):

    # Check quyền
    if not has_permission(interaction.user):
        await interaction.response.send_message(
            "❌ Bạn không có quyền dùng lệnh này!",
            ephemeral=True
        )
        return

    # QR cố định (không có số tiền)
    qr_url = f"https://img.vietqr.io/image/{BANK_ID}-{ACCOUNT_NO}-compact2.png?addInfo=Thanh%20toan&accountName={ACCOUNT_NAME}"

    embed = discord.Embed(
        title="💸 Thanh toán",
        description="Quét mã để chuyển khoản",
        color=0x00ff99
    )
    embed.set_image(url=qr_url)
    embed.add_field(name="Ngân hàng", value="Vietcombank", inline=True)
    embed.add_field(name="STK", value=ACCOUNT_NO, inline=True)

    await interaction.response.send_message(embed=embed)

bot.run(TOKEN)