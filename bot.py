import discord
from discord.ext import commands, tasks
from discord import app_commands
import aiohttp
import random
import io
import os
import sqlite3
import time
from dotenv import load_dotenv

# ================= TOKEN =================

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN 沒有設定")

# ================= BOT 設定 =================

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

# ================= 資料庫 =================

conn = sqlite3.connect("levels.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    chat_xp INTEGER DEFAULT 0,
    chat_level INTEGER DEFAULT 1,
    voice_xp INTEGER DEFAULT 0,
    voice_level INTEGER DEFAULT 1
)
""")

conn.commit()

# ================= 等級設定 =================

cooldowns = {}

LEVEL_ROLES = {
    5: "🌙 初來乍到",
    10: "🐾 夜行旅人",
    20: "💗 心動常客",
    30: "🐈 魅夜住民",
    40: "✨ 靈魂共鳴",
    50: "👑 貓舍傳說"
}

def xp_needed(level):
    return int(100 * (level ** 1.5))

# ================= 髒話系統 =================

bad_words = [
    "幹",
    "靠北",
    "機掰",
    "fuck",
    "shit"
]

funny_replies = [
    "你那麼兇是要跟本兔打架嗎 (#ﾟДﾟ)",
    "是在兇屁喔(´-ω-`)",
    "誰跟你說可以講髒話的，小屁孩",
    "寶子，嘴巴這麼賤，是不是在等我抽你⁄(⁄ ⁄ ⁄ω⁄ ⁄ ⁄)⁄",
    "你的嘴巴需要洗洗，還是我幫你？🧼"
]

# ================= 使用者資料 =================

def get_user(user_id):

    cursor.execute(
        "SELECT * FROM users WHERE user_id = ?",
        (user_id,)
    )

    user = cursor.fetchone()

    if not user:

        cursor.execute(
            "INSERT INTO users (user_id) VALUES (?)",
            (user_id,)
        )

        conn.commit()

        cursor.execute(
            "SELECT * FROM users WHERE user_id = ?",
            (user_id,)
        )

        user = cursor.fetchone()

    return user

# ================= 升級系統 =================

async def check_chat_level_up(message, xp, level):

    while xp >= xp_needed(level):

        level += 1

        await message.channel.send(
            f"🎉 {message.author.mention} 升到了 Lv.{level}！"
        )

        # 自動給身分組
        for req_level, role_name in LEVEL_ROLES.items():

            if level >= req_level:

                role = discord.utils.get(
                    message.guild.roles,
                    name=role_name
                )

                if role and role not in message.author.roles:

                    try:
                        await message.author.add_roles(role)
                    except:
                        pass

    return level

async def check_voice_level_up(member, xp, level):

    while xp >= xp_needed(level):

        level += 1

        try:
            await member.send(
                f"🎤 你的語音等級升到 Lv.{level}！"
            )
        except:
            pass

    return level

# ================= 訊息事件 =================

@bot.event
async def on_message(message):

    if message.author.bot:
        return

    msg_content = message.content.lower()

    # ---------- 髒話 ----------

    if any(word in msg_content for word in bad_words):

        reply = random.choice(funny_replies)

        await message.channel.send(
            f"{message.author.mention} {reply}"
        )

    # ---------- 打招呼 ----------

    if msg_content == "你好":

        await message.channel.send(
            "你好哇，親愛的！"
        )

    # ---------- 聊天等級 ----------

    user_id = message.author.id

    current_time = time.time()

    if user_id not in cooldowns:
        cooldowns[user_id] = 0

    # 30 秒冷卻

    if current_time - cooldowns[user_id] >= 30:

        user = get_user(user_id)

        xp = user[1]
        level = user[2]

        gain = random.randint(5, 15)

        xp += gain

        level = await check_chat_level_up(
            message,
            xp,
            level
        )

        cursor.execute("""
        UPDATE users
        SET chat_xp = ?, chat_level = ?
        WHERE user_id = ?
        """, (
            xp,
            level,
            user_id
        ))

        conn.commit()

        cooldowns[user_id] = current_time

    await bot.process_commands(message)

# ================= 語音等級 =================

@tasks.loop(minutes=1)
async def voice_xp_loop():

    for guild in bot.guilds:

        for vc in guild.voice_channels:

            members = [
                m for m in vc.members
                if not m.bot
            ]

            if len(members) == 0:
                continue

            for member in members:

                user = get_user(member.id)

                xp = user[3]
                level = user[4]

                gain = 2

                # 多人語音加成
                if len(members) >= 2:
                    gain += 1

                # 開麥加成
                if not member.voice.self_mute:
                    gain += 1

                xp += gain

                level = await check_voice_level_up(
                    member,
                    xp,
                    level
                )

                cursor.execute("""
                UPDATE users
                SET voice_xp = ?, voice_level = ?
                WHERE user_id = ?
                """, (
                    xp,
                    level,
                    member.id
                ))

                conn.commit()

# ================= Rank 指令 =================

@bot.tree.command(
    name="rank",
    description="查看你的等級"
)
async def rank(interaction: discord.Interaction):

    user = get_user(interaction.user.id)

    embed = discord.Embed(
        title=f"{interaction.user.name} 的等級資料",
        color=discord.Color.purple()
    )

    embed.add_field(
        name="💬 聊天等級",
        value=f"Lv.{user[2]} | XP: {user[1]}",
        inline=False
    )

    embed.add_field(
        name="🎤 語音等級",
        value=f"Lv.{user[4]} | XP: {user[3]}",
        inline=False
    )

    await interaction.response.send_message(
        embed=embed
    )

# ================= 排行榜 =================

@bot.tree.command(
    name="leaderboard",
    description="查看排行榜"
)
async def leaderboard(interaction: discord.Interaction):

    cursor.execute("""
    SELECT user_id, chat_level, voice_level
    FROM users
    ORDER BY (chat_level + voice_level) DESC
    LIMIT 10
    """)

    data = cursor.fetchall()

    embed = discord.Embed(
        title="🏆 排行榜",
        color=discord.Color.gold()
    )

    text = ""

    for i, row in enumerate(data, start=1):

        user = bot.get_user(row[0])

        if user is None:
            continue

        text += (
            f"#{i} {user.name}\n"
            f"💬 Lv.{row[1]} | 🎤 Lv.{row[2]}\n\n"
        )

    embed.description = text

    await interaction.response.send_message(
        embed=embed
    )

# ================= 歡迎訊息 =================

@bot.event
async def on_member_join(member):

    channel = member.guild.system_channel

    if not channel:
        return

    url = "https://cataas.com/cat/cute"

    async with aiohttp.ClientSession() as session:

        async with session.get(url) as resp:

            if resp.status == 200:

                img_data = await resp.read()

                file = discord.File(
                    fp=io.BytesIO(img_data),
                    filename="welcome_cat.jpg"
                )

                welcome_messages = [
                    "恭迎我們尊貴的主人 {name}，喵！",
                    "喵嗚～歡迎 {name} 降臨本咖啡廳！",
                    "{name} ㄤㄤ，主人大人終於出現啦！🎉",
                    "{name}主人好，今天也請多多指教喵！",
                    "貓貓張開雙爪擁抱 {name}主人 🐾"
                ]

                welcome_description = (
                    "聊天區請友善交流！\n"
                    "請閱讀伺服器規則 📜\n"
                    "記得去身分組區領身分組喵！🐾"
                )

                title = random.choice(
                    welcome_messages
                ).format(name=member.name)

                embed = discord.Embed(
                    title=f"🎉 {title}",
                    description=welcome_description,
                    color=discord.Color.random()
                )

                embed.set_image(
                    url="attachment://welcome_cat.jpg"
                )

                await channel.send(
                    file=file,
                    embed=embed
                )

            else:

                await channel.send(
                    f"🎉 歡迎 {member.mention}！"
                )

# ================= 啟動 =================

@bot.event
async def on_ready():

    await bot.tree.sync()

    if not voice_xp_loop.is_running():
        voice_xp_loop.start()

    print(f"🤖 機器人已上線：{bot.user}")

# ================= 啟動 BOT =================

bot.run(TOKEN)
