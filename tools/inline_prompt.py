# -*- coding: utf-8 -*-
"""填充提示词模板中的占位符，输出可直接交给 Codex 的提示词文件。

用法：
  python tools/inline_prompt.py <模板.md> <输出.md> KEY=值 [KEY=值 ...]
- 普通占位符：{{JOURNAL}}、{{MANUSCRIPT}} 等，用 KEY=值 替换；
- 文件内联：模板中写 {{FILE:相对或绝对路径}}，脚本会把该文件全文嵌入（用于 Codex 沙箱读不到文件的环境）；
  也可以用 KEY=@路径 把某个占位符替换为文件全文。
"""
import os
import re
import sys


def read(path):
    with open(path, encoding='utf-8') as fh:
        return fh.read()


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    tpl, out = sys.argv[1], sys.argv[2]
    text = read(tpl)
    for kv in sys.argv[3:]:
        k, v = kv.split('=', 1)
        if v.startswith('@'):
            v = '\n<<<文件 %s 开始>>>\n%s\n<<<文件结束>>>\n' % (v[1:], read(v[1:]))
        text = text.replace('{{%s}}' % k, v)
    text = re.sub(r'\{\{FILE:([^}]+)\}\}',
                  lambda m: '\n<<<文件 %s 开始>>>\n%s\n<<<文件结束>>>\n' % (m.group(1), read(m.group(1))), text)
    left = sorted(set(re.findall(r'\{\{([A-Z_]+)\}\}', text)))
    with open(out, 'w', encoding='utf-8') as fh:
        fh.write(text)
    print('已生成', out, '| 未填占位符：', left or '无')


if __name__ == '__main__':
    main()
