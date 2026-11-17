# -*- coding: utf-8 -*-
"""发布或分享前的隐私扫描：查找邮箱、手机号、身份证号、本机绝对路径、令牌样式字符串，以及自定义敏感词。

用法：python tools/privacy_scan.py <目录> [--words 敏感词文件]
敏感词文件：每行一个词（例如真实姓名、单位、具体论文题目），不要把这个文件本身提交到公开仓库。
退出码：0 = 未发现；1 = 发现可疑内容（逐条列出文件与行号）。
"""
import os
import re
import sys

PATTERNS = {
    '邮箱': re.compile(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'),
    '手机号': re.compile(r'(?<!\d)1[3-9]\d{9}(?!\d)'),
    '身份证号': re.compile(r'(?<!\d)\d{17}[\dXx](?!\d)'),
    '本机路径': re.compile(r'/home/[A-Za-z0-9_.-]+/|/Users/[A-Za-z0-9_.-]+/|[A-Z]:\\\\Users\\\\'),
    '令牌': re.compile(r'gh[pousr]_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}'),
}
SKIP_DIRS = {'.git', '__pycache__', 'build'}
TEXT_EXT = {'.md', '.txt', '.py', '.sh', '.tex', '.json', '.yml', '.yaml', '.toml', '.cfg', ''}
ALLOW = {'example@example.com', 'noreply@example.com'}


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    root = sys.argv[1]
    words = []
    if '--words' in sys.argv:
        wf = sys.argv[sys.argv.index('--words') + 1]
        words = [w.strip() for w in open(wf, encoding='utf-8') if w.strip()]
    hits = []
    for d, dirs, files in os.walk(root):
        dirs[:] = [x for x in dirs if x not in SKIP_DIRS]
        for f in files:
            if os.path.splitext(f)[1].lower() not in TEXT_EXT:
                continue
            path = os.path.join(d, f)
            try:
                lines = open(path, encoding='utf-8').read().splitlines()
            except UnicodeDecodeError:
                continue
            for i, line in enumerate(lines, 1):
                for name, pat in PATTERNS.items():
                    for m in pat.findall(line):
                        if m not in ALLOW:
                            hits.append((path, i, name, m))
                for w in words:
                    if w in line:
                        hits.append((path, i, '敏感词', w))
    for path, i, name, m in hits:
        print('%s:%d\t%s\t%s' % (os.path.relpath(path, root), i, name, m))
    print('发现 %d 处可疑内容' % len(hits) if hits else '未发现可疑内容')
    sys.exit(1 if hits else 0)


if __name__ == '__main__':
    main()
