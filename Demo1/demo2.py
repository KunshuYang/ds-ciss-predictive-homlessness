from pyecharts import options as opts
from pyecharts.charts import Map
from pyecharts.faker import Faker
import pandas as pd
import json
from pyecharts.commons.utils import JsCode

# 读取数据
file_path = 'C:/Users/ykks/Desktop/zuoye/spark/final_dataset.csv'
df = pd.read_csv(file_path)

# 提取州信息并计算每个州的无家可归人数
df['State'] = df['CoC Number'].str[:2]
state_data = df[df['Homelessness.Type'] == 'Overall.Homeless'].groupby('State')['Count'].sum().reset_index()

# 创建州名和州简称的映射
state_abbrev = {
    'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas', 'CA': 'California',
    'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware', 'FL': 'Florida', 'GA': 'Georgia',
    'HI': 'Hawaii', 'ID': 'Idaho', 'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa',
    'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine', 'MD': 'Maryland',
    'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota', 'MS': 'Mississippi', 'MO': 'Missouri',
    'MT': 'Montana', 'NE': 'Nebraska', 'NV': 'Nevada', 'NH': 'New Hampshire', 'NJ': 'New Jersey',
    'NM': 'New Mexico', 'NY': 'New York', 'NC': 'North Carolina', 'ND': 'North Dakota', 'OH': 'Ohio',
    'OK': 'Oklahoma', 'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island', 'SC': 'South Carolina',
    'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah', 'VT': 'Vermont',
    'VA': 'Virginia', 'WA': 'Washington', 'WV': 'West Virginia', 'WI': 'Wisconsin', 'WY': 'Wyoming'
}

# 将州简称转换为完整州名
state_data['State'] = state_data['State'].map(state_abbrev)

# 创建地图
map_chart = Map()
map_chart.add("Homeless Population", [list(z) for z in zip(state_data['State'], state_data['Count'])], "美国")

# 设置全局选项
map_chart.set_global_opts(
    title_opts=opts.TitleOpts(
        title="USA Homeless Population Estimates",
        subtitle="Data from your dataset",
        pos_left="right"
    ),
    visualmap_opts=opts.VisualMapOpts(
        min_=state_data['Count'].min(),
        max_=state_data['Count'].max(),
        is_calculable=True,
        range_color=["#313695", "#4575b4", "#74add1", "#abd9e9", "#e0f3f8", "#ffffbf", 
                     "#fee090", "#fdae61", "#f46d43", "#d73027", "#a50026"],
        pos_left="right",
        pos_top="center"
    ),
    tooltip_opts=opts.TooltipOpts(
        trigger="item",
        formatter=JsCode(
            """
            function(params) {
                return params.name + ': ' + params.value;
            }
            """
        )
    ),
    toolbox_opts=opts.ToolboxOpts(
        is_show=True,
        orient="vertical",
        pos_left="left",
        pos_top="top",
        feature={
            "dataView": {"readOnly": False},
            "restore": {},
            "saveAsImage": {}
        }
    )
)

# 设置系列选项
map_chart.set_series_opts(
    label_opts=opts.LabelOpts(is_show=False),
    emphasis_opts=opts.EmphasisOpts(
        label_opts=opts.LabelOpts(is_show=True)
    )
)

# 生成HTML文件
map_chart.render("usa_homeless_population_custom.html")

print("Map has been generated as 'usa_homeless_population_custom.html'")