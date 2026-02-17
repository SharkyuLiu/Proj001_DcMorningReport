#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""測試金融數據獲取"""

import sys
sys.path.insert(0, '.')

from main import get_financial_data, format_message, get_weather, get_reminders, get_vocabulary
import json

print("🧪 測試金融數據獲取\n")

print("=" * 50)
print("1️⃣ 獲取天氣數據...")
print("=" * 50)
weather = get_weather()
if "error" in weather:
    print(f"❌ {weather['error']}")
else:
    print(f"✅ 台中市溫度: {weather.get('current_temp')}°C")

print("\n" + "=" * 50)
print("2️⃣ 獲取提醒事項...")
print("=" * 50)
reminders = get_reminders()
print(f"✅ 找到 {len(reminders)} 項提醒")

print("\n" + "=" * 50)
print("3️⃣ 獲取金融數據...")
print("=" * 50)
financial = get_financial_data()

print("\n\n📊 **金融數據概览**:\n")
for ticker, data in financial.items():
    if "error" not in data:
        symbol = "📈" if data["change_pct"] >= 0 else "📉"
        price = data["price"]
        change = data["change_pct"]
        print(f"  ✅ {ticker:10s}: ${price:>10} {symbol} {change:>7.2f}%")
    else:
        print(f"  ❌ {ticker:10s}: {data['error']}")

print(f"\n\n成功獲取: {sum(1 for v in financial.values() if 'error' not in v)}/{len(financial)} 個商品")

print("\n" + "=" * 50)
print("4️⃣ 獲取英文單字...")
print("=" * 50)
vocab = get_vocabulary()
print(f"✅ 隨機抽取 {len(vocab)} 個單字")

print("\n" + "=" * 50)
print("5️⃣ 生成訊息...")
print("=" * 50)
message = format_message(weather, reminders, financial, vocab)
print(message[:500])
print("\n[... 訊息已截斷 ...]")
