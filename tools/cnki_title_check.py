# -*- coding: utf-8 -*-
"""打开知网“知网节”详情页，读取篇名，用于核实“某刊某期确有此文”（期刊是否仍被知网收录的证据）。

用法：python tools/cnki_title_check.py <知网详情页URL> [<URL> ...]
说明：
- 国内主站（kns/navi.cnki.net）在部分网络环境下无法直连，可改用海外版
  https://oversea.cnki.net/kcms/detail/detail.aspx?dbcode=CJFD&filename=<文件名> 。
- 只读取公开的题录页标题，不下载全文，不绕过任何访问控制。
- 能打开且篇名、刊名、年期与预期一致，才记为“已核实”；打不开不等于不存在，记为“未核实”。
"""
import re
import subprocess
import sys
import urllib.request

UA = {'User-Agent': 'Mozilla/5.0 (paperflow-cn reference check)'}


def fetch(url):
    """先用 urllib；失败时退回 curl（部分网络环境下 urllib 的代理/TLS 处理与 curl 不同）。"""
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.read().decode('utf-8', 'ignore')
    except Exception:  # noqa: BLE001
        out = subprocess.run(['curl', '-sL', '-m', '30', '-A', UA['User-Agent'], url],
                             capture_output=True, check=True)
        return out.stdout.decode('utf-8', 'ignore')


def title_of(url):
    html = fetch(url)
    m = re.search(r'<title>([^<]*)</title>', html)
    return m.group(1).replace(' - 中国知网', '').strip() if m else ''


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    for url in sys.argv[1:]:
        try:
            t = title_of(url)
            status = '已打开' if t and t != '知网节' else '页面无篇名（可能文件名不对）'
        except Exception as e:  # noqa: BLE001
            t, status = '', '无法访问：%s' % e.__class__.__name__
        print('%s\t%s\t%s' % (status, t, url))


if __name__ == '__main__':
    main()
