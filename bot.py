import discord
import aiohttp
import random
import io
import os
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

if not TOKEN or TOKEN == "your_discord_token_here":
    raise RuntimeError(
        "DISCORD_TOKEN is not set or invalid. "
        "Please set the correct Discord bot token in environment variables."
    )

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

# ---------------- 髒話 ----------------
bad_words = ["幹", "靠北", "機掰", "fuck", "shit"]
funny_replies = [
    "你那麼兇是要跟本兔打架嗎(#ﾟДﾟ)",
    "是在兇屁喔(´-ω-)",
    "誰跟你說可以講髒話的，小屁孩，八嘎鴨肉(╯°Д°）╯︵ /(.□ . )",
    "寶子，嘴巴這麼賤，是不是在等我抽你⁄(⁄ ⁄ ⁄ω⁄ ⁄ ⁄)⁄",
    "你的嘴巴需要洗洗，還是我幫你？🧼"
]

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    msg_content = message.content.lower()
    
    # 髒話回覆
    if any(word in msg_content for word in bad_words):
        reply = random.choice(funny_replies)
        await message.channel.send(f"{message.author.mention} {reply}")
        return
    
    # 打招呼
    if msg_content == "你好":
        await message.channel.send("你好哇，親愛的！")
        return
    
    # 允許指令處理
    await bot.process_commands(message)

# ---------------- 歡迎訊息 ----------------
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
                file = discord.File(fp=io.BytesIO(img_data), filename="welcome_cat.jpg")
                
                welcome_messages = [
                    "恭迎我們尊貴的主人 {name}，喵！",
                    "喵嗚～歡迎 {name} 降臨本咖啡廳！",
                    "{name} ㄤㄤ，主人大人終於出現啦！🎉",
                    "{name}主人好，今天也請多多指教喵！",
                    "貓貓張開雙爪擁抱 {name}主人 🐾"
                ]
                
                welcome_description = (
                    "聊天區請友善交流！\n"
                    "請閱讀伺服器規則 📜，\n"
                    "記得去身分組區領身分組喵！🐾"
                )
                
                title = random.choice(welcome_messages).format(name=member.name)
                embed = discord.Embed(
                    title=f"🎉 {title}",
                    description=welcome_description,
                    color=discord.Color.random()
                )
                embed.set_image(url="attachment://welcome_cat.jpg")
                await channel.send(file=file, embed=embed)
            else:
                await channel.send(f"🎉 歡迎 {member.mention}！但今天貓貓罷工了 😿")

# ---------------- 公告指令 ----------------
@bot.command(name="公告")
async def announcement(ctx):
    await ctx.send("""
☕ 喵舍・店內守則

歡迎來到喵舍 
這裡是提供聊天、陪伴、交友與遊戲交流的空間。

希望每位來到這裡的人，
都能在舒服的氛圍中好好待著。

為了維持店內環境與大家的體驗，
請遵守以下規則 ✦

꒰ঌ ♡ ໒꒱ ┈┈┈┈┈┈┈

1｜尊重每位成員
禁止任何形式的人身攻擊、歧視、惡意嘲諷、造謠與挑釁行為。

2｜避免公開爭執
若有私人糾紛請私下處理，
不要影響公開聊天室與語音房氣氛。

3｜禁止騷擾行為
包含持續糾纏、洗訊息、惡意跟房、
不適當調情與讓人感到不舒服的互動。

4｜禁止散播不實資訊
請勿刻意帶風向、造謠或散播假消息。

5｜禁止廣告與引流
未經允許不得宣傳其他群組、
社群、商業內容或外部連結。

6｜公開頻道請注意尺度
禁止過度裸露、限制級內容、
黃色圖片影片與過激性暗示言論。

7｜請勿大量洗頻
包含大量貼圖、符號、重複訊息與惡意刷版。

8｜尊重語音房成員
進入私人語音房前請先詢問，
也禁止炸麥、故意吵鬧與干擾他人。

9｜善用標註功能
禁止隨意 @everyone、
或大量標註成員造成干擾。

10｜管理團隊保有最終處理權
若有影響社群氛圍與秩序之行為，
管理員將視情況進行處理。

꒰ঌ ♡ ໒꒱ ┈┈┈┈┈┈┈

若遇到問題、騷擾或違規情況，
請至客服單聯繫管理員。

感謝每位願意一起維護喵舍氛圍的你 ☕
""")

# ---------------- 啟動 ----------------
@bot.event
async def on_ready():
    print(f'🤖 機器人已上線：{bot.user}')

bot.run(TOKEN)
