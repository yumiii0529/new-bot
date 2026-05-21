# 喵喵 Discord 機器人 🐱

一個可愛的 Discord 機器人，提供 Roblox 帳號查詢、歡迎訊息和互動功能。

## 功能

- 🐾 **Roblox 帳號查詢** - 透過 Bloxlink API 查詢使用者的 Roblox 資料
- 😺 **歡迎訊息** - 新成員加入時發送可愛的歡迎訊息和貓咪圖片
- 💬 **髒話回覆** - 友善的方式回覆髒話
- 👋 **打招呼** - 回應「你好」訊息

## 安裝

### 1. 複製 `.env.example` 為 `.env`

```bash
cp .env.example .env
```

### 2. 配置環境變量

編輯 `.env` 文件，填入：

- **DISCORD_TOKEN**: 從 [Discord Developer Portal](https://discord.com/developers/applications) 獲取
  1. 建立新應用程式
  2. 進入 Bot 頁面，點擊 "Add Bot"
  3. 在 TOKEN 下方點擊 "Copy" 複製 Token

- **BLOXLINK_API_KEY**: 從 [Bloxlink Developer Portal](https://bloxlink.com/developer) 獲取
  1. 登入或註冊
  2. 建立新應用程式
  3. 複製 API Key

### 3. 安裝依賴

```bash
pip install -r requirements.txt
```

## 使用

### 啟動機器人

```bash
python bot.py
```

機器人應該會輸出：
```
🤖 機器人已上線：YourBotName#0000
```

### 命令

- `!查詢` - 查詢你的 Roblox 資料
- `!查詢 @使用者` - 查詢指定使用者的 Roblox 資料
- `你好` - 機器人會回應你

## Discord 機器人設置

### 必需權限

在 [Discord Developer Portal](https://discord.com/developers/applications) 中：

1. 進入 OAuth2 > URL Generator
2. 選擇 Scopes: `bot`
3. 選擇 Permissions:
   - Send Messages
   - Embed Links
   - Attach Files
   - Read Message History
4. 複製生成的 URL 並在瀏覽器中開啟，將機器人邀請到伺服器

### 必需 Intents

確保在 Developer Portal 的 "Bot" 頁面啟用：
- Message Content Intent
- Server Members Intent

## 專案結構

```
.
├── bot.py              # 主要機器人代碼
├── requirements.txt    # Python 依賴
├── .env.example       # 環境變量範例
├── .gitignore         # Git 忽略文件
└── README.md          # 說明文檔
```

## 故障排除

### 機器人無法連接

- 檢查 `DISCORD_TOKEN` 是否正確
- 確保機器人已新增至伺服器
- 檢查機器人是否有必需的權限

### Roblox 查詢失敗

- 檢查 `BLOXLINK_API_KEY` 是否正確
- 確保使用者已在 Discord 上綁定 Roblox 帳號
- 檢查 Bloxlink API 是否可用

## 許可

MIT License

## 支援

如有問題，請提出 issue 或 PR！