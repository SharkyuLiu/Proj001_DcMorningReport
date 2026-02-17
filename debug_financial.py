import main

# 獲取金融數據
financial = main.get_financial_data()

# 打印詳細信息
print('=== financial 字典內容 ===')
for key, value in financial.items():
    print(f'{key}: {value}')

print('\n=== 檢查邏輯 ===')
stocks = ['MU', 'PLTR', 'ORCL', 'TSLA', 'NVDA']
for ticker in stocks:
    if ticker in financial:
        if 'error' not in financial[ticker]:
            print(f'{ticker}: OK 應該顯示')
        else:
            print(f'{ticker}: ERROR {financial[ticker]["error"]}')
    else:
        print(f'{ticker}: NOT IN DICT')
