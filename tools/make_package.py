# -*- coding: utf-8 -*-
"""生成投稿包：Word 正文、预览 PDF、图片原图、投稿邮件/检查清单/作者信息表，并写 SHA256SUMS、打 zip。

用法：
  python tools/make_package.py --src <稿件目录> --name <文件名前缀> --out <投稿包目录> [--extra 文件 ...]
示例：
  python tools/make_package.py --src examples/demo --name 作者-论文题目 --out build/submission

步骤：build_docx.py 生成 Word → LibreOffice 转预览 PDF → check_consistency 逐段核对（不一致则中止）
→ 复制图片与附加文件 → 从 templates/ 复制投稿邮件、检查清单、作者信息表（若投稿包中尚无）→ sha256 → zip。
"""
import argparse
import hashlib
import os
import shutil
import subprocess
import sys
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES = os.path.join(ROOT, 'templates')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--src', required=True, help='含 content.py / journal_style.py / build_docx.py 的稿件目录')
    ap.add_argument('--name', required=True, help='投稿文件名前缀，如“作者-论文题目”')
    ap.add_argument('--out', required=True, help='投稿包输出目录')
    ap.add_argument('--extra', nargs='*', default=[], help='额外放入投稿包的文件（如谱例源文件、检测报告）')
    a = ap.parse_args()

    src = os.path.abspath(a.src)
    out = os.path.abspath(a.out)
    os.makedirs(out, exist_ok=True)
    build = os.path.join(src, 'build')
    docx = os.path.join(build, a.name + '.docx')

    subprocess.run([sys.executable, os.path.join(src, 'build_docx.py'), docx], check=True, cwd=src)
    pdf = docx[:-5] + '.pdf'
    profile = 'file://' + os.path.join(build, '.lo_profile')     # 独立配置目录，避免与已打开的 LibreOffice 冲突
    try:
        subprocess.run(['soffice', '-env:UserInstallation=' + profile, '--headless', '--convert-to', 'pdf',
                        '--outdir', build, docx], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                       timeout=300)
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
        pass
    if not os.path.exists(pdf):
        print('提示：LibreOffice 转换预览 PDF 失败，本次投稿包不含预览 PDF（不影响 Word 投稿稿）')
    r = subprocess.run([sys.executable, os.path.join(ROOT, 'tools', 'check_consistency.py'), src, docx])
    if r.returncode != 0:
        sys.exit('Word 与 content.py 不一致，已中止打包')

    shutil.copy(docx, os.path.join(out, a.name + '.docx'))
    if os.path.exists(pdf):
        shutil.copy(pdf, os.path.join(out, a.name + '_预览.pdf'))
    sys.path.insert(0, src)
    import content as C
    for key, (path, _cap) in getattr(C, 'FIGS', {}).items():
        shutil.copy(path, os.path.join(out, '%s-%s%s' % (a.name, key, os.path.splitext(path)[1])))
    for f in a.extra:
        shutil.copy(f, os.path.join(out, os.path.basename(f)))
    for t in ('投稿邮件_推荐文本.txt', '投稿前检查清单.txt', '作者信息填写表.txt'):
        dst = os.path.join(out, t)
        if not os.path.exists(dst):
            shutil.copy(os.path.join(TEMPLATES, t), dst)

    files = sorted(f for f in os.listdir(out) if f != 'SHA256SUMS.txt' and not f.endswith('.zip'))
    with open(os.path.join(out, 'SHA256SUMS.txt'), 'w', encoding='utf-8') as fh:
        for f in files:
            fh.write(hashlib.sha256(open(os.path.join(out, f), 'rb').read()).hexdigest() + '  ' + f + '\n')
    zpath = out.rstrip('/') + '.zip'
    base = os.path.basename(out.rstrip('/'))
    with zipfile.ZipFile(zpath, 'w', zipfile.ZIP_DEFLATED) as z:
        for f in files + ['SHA256SUMS.txt']:
            z.write(os.path.join(out, f), os.path.join(base, f))
    print('投稿包：', zpath)
    for f in files:
        print('   ', f)


if __name__ == '__main__':
    main()
