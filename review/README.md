# review

审查 git 暂存区的变更，根据文件类型自动切换审查模式（代码审查 / 写作润色）。

## 功能

- 读取 `git diff --cached`，导出到临时文件后逐行审查
- 自动检测内容类型：代码文件走 code review，文章文件走写作审查
- 混合变更时按文件类型分别审查
- 按文件分组输出问题、建议和亮点
- 写作模式提供具体的改写建议（原文 → 改进）
- 审查完成后自动清理临时文件

## 使用方式

```
/review
```

**前提：** 需要先 `git add` 暂存变更。本 skill 不会执行 `git add`、`git commit` 或 `git push`。

## 审查维度

### 代码模式

- Bug / 逻辑错误
- 安全隐患
- 性能问题
- 命名与可读性
- 最佳实践

### 写作模式

- 行文流畅度
- 逻辑连贯性
- 错别字 / 语法
- 排版格式
- 用词准确性
- 可读性改善建议

## 输出格式

按文件分组，每个文件包含：
- 🔴 必须修复的问题
- 🟡 建议改进
- 🟢 亮点

最后给出整体总结。

## 文件结构

```
review/
├── SKILL.md    # Skill 定义（prompt + 配置）
└── README.md   # 本文件（不会被模型读取）
```

---

## English

Review staged git changes with automatic content type detection (code review vs writing/proofreading).

### Features

- Reads `git diff --cached`, exports to a temp file, and reviews line by line
- Auto-detects content type: code files get code review, article files get writing review
- Mixed changes are reviewed per-file with matching criteria
- Groups output by file with issues, suggestions, and highlights
- Writing mode provides concrete rewrite suggestions (before → after)
- Auto-cleans temp file after review

### Usage

```
/review
```

**Prerequisite:** Stage changes with `git add` first. This skill will not run `git add`, `git commit`, or `git push`.

### Review Criteria

**Code Mode:** bugs, security, performance, naming/readability, best practices

**Writing Mode:** fluency, coherence, typos/grammar, formatting, word choice, readability

### Output Format

Grouped by file, each containing:
- 🔴 Must fix
- 🟡 Could improve
- 🟢 Highlights

Followed by an overall summary.
