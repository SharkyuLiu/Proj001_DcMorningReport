import os
import requests
import random
import time
from datetime import datetime
from zoneinfo import ZoneInfo
import yfinance as yf

# 設定 User-Agent 避免被 API 限制
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

# TOEIC 900 級別商用單詞詞典（50 個）
VOCABULARY = [
    {"word": "Prudent", "meaning": "謹慎的；明智的", "usage": "Be prudent when making financial decisions.", "context": "商務"},
    {"word": "Meticulous", "meaning": "一絲不苟的；細心的", "usage": "A meticulous approach to project management is essential.", "context": "商務"},
    {"word": "Juxtapose", "meaning": "並列；對比", "usage": "The designer juxtaposed old and modern elements.", "context": "商務"},
    {"word": "Fortuitous", "meaning": "幸運的；偶然的", "usage": "Their meeting was a fortuitous encounter.", "context": "商務"},
    {"word": "Recalcitrant", "meaning": "不願合作的；頑固的", "usage": "The recalcitrant employee refused to follow protocols.", "context": "商務"},
    {"word": "Perspicacious", "meaning": "有洞察力的；敏銳的", "usage": "Her perspicacious analysis led to significant improvements.", "context": "商務"},
    {"word": "Ephemeral", "meaning": "短暫的；曇花一現的", "usage": "Social media trends are often ephemeral.", "context": "商務"},
    {"word": "Ameliorate", "meaning": "改善；緩和", "usage": "New policies will ameliorate working conditions.", "context": "商務"},
    {"word": "Obfuscate", "meaning": "使困惑；模糊", "usage": "Don't obfuscate the facts in your report.", "context": "商務"},
    {"word": "Serendipity", "meaning": "幸運巧合；天賜之福", "usage": "Finding that client was pure serendipity.", "context": "商務"},
    {"word": "Sycophant", "meaning": "阿諛奉承者；馬屁精", "usage": "Avoid becoming a sycophant in your workplace.", "context": "商務"},
    {"word": "Nebulous", "meaning": "模糊的；不清楚的", "usage": "The project goals are still nebulous.", "context": "商務"},
    {"word": "Pragmatic", "meaning": "實用主義的；務實的", "usage": "We need a pragmatic approach to solve this.", "context": "商務"},
    {"word": "Candid", "meaning": "誠實的；坦率的", "usage": "Please give me candid feedback on my presentation.", "context": "商務"},
    {"word": "Diligent", "meaning": "勤奮的；認真的", "usage": "Diligent work led to the project's success.", "context": "商務"},
    {"word": "Zealous", "meaning": "熱情的；狂熱的", "usage": "Her zealous approach inspired the entire team.", "context": "商務"},
    {"word": "Succinct", "meaning": "簡潔的；扼要的", "usage": "Keep your emails succinct and clear.", "context": "商務"},
    {"word": "Verbose", "meaning": "冗長的；啰嗦的", "usage": "Avoid being verbose in business communications.", "context": "商務"},
    {"word": "Paradigm", "meaning": "範例；典範", "usage": "This represents a paradigm shift in technology.", "context": "商務"},
    {"word": "Venerate", "meaning": "尊敬；崇敬", "usage": "Employees venerate the company's founder.", "context": "商務"},
    {"word": "Admonish", "meaning": "告誡；警告", "usage": "The manager admonished the team for missing deadlines.", "context": "商務"},
    {"word": "Belabor", "meaning": "費力地解釋；過度強調", "usage": "Don't belabor the point; we already understand.", "context": "商務"},
    {"word": "Cogent", "meaning": "令人信服的；有力的", "usage": "She presented a cogent argument for the proposal.", "context": "商務"},
    {"word": "Disseminate", "meaning": "傳播；散佈", "usage": "The company disseminated the new policy to all staff.", "context": "商務"},
    {"word": "Enigmatic", "meaning": "神秘的；費解的", "usage": "The CEO's enigmatic announcement left everyone confused.", "context": "商務"},
    {"word": "Frivolous", "meaning": "輕浮的；不重要的", "usage": "Don't waste time on frivolous matters.", "context": "商務"},
    {"word": "Galvanize", "meaning": "激勵；促使行動", "usage": "The crisis galvanized the team into action.", "context": "商務"},
    {"word": "Humility", "meaning": "謙虛；謙遜", "usage": "Good leaders demonstrate humility and openness.", "context": "商務"},
    {"word": "Impeccable", "meaning": "完美的；無可挑剔的", "usage": "Her track record is impeccable.", "context": "商務"},
    {"word": "Jeopardize", "meaning": "危害；危及", "usage": "Poor planning could jeopardize the entire project.", "context": "商務"},
    {"word": "Kinetic", "meaning": "動態的；充滿活力的", "usage": "The team has kinetic energy that drives innovation.", "context": "商務"},
    {"word": "Lucrative", "meaning": "有利可圖的；賺錢的", "usage": "Real estate can be a lucrative investment.", "context": "商務"},
    {"word": "Mitigate", "meaning": "緩解；減輕", "usage": "We must mitigate the risks before proceeding.", "context": "商務"},
    {"word": "Nascent", "meaning": "新興的；初期的", "usage": "The nascent startup shows great potential.", "context": "商務"},
    {"word": "Obsolete", "meaning": "過時的；已淘汰的", "usage": "That technology is now obsolete.", "context": "商務"},
    {"word": "Proficient", "meaning": "熟練的；精通的", "usage": "She is proficient in multiple programming languages.", "context": "商務"},
    {"word": "Quintessential", "meaning": "典型的；最典型的", "usage": "This is the quintessential example of good leadership.", "context": "商務"},
    {"word": "Resilient", "meaning": "有韌性的；可恢復的", "usage": "Our business model is resilient to market changes.", "context": "商務"},
    {"word": "Sagacious", "meaning": "聰慧的；賢明的", "usage": "The sagacious decision led to record profits.", "context": "商務"},
    {"word": "Truncate", "meaning": "截短；縮短", "usage": "Please truncate the report to one page.", "context": "商務"},
    {"word": "Ubiquitous", "meaning": "無處不在的；普遍的", "usage": "Internet connectivity is now ubiquitous.", "context": "商務"},
    {"word": "Validate", "meaning": "證實；驗證", "usage": "We need to validate this hypothesis with data.", "context": "商務"},
    {"word": "Warrant", "meaning": "保證；授權", "usage": "The results warrant further investigation.", "context": "商務"},
    {"word": "Xerox", "meaning": "複印；影印", "usage": "Can you xerox these documents for me?", "context": "商務"},
    {"word": "Yardstick", "meaning": "標準；衡量標準", "usage": "Use performance metrics as a yardstick.", "context": "商務"},
    {"word": "Zealot", "meaning": "狂熱者；極端分子", "usage": "Avoid becoming a technology zealot.", "context": "商務"},
    {"word": "Acumen", "meaning": "敏銳；技巧", "usage": "Business acumen is crucial for success.", "context": "商務"},
    {"word": "Benevolent", "meaning": "慈善的；仁慈的", "usage": "The company has a benevolent foundation.", "context": "商務"},
    {"word": "Catalyst", "meaning": "催化劑；促進者", "usage": "Innovation is the catalyst for growth.", "context": "商務"},
    {"word": "Debacle", "meaning": "慘敗；崩潰", "usage": "The product launch was a complete debacle.", "context": "商務"},
]

