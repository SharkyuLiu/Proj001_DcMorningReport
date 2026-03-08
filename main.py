import os
import requests
import random
import time
from datetime import datetime
from zoneinfo import ZoneInfo
import yfinance as yf
import json
import schedule

# 設定 User-Agent 避免被 API 限制
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

# TOEIC 900 級別商用單詞詞典（200 個）
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
    {"word": "Efficacious", "meaning": "有效的；奏效的", "usage": "The new marketing strategy proved efficacious.", "context": "商務"},
    {"word": "Facile", "meaning": "容易的；膚淺的", "usage": "Don't rely on facile solutions for complex problems.", "context": "商務"},
    {"word": "Gregarious", "meaning": "群居的；愛社交的", "usage": "She is a gregarious person who enjoys teamwork.", "context": "商務"},
    {"word": "Harbinger", "meaning": "先兆；預告者", "usage": "Economic data is a harbinger of future trends.", "context": "商務"},
    {"word": "Indolent", "meaning": "懶惰的；不願費力的", "usage": "An indolent approach will damage your career.", "context": "商務"},
    {"word": "Juxtaposition", "meaning": "並列；對比", "usage": "The juxtaposition of old and new strategies worked well.", "context": "商務"},
    {"word": "Kudos", "meaning": "讚譽；掌聲", "usage": "Kudos to the team for their outstanding performance.", "context": "商務"},
    {"word": "Loquacious", "meaning": "話多的；冗長的", "usage": "The loquacious presenter held everyone's attention.", "context": "商務"},
    {"word": "Meander", "meaning": "蜿蜒；漫步", "usage": "The conversation began to meander off topic.", "context": "商務"},
    {"word": "Nomenclature", "meaning": "命名法；專用術語", "usage": "Understanding the nomenclature is essential in this field.", "context": "商務"},
    {"word": "Obsequious", "meaning": "過度殷勤的；奴顏婢膝的", "usage": "His obsequious behavior made colleagues uncomfortable.", "context": "商務"},
    {"word": "Paucity", "meaning": "缺乏；不足", "usage": "There is a paucity of qualified candidates.", "context": "商務"},
    {"word": "Quixotic", "meaning": "不切實際的；空想的", "usage": "His quixotic plan was ultimately unsuccessful.", "context": "商務"},
    {"word": "Rancor", "meaning": "怨恨；仇恨", "usage": "There is lingering rancor between the two departments.", "context": "商務"},
    {"word": "Salient", "meaning": "突出的；主要的", "usage": "The salient points should be included in the summary.", "context": "商務"},
    {"word": "Taciturn", "meaning": "沉默寡言的", "usage": "The taciturn executive rarely spoke in meetings.", "context": "商務"},
    {"word": "Ubiquity", "meaning": "無所不在；普遍性", "usage": "The ubiquity of mobile phones changed communication.", "context": "商務"},
    {"word": "Vigilant", "meaning": "警惕的；謹慎的", "usage": "We must remain vigilant against security threats.", "context": "商務"},
    {"word": "Wacky", "meaning": "古怪的；荒唐的", "usage": "His wacky ideas sometimes lead to innovation.", "context": "商務"},
    {"word": "Xerophyte", "meaning": "耐旱植物", "usage": "This company is xerophyte in its resource management.", "context": "商務"},
    {"word": "Yearn", "meaning": "渴望；懷念", "usage": "Employees yearn for better work-life balance.", "context": "商務"},
    {"word": "Zephyr", "meaning": "微風；輕風", "usage": "Even a zephyr of change can shift market dynamics.", "context": "商務"},
    {"word": "Abscond", "meaning": "逃跑；潛逃", "usage": "The suspect absconded with company funds.", "context": "商務"},
    {"word": "Aberrant", "meaning": "異常的；不正常的", "usage": "The aberrant behavior did not reflect company values.", "context": "商務"},
    {"word": "Abeyance", "meaning": "暫停；懸而未決", "usage": "The project remains in abeyance pending approval.", "context": "商務"},
    {"word": "Ablate", "meaning": "消融；磨損", "usage": "Our market share began to ablate.", "context": "商務"},
    {"word": "Abnegation", "meaning": "放棄；拒絕", "usage": "His abnegation of responsibility disappointed us.", "context": "商務"},
    {"word": "Abrade", "meaning": "磨損；擦傷", "usage": "Poor customer service abrades brand loyalty.", "context": "商務"},
    {"word": "Abrogate", "meaning": "廢止；撤銷", "usage": "The contract was abrogated due to non-compliance.", "context": "商務"},
    {"word": "Abstemious", "meaning": "節制的；不放縱的", "usage": "An abstemious approach to spending is prudent.", "context": "商務"},
    {"word": "Abstinence", "meaning": "節制；禁慾", "usage": "Abstinence from risky investments is wise.", "context": "商務"},
    {"word": "Abstruse", "meaning": "深奧的；難懂的", "usage": "The financial model is too abstruse for most people.", "context": "商務"},
    {"word": "Abundance", "meaning": "豐富；大量", "usage": "The market has an abundance of similar products.", "context": "商務"},
    {"word": "Accede", "meaning": "同意；贊成", "usage": "The client finally acceded to our proposal.", "context": "商務"},
    {"word": "Accelerate", "meaning": "加速；促進", "usage": "We need to accelerate the project timeline.", "context": "商務"},
    {"word": "Accentuate", "meaning": "強調；突出", "usage": "This feature accentuates the product's benefits.", "context": "商務"},
    {"word": "Accolade", "meaning": "讚揚；榮譽", "usage": "She received accolades for her innovation.", "context": "商務"},
    {"word": "Accommodate", "meaning": "容納；適應", "usage": "We can accommodate your special requirements.", "context": "商務"},
    {"word": "Accomplice", "meaning": "共犯；幫凶", "usage": "He was found to be an accomplice in the fraud.", "context": "商務"},
    {"word": "Accord", "meaning": "協議；一致", "usage": "We reached an accord on the key terms.", "context": "商務"},
    {"word": "Accost", "meaning": "主動交談；招呼", "usage": "The sales rep accosted customers in the lobby.", "context": "商務"},
    {"word": "Accuracy", "meaning": "準確性；精確度", "usage": "Data accuracy is critical for our reports.", "context": "商務"},
    {"word": "Acculturation", "meaning": "文化適應；同化", "usage": "New employees undergo acculturation processes.", "context": "商務"},
    {"word": "Accumulate", "meaning": "積累；堆積", "usage": "Compound interest allows wealth to accumulate.", "context": "商務"},
    {"word": "Achieve", "meaning": "達成；完成", "usage": "We achieved our quarterly targets ahead of schedule.", "context": "商務"},
    {"word": "Acrid", "meaning": "刺鼻的；尖刻的", "usage": "The acrid tone of the email damaged relationships.", "context": "商務"},
    {"word": "Acrimony", "meaning": "尖刻；苦毒", "usage": "The negotiations ended with acrimony.", "context": "商務"},
    {"word": "Acrobat", "meaning": "雜技演員；適應性強的人", "usage": "He is an acrobat in navigating complex situations.", "context": "商務"},
    {"word": "Acronym", "meaning": "縮寫詞；首字母縮略詞", "usage": "Learn the common acronyms used in our industry.", "context": "商務"},
    {"word": "Actualize", "meaning": "實現；使具體化", "usage": "We must actualize our vision through action.", "context": "商務"},
    {"word": "Acuity", "meaning": "敏銳；尖銳", "usage": "His analytical acuity impressed the board.", "context": "商務"},
    {"word": "Acumen", "meaning": "敏銳；技巧", "usage": "Business acumen is essential for leadership.", "context": "商務"},
    {"word": "Acute", "meaning": "尖銳的；急性的", "usage": "We face an acute shortage of skilled workers.", "context": "商務"},
    {"word": "Adage", "meaning": "格言；諺語", "usage": "The adage 'time is money' holds true in business.", "context": "商務"},
    {"word": "Adamant", "meaning": "堅定的；不屈的", "usage": "He was adamant about his decision.", "context": "商務"},
    {"word": "Adaptation", "meaning": "適應；改編", "usage": "Innovation requires rapid adaptation to change.", "context": "商務"},
    {"word": "Addendum", "meaning": "附錄；附加內容", "usage": "See the addendum for additional information.", "context": "商務"},
    {"word": "Adequate", "meaning": "充分的；足夠的", "usage": "Our resources are adequate for this project.", "context": "商務"},
    {"word": "Adhere", "meaning": "粘附；遵守", "usage": "Employees must adhere to company policies.", "context": "商務"},
    {"word": "Adjacent", "meaning": "鄰近的；相鄰的", "usage": "The adjacent sectors show similar trends.", "context": "商務"},
    {"word": "Adjourn", "meaning": "延期；休會", "usage": "We will adjourn the meeting until next week.", "context": "商務"},
    {"word": "Adjunct", "meaning": "附加物；助手", "usage": "She serves as an adjunct professor at the university.", "context": "商務"},
    {"word": "Adjust", "meaning": "調整；適應", "usage": "We need to adjust our pricing strategy.", "context": "商務"},
    {"word": "Administer", "meaning": "管理；執行", "usage": "The manager administers employee benefits.", "context": "商務"},
    {"word": "Admirable", "meaning": "令人欽佩的；值得讚美的", "usage": "Her admirable work ethic inspires others.", "context": "商務"},
    {"word": "Admiration", "meaning": "欽佩；讚美", "usage": "I have great admiration for his leadership.", "context": "商務"},
    {"word": "Admissible", "meaning": "可接受的；可認可的", "usage": "The evidence is admissible in court.", "context": "商務"},
    {"word": "Admission", "meaning": "承認；進入", "usage": "His admission of error showed integrity.", "context": "商務"},
    {"word": "Admittedly", "meaning": "誠然；的確", "usage": "The plan is admittedly complex.", "context": "商務"},
    {"word": "Admixture", "meaning": "混合物；摻雜", "usage": "Success is an admixture of luck and hard work.", "context": "商務"},
    {"word": "Admonition", "meaning": "警告；勸告", "usage": "The compliance warning was an admonition.", "context": "商務"},
    {"word": "Adolescent", "meaning": "青少年；不成熟的", "usage": "The company demonstrated adolescent behavior.", "context": "商務"},
    {"word": "Adonis", "meaning": "美男子", "usage": "He is considered the adonis of the office.", "context": "商務"},
    {"word": "Adopt", "meaning": "採納；通過", "usage": "The board will adopt the new policy.", "context": "商務"},
    {"word": "Adoration", "meaning": "崇拜；愛慕", "usage": "Customers feel adoration for the brand.", "context": "商務"},
    {"word": "Adorn", "meaning": "裝飾；妝點", "usage": "Awards adorn the company's office walls.", "context": "商務"},
    {"word": "Adroit", "meaning": "靈巧的；熟練的", "usage": "Her adroit negotiation skills secured the deal.", "context": "商務"},
    {"word": "Adulation", "meaning": "奉承；讚美", "usage": "The CEO received adulation from shareholders.", "context": "商務"},
    {"word": "Adult", "meaning": "成年人；成熟的", "usage": "We need adult leadership in this crisis.", "context": "商務"},
    {"word": "Adulterate", "meaning": "摻雜；污染", "usage": "Never adulterate your product quality.", "context": "商務"},
    {"word": "Advance", "meaning": "前進；預付", "usage": "We advance the project deadline.", "context": "商務"},
    {"word": "Advantage", "meaning": "優勢；好處", "usage": "This location has a strategic advantage.", "context": "商務"},
    {"word": "Adventure", "meaning": "冒險；奇遇", "usage": "Entrepreneurship is an adventure.", "context": "商務"},
    {"word": "Adversary", "meaning": "對手；敵手", "usage": "Our main adversary is the competitor.", "context": "商務"},
    {"word": "Adverse", "meaning": "不利的；敵對的", "usage": "Adverse market conditions affected sales.", "context": "商務"},
    {"word": "Adversity", "meaning": "逆境；不幸", "usage": "The company overcame adversity.", "context": "商務"},
    {"word": "Advertise", "meaning": "做廣告；宣傳", "usage": "We advertise our products on social media.", "context": "商務"},
    {"word": "Advertisement", "meaning": "廣告", "usage": "The advertisement went viral online.", "context": "商務"},
    {"word": "Advice", "meaning": "建議；忠告", "usage": "Follow the consultant's advice carefully.", "context": "商務"},
    {"word": "Advisable", "meaning": "明智的；可取的", "usage": "It is advisable to review contracts before signing.", "context": "商務"},
    {"word": "Advise", "meaning": "勸告；建議", "usage": "I advise you to reconsider.", "context": "商務"},
    {"word": "Advocate", "meaning": "提倡；擁護", "usage": "She advocates for better employee benefits.", "context": "商務"},
    {"word": "Aerial", "meaning": "空中的；航空的", "usage": "The aerial view shows our market position.", "context": "商務"},
    {"word": "Aerate", "meaning": "通風；充氣", "usage": "We aerate opinions in open forums.", "context": "商務"},
    {"word": "Aeronautics", "meaning": "航空學", "usage": "Innovations in aeronautics benefit our industry.", "context": "商務"},
    {"word": "Aesthetic", "meaning": "美學的；審美的", "usage": "The aesthetic design appeals to customers.", "context": "商務"},
    {"word": "Affable", "meaning": "和藹的；親切的", "usage": "The CEO is affable and approachable.", "context": "商務"},
    {"word": "Affair", "meaning": "事情；事務", "usage": "Managing company affairs requires attention.", "context": "商務"},
    {"word": "Affect", "meaning": "影響；假裝", "usage": "Market trends affect our strategy.", "context": "商務"},
    {"word": "Affectation", "meaning": "矯揉造作；裝飾", "usage": "Avoid affectation in professional communication.", "context": "商務"},
    {"word": "Affection", "meaning": "感情；喜愛", "usage": "Customers show affection for our brand.", "context": "商務"},
    {"word": "Affidavit", "meaning": "誓言書；宣誓書", "usage": "Submit an affidavit with your application.", "context": "商務"},
    {"word": "Affiliate", "meaning": "關聯公司；聯盟", "usage": "We partner with affiliated companies.", "context": "商務"},
    {"word": "Affiliation", "meaning": "隸屬；聯繫", "usage": "What is your professional affiliation?", "context": "商務"},
    {"word": "Affinity", "meaning": "親和力；傾向", "usage": "She has an affinity for technology.", "context": "商務"},
    {"word": "Affirm", "meaning": "確認；申明", "usage": "We affirm our commitment to quality.", "context": "商務"},
    {"word": "Affirmative", "meaning": "肯定的；贊成的", "usage": "The answer is in the affirmative.", "context": "商務"},
    {"word": "Affix", "meaning": "貼上；附加", "usage": "Affix your signature to the document.", "context": "商務"},
    {"word": "Afflict", "meaning": "折磨；使痛苦", "usage": "Rising costs afflict small businesses.", "context": "商務"},
    {"word": "Affluence", "meaning": "富裕；豐富", "usage": "Affluence brings both opportunities and challenges.", "context": "商務"},
    {"word": "Affluent", "meaning": "富有的；豐富的", "usage": "Our affluent client base demands premium services.", "context": "商務"},
    {"word": "Afford", "meaning": "能夠承擔；提供", "usage": "We can afford to invest in innovation.", "context": "商務"},
    {"word": "Affront", "meaning": "侮辱；冒犯", "usage": "The remark was an affront to our team.", "context": "商務"},
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

