# -*- coding: utf-8 -*-
"""核对 Word 成稿与 content.py 是否逐段一致，并统计字数。

用法：python tools/check_consistency.py <稿件目录(含content.py)> <成稿.docx>
退出码：0 = 一致；1 = 有缺失（会列出缺失段落的开头）。
原理：用 pandoc 把 docx 转成纯文本，去掉空白后检查 content.B 中每一段正文、每条注释是否都出现在其中。
"""
import os
import subprocess
import sys
import tempfile


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    src, docx = sys.argv[1], sys.argv[2]
    sys.path.insert(0, os.path.abspath(src))
    import content as C

    with tempfile.TemporaryDirectory() as td:
        txt = os.path.join(td, 'out.txt')
        subprocess.run(['pandoc', docx, '-t', 'plain', '-o', txt], check=True)
        plain = open(txt, encoding='utf-8').read()
    flat = ''.join(plain.split())

    items = [('正文', b[1]) for b in C.B if b[0] == 'p'] + [('注释', r) for r in C.REFS]
    items += [('摘要', C.ABSTRACT), ('关键词', C.KEYWORDS), ('作者简介', C.AUTHOR_BIO)]
    missing = [(k, v[:40]) for k, v in items if ''.join(v.split()) not in flat]

    cjk = sum(1 for ch in flat if '一' <= ch <= '鿿')
    print('正文段落 %d | 注释 %d | 未引用文献 %s' % (sum(1 for b in C.B if b[0] == 'p'), len(C.REFS), C.UNUSED))
    print('全文非空白字符 %d | 汉字 %d | 正文段落字符 %d' % (len(flat), cjk, C.BODY_CHARS))
    todo = flat.count('【')
    if todo:
        print('提示：成稿中还有 %d 处【待填】标记' % todo)
    if missing:
        print('不一致：以下内容未出现在 Word 中')
        for k, v in missing:
            print('  [%s] %s' % (k, v))
        sys.exit(1)
    print('一致性核对通过')


if __name__ == '__main__':
    main()
