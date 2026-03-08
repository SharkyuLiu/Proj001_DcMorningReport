# ⏰ 定時功能使用指南

## 功能說明

程式現在支援兩種運行模式：

### 1️⃣ **一次性運行**（適合測試）
```bash
python main.py
```
執行一次，然後退出。

### 2️⃣ **定時模式**（適合生產環境）
```bash
python main.py --schedule
```
會在各設定時間自動執行，持續運行。

---

## 定時設定

目前設定的報告時間：
- **06:30** - 早晨第一份報告
- **07:00** - 早晨第二份報告

### 修改報告時間

編輯 `main.py` 中的 `main()` 函數：

```python
# 找到這段程式碼
schedule.every().day.at("06:30").do(send_daily_report)
schedule.every().day.at("07:00").do(send_daily_report)

# 改成你想要的時間，例如：
schedule.every().day.at("06:00").do(send_daily_report)  # 改成 06:00
schedule.every().day.at("07:30").do(send_daily_report)  # 改成 07:30
```

---

## 在 Windows 上持續運行

### 方式 1：Windows 工作排程器（推薦）

1. **打開工作排程器**
   ```
   開始 → 搜尋 "工作排程器" → 開啟
   ```

2. **建立基本工作**
   - 名稱：`DcMorningReport`
   - 位置：`\`

3. **設定觸發器**
   - 設定為「電腦啟動時」或「登入時」

4. **設定動作**
   - 程式：`C:\Users\Liu\Desktop\Projects\Proj001_DcMorningReport\.venv\Scripts\python.exe`
   - 引數：`C:\Users\Liu\Desktop\Projects\Proj001_DcMorningReport\main.py --schedule`
   - 開始於：`C:\Users\Liu\Desktop\Projects\Proj001_DcMorningReport`

5. **條件**
   - ✅ 電腦在電源上時執行
   - ❌ 關閉「只有在使用者登入時才執行」（允許在背景運行）

### 方式 2：後台服務（需要管理員權限）

使用 `nssm` (Non-Sucking Service Manager)：

```powershell
# 1. 下載 nssm：https://nssm.cc/download
# 2. 將 nssm.exe 複製到 C:\Windows\System32

# 3. 安裝服務
nssm install DcMorningReport "C:\Users\Liu\Desktop\Projects\Proj001_DcMorningReport\.venv\Scripts\python.exe" "main.py --schedule"

# 4. 啟動服務
nssm start DcMorningReport

# 5. 檢視日誌
nssm query DcMorningReport
```

### 方式 3：簡單的 PowerShell 腳本

建立 `run_scheduler.bat`：

```batch
@echo off
cd /d C:\Users\Liu\Desktop\Projects\Proj001_DcMorningReport
.\.venv\Scripts\python.exe main.py --schedule
```

然後設定工作排程器執行此文件。

---

## 故障排除

### 1️⃣ 定時任務未執行

**檢查清單：**
- ☑️ 已設定 `DISCORD_WEBHOOK_URL` 環境變數
- ☑️ 已設定 `FINNHUB_API_KEY` 環境變數（可選）
- ☑️ 工作排程器已啟用該任務
- ☑️ 完整路徑正確無誤
- ☑️ Python 環境變數已配置

### 2️⃣ 程式執行但沒有發送訊息

執行測試看是否有錯誤：
```bash
python test_financial.py
```

查看輸出是否有紅色的 ❌ 符號。

### 3️⃣ 無法找到 schedule 模組

確保已安裝依賴：
```bash
pip install schedule
```

---

## 監控日誌

### 方式 1：重定向輸出到文件

修改 PowerShell 腳本或工作排程器的動作，將輸出重定向到檔案：

```batch
.\.venv\Scripts\python.exe main.py --schedule >> C:\logs\dc_report.log 2>&1
```

### 方式 2：使用 PrintScreen 或其他日誌工具

在 Python 程式中新增日誌記錄：

```python
import logging

logging.basicConfig(
    filename='dc_report.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logging.info("報告已發送")
```

---

## 常見問題

**Q1: 為什麼定時任務沒有在6:30和7:00執行？**  
A: 檢查系統時鐘是否正確，以及工作排程器是否啟用。

**Q2: 可以添加更多報告時間嗎？**  
A: 可以，在 main() 函數中添加更多 `schedule.every().day.at()` 行。

**Q3: 如何停止定時服務？**  
A: 在工作排程器中禁用任務，或 Ctrl+C 終止程式（如果在前景執行）。

**Q4: 是否可以在特定日期跳過報告？**  
A: 可以在 `send_daily_report()` 函數中添加日期檢查邏輯。

---

## 進階配置

### 監控程式健康狀況

```python
# 在 main.py 中添加此函數
def check_report_status(webhook_url):
    """定期發送狀態檢查訊息"""
    msg = "✅ 晨報服務正在正常運行"
    requests.post(webhook_url, json={"content": msg})

# 然後在定時中添加
schedule.every().day.at("06:00").do(check_report_status, webhook_url)
```

### 錯誤通知

```python
def send_error_alert(error_msg, webhook_url):
    """發送錯誤警報"""
    msg = f"🚨 晨報服務出現錯誤:\n{error_msg}"
    requests.post(webhook_url, json={"content": msg})

# 在 try-except 中使用
try:
    send_daily_report()
except Exception as e:
    send_error_alert(str(e), webhook_url)
```

---

祝使用愉快！🎉
