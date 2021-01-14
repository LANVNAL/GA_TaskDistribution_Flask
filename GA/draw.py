import pyecharts.options as opts
from pyecharts.charts import Scatter
from pyecharts.faker import Faker
from pyecharts.commons.utils import JsCode
from .GA import getResultData
import time


def drawFromData():
    result = getResultData()
    x_data=[]
    y_data=[]
    # print(len(result))
    for x in range(len(result)):
        xtmp= [x] * len(result[x])
        x_data += xtmp
        y_data += result[x]
    # print(x_data)
    scatter1 = (
        Scatter(init_opts=opts.InitOpts(width="1000px", height="500px"))
            .add_xaxis(xaxis_data=x_data, )
            .add_yaxis(
            series_name="任务处理时间",
            y_axis=y_data,
            symbol_size=5,
            label_opts=opts.LabelOpts(is_show=False),
        )
            .set_series_opts()
            .set_global_opts(
            xaxis_opts=opts.AxisOpts(
                type_="value", splitline_opts=opts.SplitLineOpts(is_show=True)
            ),
            title_opts=opts.TitleOpts(title='基于遗传算法的服务器负载均衡调度策略'),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
            ),
            tooltip_opts=opts.TooltipOpts(is_show=False),
        )
    )
    timenow = int(time.time())
    echart_name = 'echarts-scatter-{}.html'.format(timenow)
    scatter1.render('./static/echarts/' + echart_name)
    return echart_name
