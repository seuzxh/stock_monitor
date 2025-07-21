# indicators/limit_up_detector.py - 涨停检测模块
import pandas as pd
from rqdatac import *
import rqdatac

def detect_limit_up(order_book_ids):
    """
    检测涨停股票
    
    参数:
        order_book_ids: 股票代码列表
        
    返回:
        list: 涨停股票代码列表
    """
    try:
        # 获取实时行情数据
        snapshot = rqdatac.get_live_ticks (
            order_book_ids=order_book_ids,
            fields=["close", "prev_close"]
        )
        
        # 计算涨跌幅
        pct_chg = (snapshot['close'] - snapshot['prev_close']) / snapshot['prev_close'] * 100
        
        # 筛选涨停股（涨跌幅≥9.95%）
        limit_up = pct_chg >= 9.95
        
        # 返回涨停股代码列表
        return [order_book_ids[i] for i, is_limit in enumerate(limit_up) if is_limit]
        
    except Exception as e:
        print(f"检测涨停时出错: {e}")
        return []