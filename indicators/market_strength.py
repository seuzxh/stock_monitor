# indicators/market_strength.py - 市场强度指标
import pandas as pd
from rqdatac import *
import rqdatac

def calculate_3m_lsi(order_book_ids, window=3):
    """
    计算3分钟联动强度指数
    
    参数:
        order_book_ids: 股票代码列表
        window: 时间窗口(分钟)
        
    返回:
        pd.Series: 各股票的LSI值
    """
    try:
        # 获取实时行情数据
        snapshot = rqdatac.get_live_ticks (
            order_book_ids=order_book_ids,
            fields=["last", "volume", "total_turnover"]
        )
        
        # 计算3分钟涨跌幅
        price_change = snapshot['last'].pct_change(periods=window)
        
        # 计算成交量放大系数（当前成交量/过去20日均量）
        vol_ma = snapshot['volume'].rolling(window=20).mean().iloc[-1]
        vol_factor = snapshot['volume'] / vol_ma
        
        # 计算LSI = (涨跌幅 * 成交量系数) / 股票数量
        lsi = (price_change * vol_factor) / len(order_book_ids)
        return lsi
        
    except Exception as e:
        print(f"计算LSI时出错: {e}")
        return pd.Series()