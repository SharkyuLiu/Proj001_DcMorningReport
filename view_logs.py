#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
查看和分析 DEBUG 日誌
用法: python view_logs.py [選項]
"""

import os
import sys
from pathlib import Path
from datetime import datetime

def view_latest_logs(num_lines=50):
    """查看最新日誌"""
    log_file = Path("logs/debug.log")
    
    if not log_file.exists():
        print("❌ 日誌文件不存在: logs/debug.log")
        return
    
    print(f"📋 查看最新 {num_lines} 行日誌 ({log_file})\n")
    print("="*80)
    
    with open(log_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 顯示最後 num_lines 行
    for line in lines[-num_lines:]:
        print(line.rstrip())
    
    print("="*80)
    print(f"✅ 共 {len(lines)} 行日誌\n")


def view_taiwan_stock_logs():
    """查看台股相關日誌"""
    log_file = Path("logs/debug.log")
    
    if not log_file.exists():
        print("❌ 日誌文件不存在")
        return
    
    print("📊 台股 DEBUG 日誌\n")
    print("="*80)
    
    with open(log_file, 'r', encoding='utf-8') as f:
        for line in f:
            # 篩選含有台股相關信息
            if any(keyword in line for keyword in ['0050', '2330', 'get_tw_stock_data', '台股']):
                print(line.rstrip())
    
    print("="*80 + "\n")


def view_yfinance_errors():
    """查看 yfinance 錯誤"""
    log_file = Path("logs/debug.log")
    
    if not log_file.exists():
        print("❌ 日誌文件不存在")
        return
    
    print("⚠️  yfinance 錯誤日誌\n")
    print("="*80)
    
    error_found = False
    with open(log_file, 'r', encoding='utf-8') as f:
        for line in f:
            if 'error' in line.lower() or 'exception' in line.lower() or '異常' in line:
                if 'tw_stock' in line or '0050' in line or '2330' in line:
                    print(line.rstrip())
                    error_found = True
    
    if not error_found:
        print("✅ 未發現台股錯誤")
    
    print("="*80 + "\n")


def get_stats():
    """取得日誌統計"""
    log_file = Path("logs/debug.log")
    
    if not log_file.exists():
        print("❌ 日誌文件不存在")
        return
    
    stats = {
        'total': 0,
        'debug': 0,
        'info': 0,
        'warning': 0,
        'error': 0
    }
    
    with open(log_file, 'r', encoding='utf-8') as f:
        for line in f:
            stats['total'] += 1
            if '| DEBUG' in line:
                stats['debug'] += 1
            elif '| INFO' in line:
                stats['info'] += 1
            elif '| WARNING' in line:
                stats['warning'] += 1
            elif '| ERROR' in line:
                stats['error'] += 1
    
    print("📊 日誌統計\n")
    print(f"  總行數:    {stats['total']}")
    print(f"  DEBUG:     {stats['debug']}")
    print(f"  INFO:      {stats['info']}")
    print(f"  WARNING:   {stats['warning']}")
    print(f"  ERROR:     {stats['error']}\n")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        
        if cmd == "taiwan":
            view_taiwan_stock_logs()
        elif cmd == "error":
            view_yfinance_errors()
        elif cmd == "stats":
            get_stats()
        elif cmd.startswith("tail"):
            # tail 100 或 tail 50 等
            num = int(cmd.split(':')[1]) if ':' in cmd else 50
            view_latest_logs(num)
        else:
            print("❌ 未知命令")
            print("\n用法:")
            print("  python view_logs.py stats      - 查看日誌統計")
            print("  python view_logs.py taiwan     - 查看台股日誌")
            print("  python view_logs.py error      - 查看錯誤日誌")
            print("  python view_logs.py tail:50    - 查看最後 50 行 (預設 50 行)")
    else:
        # 預設顯示最後 50 行 + 統計
        print("\n")
        view_latest_logs(50)
        get_stats()
        print("💡 提示: python view_logs.py [stats|taiwan|error|tail:100]")
