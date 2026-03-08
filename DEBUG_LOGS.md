# 📋 DEBUG 日誌使用指南

## 概述

本項目配備了完整的 DEBUG 日誌系統，在**本地**和 **GitHub Actions** 中均可使用。

- **本地環境**：日誌保存到 `logs/debug.log` 及控制台
- **GitHub Actions**：日誌輸出到 Actions 執行日誌（可在 GitHub 網頁查看）

## 日誌位置

### 本地環境
```
logs/
└── debug.log          # 詳細 DEBUG 日誌（自動滾動，最多 3 個備份）
    debug.log.1
    debug.log.2
    debug.log.3
```

### GitHub Actions
在 GitHub 網頁查看：
```
https://github.com/你的用戶名/Proj001_DcMorningReport/actions
→ 點擊最新的 "Daily Briefing" 工作流
→ 展開 "Run Daily Briefing" 步驟查看完整 DEBUG 輸出
→ 如果失敗，查看 "查看 DEBUG 日誌" 和 "查看台股診斷日誌" 步驟
```

## 查看日誌

### 🖥️ 本地環境查看

#### 1️⃣ 查看日誌統計
```bash
python view_logs.py stats
```

#### 2️⃣ 查看台股相關日誌
```bash
python view_logs.py taiwan
```

#### 3️⃣ 查看最後 N 行日誌
```bash
python view_logs.py tail:100    # 查看最後 100 行
python view_logs.py tail:50     # 查看最後 50 行（預設）
```

#### 4️⃣ 查看錯誤日誌
```bash
python view_logs.py error
```

### ☁️ GitHub Actions 查看

1. 進入 GitHub Actions 日誌
2. 展開 **"Run Daily Briefing (含詳細 DEBUG 輸出)"** 步驟
3. 搜索關鍵字：
   - `開始獲取台股數據` - 台股獲取開始
   - `✅ 成功` - 成功獲取
   - `❌` - 失敗信息
   - `⚠️` - 警告信息

如果失敗，GitHub Actions 會自動執行額外的診斷步驟：
- **"查看 DEBUG 日誌"** - 顯示 `logs/debug.log` 的最後 100 行
- **"查看台股診斷日誌"** - 提取所有台股相關日誌

## 日誌格式說明

每行日誌包含以下信息：
```
時間 | 日誌級別 | 函數名:行號 | 訊息內容
```

示例：
```
2026-03-08 15:06:02 | DEBUG    | get_tw_stock_data:266 | 開始獲取台股數據: 0050
2026-03-08 15:06:03 | DEBUG    | get_tw_stock_data:279 |     收到歷史數據: 10 筆記錄
2026-03-08 15:06:03 | INFO     | get_financial_data:473 |   ✅ 0050 成功: NT$76.85
```

## 日誌級別

| 級別 | 說明 |
|------|------|
| **DEBUG** | 詳細診斷信息（開發/除錯用） |
| **INFO** | 一般信息（正常運行） |
| **WARNING** | 警告（某些功能無法運行） |
| **ERROR** | 錯誤（嚴重問題） |

## 📍 GitHub Actions 特有的 DEBUG 功能

本系統在 GitHub Actions 中添加了特殊處理：

### 1️⃣ 環境檢測
```
執行環境: GitHub Actions=true, CI=true
```

### 2️⃣ 自動重試機制
在 CI 環境中，yfinance 會自動重試最多 3 次，每次間隔 2 秒

### 3️⃣ 備選方案
如果 yfinance 在 GitHub Actions 中失敗，系統會嘗試：
- investpy API
- AKShare 數據源（開源金融數據）

### 4️⃣ 自動診斷輸出
工作流失敗時自動輸出：
- `logs/debug.log` 的最後 100 行
- 台股相關的所有日誌

## 台股無數據時的診斷步驟

### 本地環境診斷

#### 步驟 1: 檢查台股日誌
```bash
python view_logs.py taiwan
```

#### 步驟 2: 查找關鍵信息

✅ **成功的標記**：
```
✅ 0050 成功 (yfinance): 0050.TW => NT$76.85 (-0.71%)
```

❌ **常見失敗原因**：
```
✗ hist 為 None                          → yfinance 返回 None
✗ hist 為空 DataFrame                   → 無可用數據
✗ 記錄數 < 2: 1 筆                      → 數據不足（需要 2 筆）
✗ 異常價格: close=76, prev=-1           → 異常價格
⚠️ [JSON 解析失敗] Yahoo Finance 被限制  → 403/429/502
⚠️ [連線超時] 網路連接問題                → 無法連接
```

#### 步驟 3: 根據錯誤採取行動

| 錯誤 | 原因 | 解決方案 |
|------|------|---------|
| JSON 解析失敗 | Yahoo Finance 限制 (403/429) | 等待數分鐘後重試 |
| hist 為 None | yfinance 連線失敗 | 檢查網路連接 |
| 記錄數 < 2 | 代碼無效或已下市 | 確認代碼（如 0050、2330） |

### GitHub Actions 診斷

#### 步驟 1: 進入 Actions 頁面
```
GitHub → Actions → Daily Briefing → 最新工作流
```

#### 步驟 2: 查看執行日誌
- 展開 **"Run Daily Briefing"** 步驟查看完整輸出
- 查看 **"查看 DEBUG 日誌"** 步驟（失敗時自動執行）
- 查看 **"查看台股診斷日誌"** 步驟（失敗時自動執行）

