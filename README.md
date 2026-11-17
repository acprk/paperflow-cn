# paperflow-cn

**中文学术期刊稿件的“评估—核实—修订—模拟审稿—投稿包”agent 工作流**，用于 [Claude Code](https://claude.com/claude-code)，审稿环节调用 [Codex CLI](https://github.com/openai/codex)（只读沙箱）。

它把一篇稿件从“能不能发”带到“可以由作者本人投出去”，每一步都要求可核查的证据：

```
P0 发稿评估 → P1 期刊核实 → P2 文献核实 → P3 修订(单一内容源→Word)
   → P4 多轮模拟审稿 → P5 独立事实核查 → P6 查新与挖掘 → P7 终审 → P8 投稿包
```

## 特点

- **单一内容源**：正文、摘要、表格、参考文献只写在 `content.py`，按期刊版式（`journal_style.py`）一键生成 Word；引文按首次出现自动编号；`check_consistency.py` 逐段核对 Word 与内容源。
- **证据优先**：期刊收录要有近一年具体篇目页面为证；参考文献逐条核实，区分“题录核实”与“实引核实”；页码、版本、作者信息不编造，一律留【待填】。
- **多组互不知情的审稿**：Codex 审稿组 + 独立事实核查子代理交叉核对；“挖掘式”审稿包含查新与反方审稿人。
- **诚信红线写进流程**：不报价、不代投、不包发表、不编造材料；投稿由作者本人完成（见 [INTEGRITY.md](INTEGRITY.md)）。

## 目录

```
.claude/agents/     8 个 agent：评估、期刊核实、文献核实、修订、审稿编排、事实核查、查新挖掘、封装
.claude/skills/     总纲 paperflow + 7 个阶段 skill
prompts/            Codex 审稿提示词模板（首轮、复审、事实核查、确认、挖掘、挖掘复核、终审）
templates/          稿件模板（content.py / journal_style.py / build_docx.py）、评估说明、期刊核实表、
                    文献核查表、投稿邮件、检查清单、作者信息表
tools/              run_codex.sh、inline_prompt.py、check_consistency.py、make_package.py、
                    cnki_title_check.py、privacy_scan.py
examples/demo/      占位示例稿件（用于自检）
WORKFLOW.md         阶段、输入输出与闸门
INTEGRITY.md        学术诚信红线
LESSONS.md          实践中踩过的坑
```

## 安装

```bash
# 1. 依赖
pip install -r requirements.txt          # python-docx、Pillow
# 系统工具：pandoc、LibreOffice（soffice）、xelatex（ctex 宏包，评估说明 PDF 用）、Codex CLI（审稿用）

# 2. 放进你的项目（或 ~/.claude 下供所有项目使用）
cp -r .claude/agents/*  <你的项目>/.claude/agents/
cp -r .claude/skills/*  <你的项目>/.claude/skills/
```

## 快速自检

```bash
python tools/make_package.py --src examples/demo --name 示例作者-示例题目 --out build/demo_submission
# 期望输出：一致性核对通过，并生成 build/demo_submission.zip
```

## 在 Claude Code 中使用

- “评估这篇稿件能不能发省级期刊” → `paperflow` / `pf-evaluate`
- “帮我核实哪些期刊被知网收录” → `pf-venue`
- “按审稿意见改稿并重新生成 Word” → `pf-revise`
- “用 Codex 组织模拟审稿 / 挖掘问题” → `pf-review` / `pf-mine`
- “做投稿包” → `pf-package`

## 许可

MIT，见 [LICENSE](LICENSE)。
