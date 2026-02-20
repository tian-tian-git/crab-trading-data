#!/usr/bin/env python3
"""
蟹爪自选股票数据抓取
"""

import akshare as ak
import pandas as pd
import json
import os
import sys
from datetime import datetime

# 添加路径导入自选股票
sys.path.insert(0, os.path.dirname(__file__))
from my_picks import MY_PICKS

def fetch_stock_data(symbol, info):
    """获取单只股票数据"""
    name = info['name']
    print(f"  抓取 {symbol} {name}...", end=" ")
    
    try:
        # 获取历史数据
        df = ak.stock_zh_a_hist(symbol=symbol, period="daily", 
                                start_date="20240101", adjust="qfq")
        
        if df.empty:
            print("✗ 无数据")
            return None
        
        # 保存 CSV
        os.makedirs('data/prices', exist_ok=True)
        df.to_csv(f'data/prices/{symbol}.csv', index=False)
        
        # 获取最新行情
        try:
            spot = ak.stock_zh_a_spot_em()
            stock_spot = spot[spot['代码'] == symbol]
            if not stock_spot.empty:
                latest = stock_spot.iloc[0]
                basic_info = {
                    'symbol': symbol,
                    'name': name,
                    'sector': info['sector'],
                    'reason': info['reason'],
                    'currentPrice': float(latest.get('最新价', 0)),
                    'previousClose': float(latest.get('昨收', 0)),
                    'change': float(latest.get('涨跌幅', 0)),
                    'volume': int(latest.get('成交量', 0)),
                    'amount': float(latest.get('成交额', 0)),
                    'turnover': float(latest.get('换手率', 0)),
                    'pe': float(latest.get('市盈率-动态', 0) or 0),
                    'pb': float(latest.get('市净率', 0) or 0),
                    'marketCap': float(latest.get('总市值', 0) or 0),
                    'updatedAt': datetime.now().isoformat()
                }
            else:
                latest_row = df.iloc[-1]
                basic_info = {
                    'symbol': symbol,
                    'name': name,
                    'sector': info['sector'],
                    'reason': info['reason'],
                    'currentPrice': float(latest_row['收盘']),
                    'previousClose': float(latest_row['收盘']),
                    'volume': int(latest_row['成交量']),
                    'updatedAt': datetime.now().isoformat()
                }
        except:
            latest_row = df.iloc[-1]
            basic_info = {
                'symbol': symbol,
                'name': name,
                'sector': info['sector'],
                'reason': info['reason'],
                'currentPrice': float(latest_row['收盘']),
                'previousClose': float(latest_row['收盘']),
                'volume': int(latest_row['成交量']),
                'updatedAt': datetime.now().isoformat()
            }
        
        print(f"✓ 价格: {basic_info['currentPrice']:.2f}")
        return basic_info
        
    except Exception as e:
        print(f"✗ 错误: {e}")
        return None

def main():
    print("=" * 60)
    print("🦞 蟹爪自选股票数据抓取")
    print("=" * 60)
    print(f"共 {len(MY_PICKS)} 只股票\n")
    
    all_data = {}
    failed = []
    
    for i, (symbol, info) in enumerate(MY_PICKS.items()):
        print(f"[{i+1}/{len(MY_PICKS)}]", end="")
        data = fetch_stock_data(symbol, info)
        if data:
            all_data[symbol] = data
        else:
            failed.append(symbol)
    
    # 保存汇总
    os.makedirs('data', exist_ok=True)
    with open('data/my_picks.json', 'w', encoding='utf-8') as f:
        json.dump(all_data, f, indent=2, ensure_ascii=False)
    
    with open('data/last_update.txt', 'w') as f:
        f.write(datetime.now().isoformat())
    
    print(f"\n完成！成功: {len(all_data)}, 失败: {len(failed)}")
    if failed:
        print(f"失败: {', '.join(failed)}")

if __name__ == '__main__':
    main()
