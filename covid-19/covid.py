# coding=utf-8
import requests

from bs4 import BeautifulSoup
from pyecharts.charts import Bar
from pyecharts import options as opts
from pyecharts.commons.utils import JsCode
from pyecharts.globals import ThemeType

# 获取数据
req = requests.get('https://www.worldometers.info/coronavirus/')
req.encoding = 'utf-8'

soup = BeautifulSoup(req.text, 'html.parser')

# 获取表格行
result = soup.find(attrs={'id': 'main_table_countries_today'}).find('tbody').find_all('tr')

# 解析数据
countries = []
diagnoses = []
deaths = []
actives = []
recovered = []
new = []


def fix(str):
    if not str:
        return 0
    return str.replace(',', '')


for i in range(40):
    tr = result[i]
    if not tr.has_attr('class'):
        td = tr.find_all('td')
        # 国家
        # print(td[1].text)
        countries.append(td[1].text)
        # 确诊人数
        diagnoses.append(fix(td[2].text))
        # 死亡人数
        deaths.append(fix(td[4].text))
        # 现存确诊人数
        actives.append(fix(td[7].text))
        # 治愈人数
        recovered.append(fix(td[6].text))
        # 新增人数
        new.append(fix(td[3].text))


def formatter(n):
    if len(n) > 4:
        return str(n / 10000) + 'w'



# 生成柱状图
bar = (
    Bar(init_opts=opts.InitOpts(theme=ThemeType.WESTEROS, width='1800px', height='700px'))
    .set_global_opts(
        title_opts=opts.TitleOpts(
            title="疫情分析柱状图",
            subtitle=""
        ),
        datazoom_opts=opts.DataZoomOpts(

        ),
        tooltip_opts=opts.TooltipOpts(

        ),
        toolbox_opts=opts.ToolboxOpts(

        ),
        xaxis_opts=opts.AxisOpts(
            name_gap=30,
            split_number=3,
            name_rotate=60,
            name='国家',
            max_interval=10,
            axislabel_opts={"rotate":45}
        ),
        yaxis_opts=opts.AxisOpts(

            # name_gap=30,
            # split_number=3,
            # name_rotate=60,
            name='人数',
            # max_interval=10,
            axislabel_opts={

                #'formatter': '{b}aaa'
            },

        )
    )
    .set_series_opts(
        label_opts=opts.LabelOpts(is_show=False),
        markpoint_opts=opts.MarkPointOpts(
            data=[
                opts.MarkPointItem(type_='max',name='最大值'),# 最大值标记点
                opts.MarkPointItem(type_='min',name='最小值'),# 最小值标记点
                opts.MarkPointItem(type_='average',name='平均值')# 平均值标记点
            ]
        ),
        formatter=JsCode("""
            function(a){
            var result = [ ], counter = 0;
            var num_array = a.data.toString().split('.');
            var num = num_array[0];
            var newstr = '';
            for (var i = num.length - 1; i >= 0; i--) {
                counter++;
                result.unshift(num[i]);
                if (!(counter % 3) && i != 0) { 
                    result.unshift(',');
                }
            }
            if(num_array.length>1){
                newstr = result.join('');
                newstr += '.'+num_array[1];
                return newstr;
            }else{
                return result.join('');
            }
            }""")
    )
    .add_xaxis(countries)
    .add_yaxis('累计确诊人数', diagnoses)
    .add_yaxis('新增确诊人数', new)
    .add_yaxis('现存确诊人数', actives)
    .add_yaxis('治愈人数', recovered)
    .add_yaxis('死亡人数', deaths)
)

bar.render('covid-19.html')


