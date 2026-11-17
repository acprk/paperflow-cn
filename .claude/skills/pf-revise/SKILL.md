---
name: pf-revise
description: paperflow-cn P3——把稿件迁入单一内容源 content.py，按目标期刊版式（journal_style.py）生成 Word，按评估说明、文献核查表与审稿意见逐条修改并做一致性核对。任何改稿都走这个流程。
---

# P3 修订

1. `cp -r templates/manuscript <稿件目录>/paper`，修改 `journal_style.py` 以匹配目标期刊稿约。
2. 把原稿迁入 `content.py`：摘要、关键词、正文（`h1/h2/p/table/fig`）、`REFDB`、作者简介（个人信息留【待填】）。
3. 修改：交给 **pf-revision-editor**，或自己用编辑工具逐处修改（不要写批量替换脚本）。
4. 生成与核对：
   ```
   python paper/build_docx.py paper/build/稿件.docx
   python tools/check_consistency.py paper paper/build/稿件.docx
   soffice --headless --convert-to pdf --outdir paper/build paper/build/稿件.docx
   ```
5. 渲染 PDF 页面抽查：注释页、表格页、图片/谱例页。

## 闸门 G3
- [ ] 一致性核对通过；摘要/引言/结语与正文一致；
- [ ] 每轮修改前已备份；
- [ ] 所有【待填】都是只能由作者提供的信息；
- [ ] 语言修改未改动事实、数字、引文编号与论点强度。
