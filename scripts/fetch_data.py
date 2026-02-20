#!/usr/bin/env python3
"""
股票数据抓取脚本 - 在 GitHub Actions 上运行
"""

import yfinance as yf
import pandas as pd
import json
import os
from datetime import datetime

# 关注的股票列表
STOCKS = [
    'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA', 'META',
    'NFLX', 'AMD', 'CRM', 'PYPL', 'UBER', 'COIN', 'PLTR',
    'BABA', 'JD', 'NIO', 'XPEV', 'LI', 'PDD',
    'JPM', 'BAC', 'GS', 'MS', 'WFC',
    'JNJ', 'PFE', 'UNH', 'ABBV', 'MRK',
    'XOM', 'CVX', 'COP', 'EOG', 'SLB',
    'DIS', 'NKE', 'SBUX', 'MCD', 'LULU',
    'V', 'MA', 'AXP', 'DFS', 'COF',
    'SPY', 'QQQ', 'IWM', 'VTI', 'VOO',
    'BTC-USD', 'ETH-USD'
]

def fetch_stock_data(symbol):
    """获取单只股票数据"""
    try:
        ticker = yf.Ticker(symbol)
        
        # 基本信息
        info = ticker.info
        
        # 历史价格 (6个月)
        hist = ticker.history(period="6mo")
        
        # 保存为 CSV
        os.makedirs('data/prices', exist_ok=True)
        hist.to_csv(f'data/prices/{symbol}.csv')
        
        # 保存基本信息为 JSON
        basic_info = {
            'symbol': symbol,
            'name': info.get('longName', symbol),
            'sector': info.get('sector', 'N/A'),
            'industry': info.get('industry', 'N/A'),
            'marketCap': info.get('marketCap', 0),
            'peRatio': info.get('trailingPE', 0),
            'forwardPE': info.get('forwardPE', 0),
            'pegRatio': info.get('pegRatio', 0),
            'priceToBook': info.get('priceToBook', 0),
            'dividendYield': info.get('dividendYield', 0),
            'beta': info.get('beta', 0),
            'fiftyTwoWeekHigh': info.get('fiftyTwoWeekHigh', 0),
            'fiftyTwoWeekLow': info.get('fiftyTwoWeekLow', 0),
            'averageVolume': info.get('averageVolume', 0),
            'currentPrice': info.get('currentPrice', info.get('regularMarketPrice', 0)),
            'previousClose': info.get('previousClose', 0),
            'updatedAt': datetime.now().isoformat()
        }
        
        return basic_info
    except Exception as e:
        print(f"Error fetching {symbol}: {e}")
        return None

def main():
    print(f"开始抓取 {len(STOCKS)} 只股票数据...")
    
    all_data = {}
    
    for i, symbol in enumerate(STOCKS):
        print(f"[{i+1}/{len(STOCKS)}] 抓取 {symbol}...")
        data = fetch_stock_data(symbol)
        if data:
            all_data[symbol] = data
    
    # 保存汇总数据
    os.makedirs('data', exist_ok=True)
    with open('data/stocks.json', 'w') as f:
        json.dump(all_data, f, indent=2)
    
    # 保存更新时间
    with open('data/last_update.txt', 'w') as f:
        f.write(datetime.now().isoformat())
    
    print(f"完成！成功抓取 {len(all_data)} 只股票")

if __name__ == '__main__':
    main()
