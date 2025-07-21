# main.py - 主程序
import time
import pandas as pd
import rqdatac
from config import RQDATA_USER, RQDATA_PASSWORD, REFRESH_INTERVAL
from rqdatac import init
from indicators.market_strength import calculate_3m_lsi
from indicators.limit_up_detector import detect_limit_up

# 初始化RQData
rqdatac.init()

def monitor_market():
    """实时监控市场"""
    try:
        # 获取全市场股票列表
        all_stocks = rqdatac.all_instruments("CS")['order_book_id'].tolist()
        
        while True:
            # 记录当前时间
            current_time = pd.Timestamp.now()
            print(f"\n{'='*50}")
            print(f"监控时间: {current_time}")
            
            # 计算全市场LSI
            lsi_values = calculate_3m_lsi(all_stocks)
            if not lsi_values.empty:
                print(f"全市场3m-LSI均值: {lsi_values.mean():.4f}")
            
            # 检测涨停股
            limit_up_stocks = detect_limit_up(all_stocks)
            if limit_up_stocks:
                print(f"当前涨停股数量: {len(limit_up_stocks)}")
                print(f"部分涨停股: {limit_up_stocks[:5]}...")
                
                # 分析龙头股概念
                if len(limit_up_stocks) > 0:
                    lead_stock = limit_up_stocks[0]
                    try:
                        # 获取龙头股所属概念
                        concepts = rqdatac.concept("stock", lead_stock)
                        if concepts:
                            print(f"龙头股 {lead_stock} 所属概念: {concepts}")
                            
                            # 分析每个概念强度
                            for concept in concepts:
                                # 获取概念成分股
                                members = rqdatac.concept("concept", concept)
                                if members and len(members) > 0:
                                    # 计算概念LSI
                                    concept_lsi = calculate_3m_lsi(members)
                                    if not concept_lsi.empty:
                                        avg_lsi = concept_lsi.mean()
                                        print(f"概念 {concept} - 3m-LSI: {avg_lsi:.4f}, 成分股: {len(members)}")
                                        
                                        # 触发预警条件
                                        if avg_lsi > 2.0:
                                            print(f"!!! 概念 {concept} 触发预警 (LSI={avg_lsi:.2f}) !!!")
                                            print("建议关注该概念未涨停个股")
                    except Exception as e:
                        print(f"分析龙头股概念时出错: {e}")
            else:
                print("当前无涨停股")
            
            # 等待指定间隔后再次检查
            print(f"等待{REFRESH_INTERVAL//60}分钟后再次检查...")
            time.sleep(REFRESH_INTERVAL)
            
    except KeyboardInterrupt:
        print("\n监控已停止")
    except Exception as e:
        print(f"监控过程中出现错误: {e}")

if __name__ == "__main__":
    print("启动异动盯盘系统...")
    monitor_market()