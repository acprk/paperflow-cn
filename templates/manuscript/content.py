# -*- coding: utf-8 -*-
"""稿件内容的“单一来源”（single source of truth）。

所有正文、摘要、表格、图题、参考文献都只写在这里；build_docx.py 读取本文件生成 Word。
这样做的好处：
- 修改只改一处，Word / PDF / 纯文本永远一致；
- 引文按首次出现自动编号，删改段落不会弄乱编号；
- 可用 tools/check_consistency.py 逐段核对 Word 是否包含本文件的全部内容。

写作约定：
- 引文写作 [@key] 或 [@key1,@key2]，key 必须在 REFDB 中；
- 未确认的信息一律写成【待填】，不得编造（作者信息、页码、版本、数据）；
- 每条参考文献都要能在公开来源核实（见 INTEGRITY.md）。
"""
import os
import re

import journal_style as S

TITLE = '【论文题目】'
SUBTITLE = ''
AUTHOR = '【作者姓名】'
AFFIL = '（【单位】，【省份】 【城市】 【邮编】）'
CLC = ''                  # 例：'中图分类号：J60　　文献标识码：A'（期刊要求时填写）
EN_TITLE = ''             # 期刊要求英文摘要时填写，否则留空
EN_AUTHOR = EN_AFFIL = EN_ABSTRACT = EN_KEYWORDS = ''

ABSTRACT = ('【摘要：交代研究对象、问题、方法或思路、主要内容与边界。一般 200—300 字，'
            '第三人称写法，不以“本文”作主语（以目标期刊稿约为准）。】')
KEYWORDS = '【关键词1】；【关键词2】；【关键词3】'

# ---------------- 参考文献（GB/T 7714 著录；每条须可核实，并尽量标实引页码） ----------------
REFDB = {
    'demo2020': '【作者】. 【题名】[J]. 【刊名】, 2020(1): 1-10.',
    'demo2021': '【作者】. 【书名】[M]. 【出版地】: 【出版者】, 2021: 23-25.',
}

# ---------------- 表格：key -> (表题, 表头, 行, 列宽比例) ----------------
TABLES = {
    'demo': ('表1  【表题】', ['【列1】', '【列2】', '【列3】'],
             [['【内容】', '【内容】', '【内容】'],
              ['【内容】', '【内容】', '【内容】']],
             [0.25, 0.45, 0.30]),
}

# ---------------- 图片：key -> (图片路径, 题注) ；题注位置见 journal_style.CAPTION ----------------
HERE = os.path.dirname(os.path.abspath(__file__))
FIGS = {}              # 例：{'f1': (os.path.join(HERE, 'figures', 'f1.png'), '图1  【图题】')}
SCORE_KEYS = set()     # 属于“谱例”的图（题注放在谱上居左）

# ---------------- 正文 ----------------
B = []
h1 = lambda t: B.append(('h1', t))
h2 = lambda t: B.append(('h2', t))
fig = lambda k: B.append(('fig', k))
table = lambda k: B.append(('table', k))


def p(*xs):
    for x in xs:
        B.append(('p', x))


p('【引言：问题的提出、已有研究（含最相近研究的比较）、本文的增量与讨论范围】[@demo2020]。')
h1('一、【一级标题】')
h2('（一）【二级标题】')
p('【正文段落】[@demo2021]。')
table('demo')
h1('结　语')
p('【结语：概括、边界与后续工作】。')

FUND = ''   # 如有：按期刊格式，例如 '[基金项目] 项目名称（项目编号）'
AUTHOR_BIO = '作者简介：【姓名】（【出生年】—），【性别】，【单位】【职称/学历】，研究方向：【方向】。（【城市】 【邮编】）'

# ---------------- 引文编号（按首次出现顺序） ----------------
_order = []


def _cite(m):
    keys = [k.strip().lstrip('@') for k in m.group(1).split(',')]
    nums = []
    for k in keys:
        if k not in REFDB:
            raise KeyError('未知文献键：' + k)
        if k not in _order:
            _order.append(k)
        nums.append(_order.index(k) + 1)
    nums = sorted(set(nums))
    if S.CITE_STYLE == 'separate':
        return ''.join('[%d]' % n for n in nums)
    return '[' + ','.join(str(n) for n in nums) + ']'


B = [(b[0], re.sub(r'\[(@[^\]]+)\]', _cite, b[1])) if b[0] == 'p' else b for b in B]
REFS = ['[%d] %s' % (i + 1, REFDB[k]) for i, k in enumerate(_order)]
UNUSED = [k for k in REFDB if k not in _order]
BODY_CHARS = sum(len(b[1]) for b in B if b[0] == 'p')
