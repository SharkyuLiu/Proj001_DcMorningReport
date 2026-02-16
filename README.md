# 每日早晨個人助理

> 台北時間每日早上 7:30 自動推送一份個人助理報告到 Discord

## 📋 功能特性

✅ **天氣預報** - 台中市實時天氣、溫度、降雨機率（使用免費的 open-meteo API）  
✅ **今日提醒** - 讀取 `reminders.txt` 中的提醒事項  
✅ **金融走勢** - 美股、加密貨幣、匯率實時行情  
✅ **英文單字** - 每日隨機推送 10 個 TOEIC 900 級商用單字  
✅ **自動化推送** - 使用 GitHub Actions 免費部署，無需自己的服務器

## 📦 專案結構

```
Proj001_DcMorningReport/
├── main.py                          # 主程式
├── requirements.txt                 # Python 相依套件
├── reminders.txt                    # 每日提醒事項（可自訂）
├── .github/
│   └── workflows/
│       └── daily_briefing.yml       # GitHub Actions 工作流配置
└── README.md                        # 本文件
```

## 🚀 快速開始

### 1️⃣ 本地測試

```bash
# 複製此專案
git clone <your-repo-url>
cd Proj001_DcMorningReport

# 安裝相依套件
pip install -r requirements.txt

# 設定環境變數（需要 Discord Webhook URL）
# Windows PowerShell:
$env:DISCORD_WEBHOOK_URL = "your-webhook-url-here"

# Linux/Mac:
export DISCORD_WEBHOOK_URL="your-webhook-url-here"

# 執行腳本
python main.py
```

### 2️⃣ 在 GitHub 上部署（推薦）

#### 步驟 1: 推送到 GitHub

```bash
git add .
git commit -m "初始化每日早晨助理"
git push origin main
```

#### 步驟 2: 獲取 Discord Webhook URL

在 Discord 伺服器中：

1. 右鍵點選要接收報告的頻道
2. 選擇「編輯頻道」(Edit Channel)
3. 進入「整合」(Integrations) → 「Webhooks」
4. 點擊「建立 Webhook」(Create Webhook)
5. 設定一個名稱（例如 "Morning Report Bot"）
6. 點擊「複製 Webhook URL」
7. 妥善保管此 URL（不要公開分享）

#### 步驟 3: 設定 GitHub Secrets

1. 進入你的 GitHub 倉庫
2. 設定 → Secrets and variables → Actions
3. 點擊「New repository secret」
4. 名稱: `DISCORD_WEBHOOK_URL`
5. 值: 貼上你的 Discord Webhook URL
6. 點擊「Add secret」

#### 步驟 4: 測試工作流

1. 進入倉庫的「Actions」標籤
2. 選擇「Daily Briefing」工作流
3. 點擊「Run workflow」→「Run workflow」（手動觸發）
4. 等待執行完畢，檢查 Discord 頻道是否收到訊息

#### 步驟 5: 完成！

從現在起，報告會在每天台北時間 7:30 自動發送。

## ⚙️ 自訂設定

### 修改提醒事項

編輯 `reminders.txt` 文件，每行一個提醒：

```
準備晨會開會物品
檢查郵件和 Slack 通知
複習今日重點工作
```

### 修改監控的股票

在 `main.py` 中修改這些清單：

```python
stocks = ["MU", "PLTR", "ORCL", "TSLA", "NVDA"]  # 美股代號
crypto = ["BTC-USD", "ETH-USD"]                   # 加密貨幣代號
currency = ["TWD=X"]                              # 匯率代號
```

### 修改執行時間

在 `.github/workflows/daily_briefing.yml` 中修改 cron 表達式：

```yaml
schedule:
  - cron: "30 23 * * *" # 當前: UTC 23:30 (台北 7:30)
```

Cron 語法: `分 時 日 月 周`

- `30 23 * * *` = 每天 UTC 23:30（台北時間是 UTC+8，所以是隔天 7:30）
- `0 8 * * 1-5` = 週一至週五 UTC 08:00
- `0 22 * * *` = 每天 UTC 22:00（台北時間 6:00 早晨）

## 📊 API 說明

### open-meteo（天氣預報）

- 完全免費，無需 API Key
- 網址: https://open-meteo.com
- 精度: 約 10km 範圍

### yfinance（股票和加密貨幣）

- 免費獲取雅虎財經數據
- 支持股票、加密貨幣、匯率
- 注意: 有時會受限制，大量請求時可能延遲

### Discord Webhooks

- Discord 原生功能，免費
- 無需 Discord 開發者帳戶
- 支持 Markdown 格式化

## 🔒 安全性建議

✅ **始終使用環境變數存儲敏感信息**（如 Webhook URL）  
✅ **不要在代碼或提交中硬核 Webhook URL**  
✅ **定期檢查 GitHub Secrets 的有效期**  
✅ **如果不小心洩露 Webhook，立即在 Discord 中重新生成**

## 🐛 故障排查

### 訊息沒有發送到 Discord

1. 檢查 GitHub Actions 執行日誌
   - 進入 Actions → 選擇最近的運行 → 點擊「Run Daily Briefing」步驟
2. 確認 Webhook URL 是否有效
   - 在本地測試: `python main.py`（需要設定環境變數）
3. 檢查 Discord 頻道權限
   - 確認 Bot 有權限在該頻道發送訊息

### API 連接超時

- `yfinance` 有時會很慢，工作流已設定 10 秒超時
- 如果經常超時，可以增加超時時間或減少監控的股票數量

### cron 時間有誤

- GitHub Actions 使用 UTC 時區
- 台北時間 (UTC+8) 早上 7:30 = UTC 前一天 23:30
- 時間不準確時，使用 https://crontab.guru 驗證

## 📝 修改歷史

- **v1.0** (2024-02-17) - 初始版本

## 📄 授權

MIT License - 自由使用和修改

## 💡 進階用法

### 發送多個 Discord 頻道

在 GitHub Secrets 中添加多個 Webhook URL，然後在 `main.py` 中迴圈發送：

```python
webhook_urls = os.environ.get("DISCORD_WEBHOOK_URL").split(";")
for url in webhook_urls:
    send_discord_message(message, url)
```

### 添加更多數據源

可以擴展添加：

- 新聞頭條（使用 NewsAPI）
- 待辦事項（從本地 JSON 讀取）
- 運動賽事結果
- 習慣追蹤

---

有任何問題或建議，歡迎提交 Issue 或 Pull Request！🎉
