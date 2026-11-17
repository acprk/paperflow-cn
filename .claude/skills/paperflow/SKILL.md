---
name: paperflow
description: paperflow-cn 总纲——中文学术期刊稿件从“发稿评估”到“投稿包”的端到端工作流（P0 评估 → P1 期刊核实 → P2 文献核实 → P3 修订 → P4 多轮模拟审稿 → P5 独立事实核查 → P6 查新与挖掘 → P7 终审 → P8 投稿包）。用户要评估一篇稿件能否发表、要改稿、要模拟审稿或要做投稿包时使用。
---

# paperflow-cn 总纲

先读仓库根目录的 `WORKFLOW.md`（阶段与闸门）和 `INTEGRITY.md`（诚信红线），再按阶段执行。

## 阶段 → skill → agent

| 阶段 | 做什么 | skill | agent |
|---|---|---|---|
| P0 | 发稿评估说明（问题清单+工作量，不报价） | pf-evaluate | pf-intake-evaluator |
| P1 | 期刊核实（收录证据、官方渠道、稿约、仿冒警示） | pf-venue | pf-venue-verifier |
| P2 | 参考文献核实（著录、原文内容、实引页码） | pf-refs | pf-reference-verifier |
| P3 | 迁入单一内容源并按期刊版式修订 | pf-revise | pf-revision-editor |
| P4 | Codex 多轮模拟审稿（首轮+复审） | pf-review | pf-review-orchestrator |
| P5 | 两组互不知情的专业事实核查 | pf-review | pf-review-orchestrator + pf-fact-checker |
| P6 | 查新 + 反方审稿（挖掘） | pf-mine | pf-novelty-miner + pf-review-orchestrator |
| P7 | 体例合规 + 语言自然化终审 | pf-review | pf-review-orchestrator |
| P8 | 投稿包 | pf-package | pf-packager |

## 工作目录约定（每篇稿件一个目录）

```
<稿件目录>/
  原稿_xxx.docx            作者原稿（只读，永不覆盖）
  eval_report.tex/.pdf     P0
  venue_table.md           P1
  refs_check.md            P2
  evidence/                原始证据（开放全文 txt、扫描图、目录页等）
  paper/                   从 templates/manuscript 复制：content.py journal_style.py build_docx.py figures/ build/
  reviews/                 PROMPT_*.md  CODEX_*.md  EXPERT_*.md  SUMMARY.md
  投稿包_<期刊>/            P8 输出（及同名 .zip）
```

## 汇报给用户时
- 每个阶段结束都说清：做了什么、核实了什么、发现了什么、哪些必须作者本人完成。
- 录用可能性只给主观区间并注明来源；不同审稿组尺度不同，如实给出差异。
- 不提供代写、代投、包发表或报价（见 INTEGRITY.md）。