def get_weather():
    """從 open-meteo API 獲取台中市天氣 (帶重試機制)"""
    try:
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": 24.14,
            "longitude": 120.68,
            "current": "temperature_2m,relative_humidity_2m,precipitation",
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max",
            "timezone": "Asia/Taipei",
        }
        
        # 重試 3 次，每次超時 15 秒
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = requests.get(url, params=params, timeout=15, headers=headers)
                response.raise_for_status()
                data = response.json()
                
                current = data.get("current", {})
                daily = data.get("daily", {})
                
                temp = current.get("temperature_2m", "N/A")
                humidity = current.get("relative_humidity_2m", "N/A")
                rain_prob = daily.get("precipitation_probability_max", [0])[0]
                max_temp = daily.get("temperature_2m_max", [0])[0]
                min_temp = daily.get("temperature_2m_min", [0])[0]
                
                return {
                    "current_temp": temp,
                    "humidity": humidity,
                    "max_temp": max_temp,
                    "min_temp": min_temp,
                    "rain_prob": rain_prob,
                }
            except requests.exceptions.Timeout:
                if attempt < max_retries - 1:
                    print(f"    [RETRY] 天氣 API 超時，重試 {attempt + 2}/{max_retries}...")
                    time.sleep(2)
                    continue
                else:
                    raise
    except Exception as e:
        return {"error": f"天氣獲取失敗: {str(e)}"}

def get_reminders():
    """讀取 reminders.txt 中的提醒事項"""
    try:
        if os.path.exists("reminders.txt"):
            with open("reminders.txt", "r", encoding="utf-8") as f:
                reminders = f.readlines()
            return [r.strip() for r in reminders if r.strip()]
        return []
    except Exception as e:
        return [f"讀取提醒失敗: {e}"]

