# visualization/concept_heatmap.py - 可视化模块
from pyecharts.charts import HeatMap
from pyecharts import options as opts

def plot_concept_heatmap(concepts_data):
    """
    生成概念热力图
    
    参数:
        concepts_data: 格式为[[概念名称, LSI值], ...]
        
    返回:
        pyecharts.charts.HeatMap: 热力图对象
    """
    heatmap = HeatMap()
    heatmap.add_xaxis([x[0] for x in concepts_data])
    heatmap.add_yaxis("LSI", [x[1] for x in concepts_data])
    heatmap.set_global_opts(
        title_opts=opts.TitleOpts(title="3分钟概念联动强度"),
        visualmap_opts=opts.VisualMapOpts(max_=3, min_=0.5)
    )
    return heatmap