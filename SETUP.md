# 🚀 每日早晨助理報告 - 設置指南

## 📋 功能概覽

本專案收集以下數據並發送至 Discord：
- 🌤️ **天氣預報** (台中市) - Open-Meteo API
- 📝 **日程提醒** - 本地 `reminders.txt`
- 📈 **金融商品走勢**：
  - 🇹🇼 **台股** (0050、2330) - Yahoo Finance
  - 🇺🇸 **美股大盤** (VT、QQQ、SPY、DIA、EWT) - Finnhub API ⭐
  - 🇺🇸 **美股個股** (15 支) - Finnhub API ⭐
  - 🪙 **加密貨幣** (BTC、ETH) - CoinGecko API (免費)
  - 💱 **匯率** (美元兌新台幣) - exchangerate-api (免費)
- 📚 **TOEIC 900 級英文單字** (200 個隨機抽取)

---

## 🔧 環境要求

### 必須軟體
- Python 3.8+
- pip（Python 套件管理器）

### 必須環境變數

#### 1. **Discord Webhook URL** (必需)
用於發送訊息到 Discord 頻道。

**取得方法：**
1. 在 Discord 伺服器中建立/選擇頻道
2. 右鍵點選頻道 → 編輯頻道
3. 整合 → Webhooks → 新增 Webhook
4. 複製 Webhook URL

**設定方式：**
```powershell
[Environment]::SetEnvironmentVariable("DISCORD_WEBHOOK_URL", "https://discord.com/api/webhooks/...", "User")
```

#### 2. **Finnhub API Key** (可選，但強烈建議獲取美股數據)
用於獲取準即時美股報價。

**取得方法：**
1. 前往 https://finnhub.io
2. 註冊免費帳號
3. 複製 API Key

**設定方式：**
```powershell
[Environment]::SetEnvironmentVariable("FINNHUB_API_KEY", "your_key_here", "User")
```

⚠️ **沒有此 Key 會無法獲取美股數據！**

---

## 📦 安裝依賴

```bash
pip install -r requirements.txt
```

### 依賴清單
- `requests==2.31.0` - HTTP 請求
- `yfinance==0.2.32` - Yahoo Finance 數據（台股備選）

**免費 API（不需安裝）：**
- CoinGecko（加密貨幣）
- exchangerate-api（匯率）
- Open-Meteo（天氣）

---

## 🎯 使用方式

### 方式 1：測試單次執行
```bash
python main.py
```

### 方式 2：定時執行（Windows 工作排程）
```powershell
# 1. 打開工作排程器
taskscheduler

# 2. 建立基本工作
# - 名稱：DcMorningReport
# - 觸發器：每日早上 6:00
# - 動作：程式 → C:\Python312\python.exe
# - 引數：C:\Users\Liu\Desktop\Projects\Proj001_DcMorningReport\main.py
```

### 方式 3：測試模式（不發送 Discord）
```bash
python test_financial.py
```

---

## 📊 數據來源對應表

| 數據類型 | Ticker 範例 | API 來源 | 狀態 | 需要 Key |
|---------|-----------|---------|-----|---------|
| 台股 | 0050, 2330 | Yahoo Finance | 🔴 失效 | ❌ |
| 美股大盤 | QQQ, SPY | Finnhub | ✅ 正常 | ✅ |
| 美股個股 | NVDA, TSLA | Finnhub | ✅ 正常 | ✅ |
| 加密貨幣 | BTC-USD | CoinGecko | ✅ 正常 | ❌ |
| 匯率 | TWD=X | exchangerate-api | ✅ 正常 | ❌ |
| 天氣 | 台中市 | Open-Meteo | ✅ 正常 | ❌ |

---

## ⚠️ 常見問題

### Q1: 美股數據顯示 "無可用數據"
**原因：** 未設定 `FINNHUB_API_KEY` 環境變數  
**解決：** 參考上面的環境變數設定步驟

### Q2: 台股無法獲取  
**原因：** Yahoo Finance 目前不支援台灣股票的實時數據  
**替代方案：**
- 手動更新 `reminders.txt` 記錄台股價格
- 使用其他台股 API（如 TWSE 官方 API）

### Q3: Discord 訊息發送失敗
**檢查清單：**
1. ✅ Webhook URL 是否正確
2. ✅ 網路連線是否正常
3. ✅ Discord 頻道權限是否足夠

### Q4: 加密貨幣數據無法獲取
**原因：** CoinGecko API 伺服器暫時無法連線  
**解決：** 稍後重試（通常會自動恢復）

---

## 🔄 更新歷史

### v2.0 (2026-02-18)
- ✅ 添加 CoinGecko 加密貨幣 API
- ✅ 添加 exchangerate-api 匇率 API
- ✅ 分離數據來源邏輯
- ✅ 英文單字擴充至 200 個
- ♻️ 重組金融數據為台股/美股大盤/美股個股

### v1.0
- 初始版本

---

## 📞 技術支持

如遇問題，請檢查：
1. `test_financial.py` 的輸出信息
2. 環境變數設定
3. 網路連線
4. 各 API 官網狀態

---

## 📝 Reminders 格式

編輯 `reminders.txt`，每行一項提醒：

```
準備晨會開會物品
檢查郵件和 Slack 通知
複習今日重點工作
```

---

## 🎨 自訂選項

### 修改查詢股票代碼
編輯 `main.py` 中的 `get_financial_data()` 函數：

```python
tw_stocks = ["0050", "2330"]  # 修改此行
us_market = ["VT", "QQQ", "SPY", "DIA", "EWT"]  # 修改此行
us_stocks = ["QCOM", "ANET", "TSLA", ...]  # 修改此行
```

### 修改隨機英文單字數量
編輯 `get_vocabulary()` 函數：

```python
def get_vocabulary():
    return random.sample(VOCABULARY, min(15, len(VOCABULARY)))  # 改 15 為你想要的數量
```

---

祝使用愉快！🎉