#### 步驟 3: 搜索關鍵字
使用瀏覽器搜索功能（Ctrl+F）搜索：
- `開始獲取台股數據: 0050`
- `✅ 成功 (yfinance)`
- `❌` 或 `⚠️` 標記

## 日誌輪換

- 檔案大小達 5MB 時自動啟動新日誌
- 保留最近 3 個備份
- 舊日誌自動刪除

## 常見問題

**Q: 為什麼本地成功，GitHub Actions 失敗？**  
A: GitHub Actions 使用 Linux 環境，且 IP 可能被 Yahoo Finance 限制。系統會自動重試和使用備選方案。

**Q: GitHub Actions 中可以看到 DEBUG 日誌嗎？**  
A: 可以！所有 DEBUG 訊息會輸出到 Actions 日誌。如果失敗，會自動顯示 `logs/debug.log`。

**Q: 日誌文件太大怎麼辦？**  
A: 自動輪換機制會保留最新的 3 個備份，舊日誌自動刪除。

**Q: 如何實時監控本地日誌？**  
A: 使用以下命令持續監控：
```bash
Get-Content -Path logs/debug.log -Wait  # PowerShell
tail -f logs/debug.log                    # bash/Linux
```

**Q: 日誌涵蓋所有 API 調用嗎？**  
A: 是的，每個 API（yfinance、CoinGecko、exchangerate-api 等）都有對應的 DEBUG 日誌。

---

**最後更新**: 2026-03-08  
**版本**: 2.0 (GitHub Actions 支援版)

### 3️⃣ 查看最後 N 行日誌

```bash
python view_logs.py tail:100    # 查看最後 100 行
python view_logs.py tail:50     # 查看最後 50 行（預設）
```

### 4️⃣ 查看錯誤日誌

```bash
python view_logs.py error
```

這會顯示所有包含 Exception、Error 或 Warning 的日誌。

## 日誌格式說明

每行日誌包含以下信息：

```
時間 | 日誌級別 | 函數名:行號 | 訊息內容
```

示例：

```
2026-03-08 15:06:02 | DEBUG    | get_tw_stock_data:266 | 開始獲取台股數據: 0050
2026-03-08 15:06:03 | DEBUG    | get_tw_stock_data:279 |     收到歷史數據: 10 筆記錄
2026-03-08 15:06:03 | INFO     | get_financial_data:473 |   ✅ 0050 成功: NT$76.85
```

## 日誌級別

| 級別        | 說明                        |
| ----------- | --------------------------- |
| **DEBUG**   | 詳細診斷信息（開發/除錯用） |
| **INFO**    | 一般信息（正常運行）        |
| **WARNING** | 警告（某些功能無法運行）    |
| **ERROR**   | 錯誤（嚴重問題）            |

## 台股無數據時的診斷步驟

當台股顯示無數據時：

### 步驟 1: 檢查台股日誌

```bash
python view_logs.py taiwan
```

### 步驟 2: 查找關鍵信息

查找以下模式：

✅ **成功的標記**：

```
✅ 成功: 0050.TW => 價格: 76.85, 漲跌: -0.71%
```

❌ **失敗原因**：

- `✗ hist 為 None` - yfinance 返回 None（API 問題）
- `✗ hist 為空 DataFrame` - 未收到數據
- `✗ hist 記錄數 < 2` - 數據不足（需要至少 2 筆計算漲跌）
- `✗ 收盤價 <= 0` - 異常價格
- `異常: JSONDecodeError` - Yahoo Finance 返回 HTML 錯誤頁面（通常是 403/429）

### 步驟 3: 分析錯誤

常見原因及解決方案：

| 錯誤            | 原因                         | 解決方案                  |
| --------------- | ---------------------------- | ------------------------- |
| JSONDecodeError | Yahoo Finance 限制 (403/429) | 等待數分鐘後重試          |
| hist 為 None    | yfinance 連線失敗            | 檢查網絡連接              |
| 記錄數 < 2      | 代碼無效或已下市             | 確認代碼（如 0050、2330） |

## 日誌輪換

- 檔案大小達 5MB 時自動啟動新日誌
- 保留最近 3 個備份
- 舊日誌自動删除

## IT 支持：完整日誌内容

分享 `logs/debug.log` 的完整内容時：

```bash
# 查看完整日誌
Get-Content logs/debug.log
```

或直接在 VS Code 中打開 `logs/debug.log` 查看。

## 開發者：啟用更多 DEBUG 訊息

如需更詳細的 log，可以在 `main.py` 中調整 logging 級別：

```python
file_handler.setLevel(logging.DEBUG)  # 已預設為 DEBUG
```

## 常見問題

**Q: 日誌文件太大怎麼辦？**  
A: 自動輪換機制會保留最新的 3 個備份，舊日誌自動删除。

**Q: 可以實時監控日誌嗎？**  
A: 可以，使用以下命令持續監控：

```bash
Get-Content -Path logs/debug.log -Wait
```

**Q: 日誌是機密的嗎？**  
A: 日誌包含金融數據和時間戳，避免公開分享敏感日誌。

---

**最後更新**: 2026-03-08  
**版本**: 1.0