def get_financial_data():
    """獲取金融商品數據 (優先 yfinance，備選 Finnhub)"""
    stocks = ["MU", "PLTR", "ORCL", "TSLA", "NVDA"]
    crypto = ["BTC-USD", "ETH-USD"]
    currency = ["TWD=X"]
    
    all_tickers = stocks + crypto + currency
    data = {}
    
    # 嘗試使用 yfinance
    yfinance_success = False
    try:
        for ticker in all_tickers:
            try:
                print(f"  正在查詢: {ticker}...")
                stock = yf.Ticker(ticker)
                
                # 重試 2 次
                hist = None
                for attempt in range(2):
                    try:
                        hist = stock.history(period="5d")
                        if hist is not None and not hist.empty:
                            break
                    except Exception as e:
                        if attempt == 0:
                            print(f"    [RETRY] {ticker} 重試...")
                            time.sleep(1)
                        else:
                            raise
                
                if hist is None or hist.empty:
                    print(f"    [WARN] {ticker} 無數據")
                    data[ticker] = {"error": "無可用數據"}
                    continue
                
                close_price = float(hist['Close'].iloc[-1])
                prev_close = float(hist['Close'].iloc[-2]) if len(hist) >= 2 else close_price
                change_pct = ((close_price - prev_close) / prev_close) * 100 if prev_close != 0 else 0
                
                data[ticker] = {
                    "price": float(round(close_price, 2)),
                    "change_pct": float(round(change_pct, 2)),
                }
                print(f"    [OK] {ticker}: ${close_price:.2f} ({change_pct:+.2f}%)")
                yfinance_success = True
            except Exception as ticker_error:
                print(f"    [ERROR] {ticker}: {str(ticker_error)}")
                data[ticker] = {"error": str(ticker_error)}
    except Exception as e:
        print(f"[WARNING] yfinance 失敗，嘗試備選方案...")
    
    # 如果 yfinance 完全失敗，使用 Finnhub API
    if not yfinance_success and not any(isinstance(v, dict) and "error" not in v for v in data.values()):
        print("[INFO] 嘗試使用 Finnhub API...")
        finnhub_key = os.environ.get("FINNHUB_API_KEY", "")
        
        if finnhub_key:
            try:
                for ticker in all_tickers:
                    try:
                        print(f"  Finnhub 查詢: {ticker}...")
                        
                        # Finnhub API 對不同類型的符號有不同格式
                        # 股票: MU, PLTR 等
                        # 加密貨幣: BTCUSD（無橫線）
                        # 貨幣對: USDTWD（無等號）
                        finnhub_symbol = ticker
                        if ticker.endswith("-USD"):
                            # 加密貨幣：BTC-USD → BTCUSD
                            finnhub_symbol = ticker.replace("-", "")
                        elif ticker == "TWD=X":
                            # 貨幣對：TWD=X → USDTWD
                            finnhub_symbol = "USDTWD"
                        
                        # Finnhub API 端點
                        url = f"https://finnhub.io/api/v1/quote"
                        params = {
                            "symbol": finnhub_symbol,
                            "token": finnhub_key
                        }
                        
                        response = requests.get(url, params=params, timeout=10, headers=headers)
                        if response.status_code == 200:
                            result = response.json()
                            if "c" in result and result["c"] > 0:  # c = current price
                                current = result.get("c", 0)
                                prev = result.get("pc", current)  # pc = previous close
                                change_pct = ((current - prev) / prev * 100) if prev != 0 else 0
                                
                                data[ticker] = {
                                    "price": float(round(current, 2)),
                                    "change_pct": float(round(change_pct, 2)),
                                }
                                print(f"    [OK] {ticker}: ${current:.2f} ({change_pct:+.2f}%)")
                            else:
                                print(f"    [WARN] {ticker} 無有效數據")
                        else:
                            print(f"    [ERROR] {ticker} HTTP {response.status_code}")
                    except Exception as e:
                        print(f"    [ERROR] Finnhub {ticker}: {str(e)}")
            except Exception as e:
                print(f"[ERROR] Finnhub 失敗: {str(e)}")
        else:
            print("[WARNING] FINNHUB_API_KEY 未設定，無法使用備選方案")
    
    return data

def get_vocabulary():
    """隨機抽取 10 個 TOEIC 單字"""
    return random.sample(VOCABULARY, min(10, len(VOCABULARY)))

