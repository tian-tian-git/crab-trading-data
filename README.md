# 蟹爪交易数据

自动抓取的股票数据仓库，每 6 小时更新一次。

## 数据文件

- `data/stocks.json` - 所有股票的基本信息汇总
- `data/prices/*.csv` - 各股票历史价格数据
- `data/last_update.txt` - 最后更新时间

## 股票列表

美股：AAPL, MSFT, GOOGL, AMZN, TSLA, NVDA, META, NFLX, AMD, CRM, PYPL, UBER, COIN, PLTR...
中概股：BABA, JD, NIO, XPEV, LI, PDD...
金融：JPM, BAC, GS, MS, WFC...
ETF：SPY, QQQ, IWM, VTI, VOO...
加密货币：BTC-USD, ETH-USD

## 更新时间

- 自动：每 6 小时 (UTC)
- 手动：可通过 Actions 页面触发
