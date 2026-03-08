# 📋 DEBUG 日誌使用指南

## 概述

本項目現在配備了完整的 DEBUG 日誌系統，以幫助追蹤和診斷問題。所有日誌自動保存到 `logs/debug.log`。

## 日誌位置

```
logs/
└── debug.log          # 詳細 DEBUG 日誌（自動滾動，最多 3 個備份）
    debug.log.1
    debug.log.2
    debug.log.3
```

## 查看日誌

### 1️⃣ 查看日誌統計

```bash
python view_logs.py stats
```

輸出示例：
```
📊 日誌統計

  總行數:    49
  DEBUG:     32
  INFO:      15
  WARNING:   2
  ERROR:     0
```

### 2️⃣ 查看台股相關日誌

遇到台股數據問題時，使用此命令：

```bash
python view_logs.py taiwan
```

這會顯示所有與台股 (0050, 2330) 相關的日誌，包括：
- 初始化 Ticker 物件是否成功
- 收到多少筆歷史數據
- 計算漲跌的原始價格
- 最終成功或失敗的原因

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

| 級別 | 說明 |
|------|------|
| **DEBUG** | 詳細診斷信息（開發/除錯用） |
| **INFO** | 一般信息（正常運行） |
| **WARNING** | 警告（某些功能無法運行） |
| **ERROR** | 錯誤（嚴重問題） |

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

| 錯誤 | 原因 | 解決方案 |
|------|------|---------|
| JSONDecodeError | Yahoo Finance 限制 (403/429) | 等待數分鐘後重試 |
| hist 為 None | yfinance 連線失敗 | 檢查網絡連接 |
| 記錄數 < 2 | 代碼無效或已下市 | 確認代碼（如 0050、2330） |

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