def get_tw_stock_data(ticker):
    """獲取台股數據 (使用 yfinance，已驗證可用)"""
    try:
        # 嘗試多種代碼格式
        attempts = [f"{ticker}.TW", ticker, f"{ticker}.tw"]
        
        for attempt_ticker in attempts:
            try:
                stock = yf.Ticker(attempt_ticker)
                # 使用更長期間確保有數據
                hist = stock.history(period="10d")
                
                if hist is not None and not hist.empty and len(hist) >= 2:
                    close_price = float(hist['Close'].iloc[-1])
                    prev_close = float(hist['Close'].iloc[-2])
                    
                    if close_price > 0:
                        change_pct = ((close_price - prev_close) / prev_close) * 100
                        
                        return {
                            "price": float(round(close_price, 2)),
                            "change_pct": float(round(change_pct, 2)),
                        }
            except Exception:
                pass
    except Exception:
        pass
    
    return {"error": "無可用數據"}

def get_crypto_data(symbol):
    """獲取加密貨幣數據 (使用 CoinGecko 免費 API)"""
    try:
        # CoinGecko 免費 API，無需認證
        coin_ids = {
            "BTC-USD": "bitcoin",
            "ETH-USD": "ethereum",
        }
        
        coin_id = coin_ids.get(symbol)
        if not coin_id:
            return {"error": "未知幣種"}
        
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            "ids": coin_id,
            "vs_currencies": "usd",
            "include_24hr_change": "true"
        }
        
        response = requests.get(url, params=params, timeout=10, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if coin_id in data:
                price = data[coin_id].get("usd", 0)
                change = data[coin_id].get("usd_24h_change", 0)
                
                return {
                    "price": float(round(price, 2)),
                    "change_pct": float(round(change, 2)),
                }
    except Exception as e:
        print(f"    [WARN] 加密貨幣 {symbol} 無法獲取: {str(e)[:50]}")
    
    return {"error": "無可用數據"}

def get_currency_data(symbol):
    """獲取匯率數據 (使用 exchangerate-api)"""
    try:
        if symbol == "TWD=X":
            # 獲取台幣對美元的匯率
            url = "https://api.exchangerate-api.com/v4/latest/USD"
            response = requests.get(url, timeout=10, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                twd_rate = data.get("rates", {}).get("TWD", 0)
                
                if twd_rate > 0:
                    return {
                        "price": float(round(twd_rate, 2)),
                        "change_pct": 0.0,  # 實時匯率無法計算變化百分比
                    }
    except Exception as e:
        print(f"    [WARN] 匯率 {symbol} 無法獲取: {str(e)[:50]}")
    
    return {"error": "無可用數據"}

def get_tw_futures_data(symbol="^TWIF"):
    """獲取台灣期貨指數/加權指數"""
    try:
        # 方案1: 嘗試投資 investpy 獲取台灣加權指數
        import investpy
        try:
            index_data = investpy.indices.get_index_recent_data(
                index='TWII',  # 台灣加權指數
                country='taiwan',
                as_json=False,
                order='ascending'
            )
            
            if index_data is not None and len(index_data) > 0:
                close_price = float(index_data['Close'].iloc[-1])
                prev_close = float(index_data['Close'].iloc[-2]) if len(index_data) >= 2 else close_price
                change_pct = ((close_price - prev_close) / prev_close) * 100 if prev_close != 0 else 0
                
                return {
                    "price": float(round(close_price, 2)),
                    "change_pct": float(round(change_pct, 2)),
                }
        except Exception as e:
            pass
        
        # 方案2: 嘗試 yfinance ^TWII (台灣加權指數)
        stock = yf.Ticker("^TWII")
        hist = stock.history(period="5d")
        
        if hist is not None and not hist.empty:
            close_price = float(hist['Close'].iloc[-1])
            prev_close = float(hist['Close'].iloc[-2]) if len(hist) >= 2 else close_price
            change_pct = ((close_price - prev_close) / prev_close) * 100 if prev_close != 0 else 0
            
            return {
                "price": float(round(close_price, 2)),
                "change_pct": float(round(change_pct, 2)),
            }
    except Exception as e:
        pass
    
    return {"error": "無可用數據"}

def get_financial_data():
    """獲取金融商品數據 (台股、台灣指數、美股、加密貨幣、匯率)"""
    tw_stocks = ["0050", "2330"]
    us_market = ["VT", "QQQ", "SPY", "DIA", "EWT"]
    us_stocks = ["QCOM", "ANET", "TSLA", "NVDA", "GOOGL", "AAPL", "META", "AMZN", "MSFT", "MU", "PLTR", "ORCL", "TSM", "AMD", "INTC"]
    crypto = ["BTC-USD", "ETH-USD"]
    currency = ["TWD=X"]
    
    data = {}
    finnhub_key = os.environ.get("FINNHUB_API_KEY", "")
    
    # 0️⃣ 獲取台灣加權指數數據
    print("  📍 查詢台灣指數...")
    print(f"    正在查詢: 台灣加權指數...")
    result = get_tw_futures_data()
    if "error" not in result:
        data["^TWII"] = result
        print(f"    [OK] 台灣加權指數: {result['price']} {result['change_pct']:+.2f}%")
    else:
        data["^TWII"] = result
        print(f"    [INFO] 台灣加權指數 目前無數據，將使用 0050 作為市場指標")
    
    # 1️⃣ 獲取台股數據
    print("  📍 查詢台股...")
    for ticker in tw_stocks:
        print(f"    正在查詢: {ticker}...")
        result = get_tw_stock_data(ticker)
        if "error" not in result:
            data[ticker] = result
            print(f"    [OK] {ticker}: NT${result['price']} {result['change_pct']:+.2f}%")
        else:
            data[ticker] = result
            print(f"    [WARN] {ticker} 無數據")
    
    # 2️⃣ 獲取美股數據 (優先 Finnhub 或免費 API)
    print("  📍 查詢美股...")
    us_all = us_market + us_stocks
    
    if finnhub_key:
        # 使用 Finnhub API
        for ticker in us_all:
            print(f"    正在查詢: {ticker}...")
            try:
                url = "https://finnhub.io/api/v1/quote"
                params = {
                    "symbol": ticker,
                    "token": finnhub_key
                }
                
                response = requests.get(url, params=params, timeout=10, headers=headers)
                if response.status_code == 200:
                    result = response.json()
                    if "c" in result and result["c"] > 0:
                        current = result.get("c", 0)
                        prev = result.get("pc", current)
                        change_pct = ((current - prev) / prev * 100) if prev != 0 else 0
                        
                        data[ticker] = {
                            "price": float(round(current, 2)),
                            "change_pct": float(round(change_pct, 2)),
                        }
                        print(f"    [OK] {ticker}: ${data[ticker]['price']} {data[ticker]['change_pct']:+.2f}%")
                        continue
            except Exception as e:
                pass
            
            # Finnhub 失敗，標記為無數據
            data[ticker] = {"error": "無可用數據"}
            print(f"    [WARN] {ticker} 無數據")
    else:
        # 沒有 Finnhub Key，嘗試使用 yfinance (但可能失敗)
        for ticker in us_all:
            print(f"    正在查詢: {ticker}...")
            try:
                stock = yf.Ticker(ticker)
                hist = stock.history(period="5d")
                
                if hist is not None and not hist.empty:
                    close_price = float(hist['Close'].iloc[-1])
                    prev_close = float(hist['Close'].iloc[-2]) if len(hist) >= 2 else close_price
                    change_pct = ((close_price - prev_close) / prev_close) * 100 if prev_close != 0 else 0
                    
                    data[ticker] = {
                        "price": float(round(close_price, 2)),
                        "change_pct": float(round(change_pct, 2)),
                    }
                    print(f"    [OK] {ticker}: ${data[ticker]['price']} {data[ticker]['change_pct']:+.2f}%")
                    continue
            except Exception as e:
                pass
            
            data[ticker] = {"error": "無可用數據"}
            print(f"    [WARN] {ticker} 無數據")
    
    # 3️⃣ 獲取加密貨幣數據
    print("  📍 查詢加密貨幣...")
    for ticker in crypto:
        print(f"    正在查詢: {ticker}...")
        result = get_crypto_data(ticker)
        if "error" not in result:
            data[ticker] = result
            print(f"    [OK] {ticker}: ${result['price']:,.2f} {result['change_pct']:+.2f}%")
        else:
            data[ticker] = result
            print(f"    [WARN] {ticker} 無數據")
    
    # 4️⃣ 獲取匯率數據
    print("  📍 查詢匯率...")
    for ticker in currency:
        print(f"    正在查詢: {ticker}...")
        result = get_currency_data(ticker)
        if "error" not in result:
            data[ticker] = result
            print(f"    [OK] {ticker}: {result['price']:.2f}")
        else:
            data[ticker] = result
            print(f"    [WARN] {ticker} 無數據")
    
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
    tw_stocks = ["0050", "2330"]
    tw_index = "^TWII"
    us_market = ["VT", "QQQ", "SPY", "DIA", "EWT"]
    us_stocks = ["QCOM", "ANET", "TSLA", "NVDA", "GOOGL", "AAPL", "META", "AMZN", "MSFT", "MU", "PLTR", "ORCL", "TSM", "AMD", "INTC"]
    crypto = ["BTC-USD", "ETH-USD"]
    currency = ["TWD=X"]
    
    # 台灣加權指數
    message += "*台灣加權指數:*\n"
    if tw_index in financial and "error" not in financial[tw_index]:
        data = financial[tw_index]
        symbol = "📈" if data["change_pct"] >= 0 else "📉"
        message += f"• ^TWII: {data['price']} {symbol} {data['change_pct']:+.2f}%\n"
    else:
        message += "• (無可用數據)\n"
    
    # 台股
    message += "\n*台股:*\n"
    tw_count = 0
    for ticker in tw_stocks:
        if ticker in financial:
            if "error" not in financial[ticker]:
                data = financial[ticker]
                symbol = "📈" if data["change_pct"] >= 0 else "📉"
                message += f"• {ticker}: NT${data['price']} {symbol} {data['change_pct']:+.2f}%\n"
                tw_count += 1
    if tw_count == 0:
        message += "• (無可用數據)\n"
    
    # 美股大盤
    message += "\n*美股大盤:*\n"
    market_count = 0
    for ticker in us_market:
        if ticker in financial:
            if "error" not in financial[ticker]:
                data = financial[ticker]
                symbol = "📈" if data["change_pct"] >= 0 else "📉"
                message += f"• {ticker}: ${data['price']} {symbol} {data['change_pct']:+.2f}%\n"
                market_count += 1
    if market_count == 0:
        message += "• (無可用數據)\n"
    
    # 美股個股
    message += "\n*美股個股:*\n"
    stock_count = 0
    for ticker in us_stocks:
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

def send_daily_report():
    """發送每日報告的主任務"""
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

def main():
    """主函數 - 支持定時模式和一次性運行"""
    import sys
    
    # 檢查是否為定時模式
    if len(sys.argv) > 1 and sys.argv[1] == "--schedule":
        print("⏰ 啟動定時模式...")
        print("📅 設定報告時間: 06:30 和 07:00\n")
        
        # 設定定時任務
        schedule.every().day.at("06:30").do(send_daily_report)
        schedule.every().day.at("07:00").do(send_daily_report)
        
        # 持續運行
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # 每分鐘檢查一次
        except KeyboardInterrupt:
            print("\n\n⛔ 已停止定時服務")
    else:
        # 一次性運行
        send_daily_report()

if __name__ == "__main__":
    main()
