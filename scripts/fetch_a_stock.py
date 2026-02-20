#!/usr/bin/env python3
"""
A股数据抓取脚本 - 使用 akshare (国内数据源)
"""

import akshare as ak
import pandas as pd
import json
import os
from datetime import datetime

# A股股票列表 - 沪深300成分股 + 热门股票
STOCKS = {
    # 金融
    '600519': '贵州茅台', '601398': '工商银行', '601857': '中国石油',
    '601288': '农业银行', '601988': '中国银行', '601628': '中国人寿',
    '600036': '招商银行', '601318': '中国平安', '600276': '恒瑞医药',
    # 科技
    '000858': '五粮液', '002594': '比亚迪', '300750': '宁德时代',
    '000333': '美的集团', '002415': '海康威视', '000725': '京东方A',
    '002230': '科大讯飞', '300059': '东方财富', '002371': '北方华创',
    # 新能源
    '601012': '隆基绿能', '300014': '亿纬锂能', '002460': '赣锋锂业',
    '300124': '汇川技术', '002709': '天赐材料', '300450': '先导智能',
    # 消费
    '000568': '泸州老窖', '000651': '格力电器', '002304': '洋河股份',
    '600887': '伊利股份', '600809': '山西汾酒', '000895': '双汇发展',
    # 医药
    '600276': '恒瑞医药', '000538': '云南白药', '600436': '片仔癀',
    '300122': '智飞生物', '300760': '迈瑞医疗', '603259': '药明康德',
    # 汽车
    '601633': '长城汽车', '600104': '上汽集团', '000625': '长安汽车',
    '601127': '赛力斯', '600066': '宇通客车',
    # 半导体
    '603501': '韦尔股份', '688981': '中芯国际', '603893': '瑞芯微',
    '600584': '长电科技', '002049': '紫光国微',
    # 通信
    '600941': '中国移动', '600050': '中国联通', '000063': '中兴通讯',
    # 指数
    '000001': '上证指数', '399001': '深证成指', '399006': '创业板指',
    '000300': '沪深300', '000905': '中证500',
}

def fetch_stock_data(symbol, name):
    """获取单只股票数据"""
    try:
        # 判断市场
        if symbol.startswith('6'):
            market = 'sh'
        elif symbol.startswith('0') or symbol.startswith('3'):
            market = 'sz'
        elif symbol.startswith('688'):
            market = 'sh'
        else:
            market = 'sh'
        
        full_code = f"{market}{symbol}"
        
        # 获取历史数据
        df = ak.stock_zh_a_hist(symbol=symbol, period="daily", 
                                start_date="20240101", adjust="qfq")
        
        if df.empty:
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
                    'market': 'SH' if market == 'sh' else 'SZ',
                    'currentPrice': float(latest.get('最新价', 0)),
                    'previousClose': float(latest.get('昨收', 0)),
                    'open': float(latest.get('今开', 0)),
                    'high': float(latest.get('最高', 0)),
                    'low': float(latest.get('最低', 0)),
                    'volume': int(latest.get('成交量', 0)),
                    'amount': float(latest.get('成交额', 0)),
                    'pe': float(latest.get('市盈率-动态', 0) or 0),
                    'pb': float(latest.get('市净率', 0) or 0),
                    'totalMarketCap': float(latest.get('总市值', 0) or 0),
                    'circulatingMarketCap': float(latest.get('流通市值', 0) or 0),
                    'turnover': float(latest.get('换手率', 0) or 0),
                    'amplitude': float(latest.get('振幅', 0) or 0),
                    'change': float(latest.get('涨跌幅', 0) or 0),
                    'updatedAt': datetime.now().isoformat()
                }
            else:
                # 从历史数据获取最新
                latest_row = df.iloc[-1]
                basic_info = {
                    'symbol': symbol,
                    'name': name,
                    'market': 'SH' if market == 'sh' else 'SZ',
                    'currentPrice': float(latest_row['收盘']),
                    'previousClose': float(latest_row['收盘']),
                    'volume': int(latest_row['成交量']),
                    'updatedAt': datetime.now().isoformat()
                }
        except Exception as e:
            print(f"  获取实时行情失败: {e}")
            latest_row = df.iloc[-1]
            basic_info = {
                'symbol': symbol,
                'name': name,
                'market': 'SH' if market == 'sh' else 'SZ',
                'currentPrice': float(latest_row['收盘']),
                'previousClose': float(latest_row['收盘']),
                'volume': int(latest_row['成交量']),
                'updatedAt': datetime.now().isoformat()
            }
        
        return basic_info
        
    except Exception as e:
        print(f"  Error: {e}")
        return None

def main():
    print(f"开始抓取 {len(STOCKS)} 只A股数据...")
    print("数据源: 东方财富 (akshare)")
    
    all_data = {}
    failed = []
    
    for i, (symbol, name) in enumerate(STOCKS.items()):
        print(f"[{i+1}/{len(STOCKS)}] {symbol} {name}...", end=" ")
        data = fetch_stock_data(symbol, name)
        if data:
            all_data[symbol] = data
            print(f"✓ 价格: {data['currentPrice']:.2f}")
        else:
            failed.append(symbol)
            print("✗ 失败")
    
    # 保存汇总数据
    os.makedirs('data', exist_ok=True)
    with open('data/stocks.json', 'w', encoding='utf-8') as f:
        json.dump(all_data, f, indent=2, ensure_ascii=False)
    
    # 保存更新时间
    with open('data/last_update.txt', 'w') as f:
        f.write(datetime.now().isoformat())
    
    # 保存失败列表
    if failed:
        with open('data/failed.txt', 'w') as f:
            f.write('\n'.join(failed))
    
    print(f"\n完成！成功: {len(all_data)}, 失败: {len(failed)}")
    if failed:
        print(f"失败列表: {', '.join(failed)}")

if __name__ == '__main__':
    main()
