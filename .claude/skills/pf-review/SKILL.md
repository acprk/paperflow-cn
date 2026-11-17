---
name: pf-review
description: paperflow-cn P4/P5/P7——用 Codex CLI（只读）组织多轮模拟审稿：首轮与复审、全新审稿组专业事实核查（可并行加一个独立子代理交叉核查）、投稿前体例与语言终审。用户要求“模拟审稿”“codex 审稿”“评估中稿率”时使用。
---

# P4/P5/P7 模拟审稿

1. 导出稿件纯文本到 `reviews/revised_rN.txt`。
2. 选模板（见 prompts/README.md），填占位符：
   `python tools/inline_prompt.py prompts/<模板>.md reviews/PROMPT_xx.md JOURNAL=… MANUSCRIPT=reviews/revised_rN.txt …`
   若 Codex 沙箱读不到文件，用 `KEY=@文件路径` 或 `{{FILE:路径}}` 把全文内联。
3. 后台运行：`tools/run_codex.sh <稿件目录> reviews/PROMPT_xx.md reviews/CODEX_xx.md`。
4. P5 时并行派 **pf-fact-checker**（互不知情），两份结果交叉比对。
5. 逐条核实审稿意见（打开链接、核对原文），分为：助手可改 / 须作者完成 / 不属实；可改项交 P3。
6. 复审直到结论为“可以投稿/修改后可投”，并把每轮录用估计记入 `reviews/SUMMARY.md`。

## 闸门 G4（进入 P8 之前）
- [ ] 至少两组互不知情的审稿均未发现确定的专业错误；
- [ ] 所有“助手可改”的问题已修改并经复审确认；
- [ ] 终审（final_check）的体例清单无“不符合”项，或已列为作者待办。