def format_message(weather, reminders, financial, vocab):
    """格式化並生成 Discord 訊息"""
    tw_tz = ZoneInfo("Asia/Taipei")
    now = datetime.now(tw_tz)
    date_str = now.strftime("%Y-%m-%d %H:%M")
    
    message = f"🌅 **每日早晨助理報告** ({date_str})\n\n"
    
    # 天氣區塊
    message += "🌤️ **天氣預報 (台中市)**\n"
    if "error" not in weather:
        message += f"• 目前溫度: {weather.get('current_temp', 'N/A')}°C\n"
        message += f"• 最高溫: {weather.get('max_temp', 'N/A')}°C\n"
        message += f"• 最低溫: {weather.get('min_temp', 'N/A')}°C\n"
        message += f"• 降雨機率: {weather.get('rain_prob', 'N/A')}%\n"
        message += f"• 濕度: {weather.get('humidity', 'N/A')}%\n"
    else:
        message += f"❌ {weather['error']}\n"
    message += "\n"
    
    # 提醒事項
    if reminders:
        message += "📝 **今日提醒**\n"
        for reminder in reminders:
            message += f"• {reminder}\n"
        message += "\n"
    
    # 金融商品
    message += "📈 **金融商品走勢**\n"
    stocks = ["MU", "PLTR", "ORCL", "TSLA", "NVDA"]
    crypto = ["BTC-USD", "ETH-USD"]
    currency = ["TWD=X"]
    
    # 美股
    message += "*美股:*\n"
    stock_count = 0
    for ticker in stocks:
        if ticker in financial:
            if "error" not in financial[ticker]:
                data = financial[ticker]
                symbol = "📈" if data["change_pct"] >= 0 else "📉"
                message += f"• {ticker}: ${data['price']} {symbol} {data['change_pct']:+.2f}%\n"
                stock_count += 1
    if stock_count == 0:
        message += "• (無可用數據)\n"
    
    # 加密貨幣
    message += "\n*加密貨幣:*\n"
    crypto_count = 0
    for ticker in crypto:
        if ticker in financial:
            if "error" not in financial[ticker]:
                data = financial[ticker]
                symbol = "📈" if data["change_pct"] >= 0 else "📉"
                message += f"• {ticker}: ${data['price']:,.2f} {symbol} {data['change_pct']:+.2f}%\n"
                crypto_count += 1
    if crypto_count == 0:
        message += "• (無可用數據)\n"
    
    # 匯率
    message += "\n*匯率:*\n"
    currency_count = 0
    for ticker in currency:
        if ticker in financial:
            if "error" not in financial[ticker]:
                data = financial[ticker]
                message += f"• {ticker}: {data['price']:.2f}\n"
                currency_count += 1
    if currency_count == 0:
        message += "• (無可用數據)\n"
    
    message += "\n"
    
    # 英文單字
    message += "📚 **今日英文單字 (TOEIC 900 級)**\n"
    for i, item in enumerate(vocab, 1):
        message += f"{i}. **{item['word']}** - {item['meaning']}\n"
        message += f"   例: {item['usage']}\n"
    
    return message

def send_discord_message(message, webhook_url):
    """發送訊息到 Discord (帶重試機制)"""
    try:
        payload = {
            "content": message,
        }
        
        # 重試 2 次，超時 15 秒
        for attempt in range(2):
            try:
                response = requests.post(webhook_url, json=payload, timeout=15, headers=headers)
                if response.status_code == 204:
                    print("✅ 訊息已成功發送到 Discord")
                    return True
                else:
                    print(f"❌ 發送失敗: {response.status_code} - {response.text}")
                    return False
            except requests.exceptions.Timeout:
                if attempt == 0:
                    print(f"    [RETRY] Discord 發送超時，重試...")
                    time.sleep(2)
                else:
                    raise
    except Exception as e:
        print(f"❌ 發送錯誤: {e}")
        return False

def main():
    """主函數"""
    # 獲取環境變數
    webhook_url = os.environ.get("DISCORD_WEBHOOK_URL")
    if not webhook_url:
        print("❌ 錯誤: 未設定 DISCORD_WEBHOOK_URL 環境變數")
        return
    
    print("🔄 開始收集資料...\n")
    
    # 收集所有數據
    print("📍 取得天氣數據...")
    weather = get_weather()
    if "error" in weather:
        print(f"  ⚠️  {weather['error']}")
    else:
        print(f"  ✅ 台中市溫度: {weather.get('current_temp')}°C")
    
    print("\n📝 取得提醒事項...")
    reminders = get_reminders()
    print(f"  ✅ 找到 {len(reminders)} 項提醒")
    
    print("\n💹 取得金融數據...")
    financial = get_financial_data()
    if "error" in financial:
        print(f"  ⚠️  {financial['error']}")
    else:
        success_count = sum(1 for v in financial.values() if isinstance(v, dict) and "error" not in v)
        print(f"  ✅ 成功獲取 {success_count} 個商品數據")
    
    print("\n📚 取得英文單字...")
    vocab = get_vocabulary()
    print(f"  ✅ 隨機抽取 {len(vocab)} 個單字")
    
    # 生成訊息
    print("\n✏️  正在格式化訊息...")
    message = format_message(weather, reminders, financial, vocab)
    
    # 發送訊息
    print("\n📤 發送至 Discord...\n")
    send_discord_message(message, webhook_url)

if __name__ == "__main__":
    main()
