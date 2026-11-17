# -*- coding: utf-8 -*-
"""期刊版式配置。build_docx.py 读取这里的参数。按目标期刊的稿约修改，不要改 build_docx.py。

常见中文期刊体例（以目标期刊最新稿约/刊内启事为准）：
- 正文宋体小四(12pt)或五号(10.5pt)，1.5 倍行距，首行缩进两字；
- 一级标题“一、”居中加粗，二级标题“（一）”首行缩进加粗，三级标题“1.”不加粗；
- 注释：尾注 [n]（顺序编码），或页下注 ①②（须另行改写）；
- 作者简介放首页脚注或文末；基金项目格式各刊不同。
"""

PAGE = dict(width_mm=210, height_mm=297, top_cm=2.6, bottom_cm=2.5, left_cm=2.8, right_cm=2.6)

FONT = dict(
    body_east='宋体', body_latin='Times New Roman', body_pt=12, line_spacing=1.5, first_indent_pt=24,
    title_east='黑体', title_pt=18,
    author_east='楷体', author_pt=12,
    abstract_label_east='黑体', abstract_east='楷体', abstract_pt=10.5,
    h1_east='宋体', h1_pt=12, h1_align='center',      # center / left
    h2_east='宋体', h2_pt=12, h2_indent_pt=24,
    caption_east='黑体', caption_pt=10,
    table_pt=9,
    ref_pt=10.5,
    header_east='楷体', header_pt=9,
)

LABELS = dict(abstract='摘　要：', keywords='关键词：', refs_heading='注释')   # 有的刊用“参考文献”

# 题注位置：表题在表上居中；图题在图下居中；谱例题在谱上居左（若期刊要求不同，在此修改）
CAPTION = dict(table='above-center', figure='below-center', score='above-left')

# 并引写法：'separate' -> [7][8]；'combined' -> [7,8]
CITE_STYLE = 'separate'

HEADER_SHOWS_TITLE = True
