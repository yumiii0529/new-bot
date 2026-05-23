import discord
import aiohttp
import random
import io
import os
from dotenv import load_dotenv

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
client = discord.Client(intents=intents)

# ---------------- 髒話 ----------------
bad_words = ["幹", "靠北", "機掰", "fuck", "shit"]
funny_replies = [
    "你那麼兇是要跟本兔打架嗎(#ﾟДﾟ)",
    "是在兇屁喔(´-ω-)",
    "誰跟你說可以講髒話的，小屁孩，八嘎鴨肉(╯°Д°）╯︵ /(.□ . )",
    "寶子，嘴巴這麼賤，是不是在等我抽你⁄(⁄ ⁄ ⁄ω⁄ ⁄ ⁄)⁄",
    "你的嘴巴需要洗洗，還是我幫你？🧼"
]

@client.event
async def on_message(message):
    if message.author == client.user:
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

# ---------------- 歡迎訊息 ----------------
@client.event
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

# ---------------- 啟動 ----------------
@client.event
async def on_ready():
    print(f'🤖 機器人已上線：{client.user}')

client.run(TOKEN)
