---
name: diff-review
description: |
  Use when reviewing staged git changes before committing. Triggers on /diff-review.
  Handles both code review and writing (blog/article) proofreading with deep,
  context-aware analysis.
allowed-tools:
  - Bash
  - Read
  - Glob
  - Grep
---

# Diff-Review: Deep Staged Changes Review

审查暂存区的 git 变更，根据内容类型（代码/写作）自适应审查策略。核心原则：**不只看 diff，要理解上下文和意图。**

## Language Rules

- **审查输出默认使用中文**，除非用户明确使用英文发起调用。Summary、findings、suggestions 全部用中文，即使代码注释或文件名是英文。
- 如果用户用英文调用（如 "review my changes"），则全程用英文输出。

---

## Process

### Step 1: Gather Context

```bash
git diff --cached
```

If no staged changes → tell user to `git add` first, then stop.

If staged changes exist, also gather:

```bash
git diff --cached --stat        # overview of files changed
git log --oneline -5            # recent commit context
```

**Read full files** for any file with non-trivial changes (> 5 lines modified). Do NOT review a diff in isolation — you need to understand the surrounding code/content to assess whether an issue is real.

### Step 2: Detect Review Mode

| Condition | Mode |
|-----------|------|
| All changed files are `.md`, `.mdx`, `.txt`, `.rst`, `.adoc`, `.tex`, `.org` | **Writing Mode** |
| All changed files are code | **Code Mode** |
| Both types present | **Mixed Mode** — review each file with its matching criteria, group output by type (code files first, then writing files) |

### Step 3: Understand Intent

Before reviewing, determine **why** this change was made:
- Read the commit message if present (`git log --oneline -1` for amend scenarios)
- Look at the change pattern — is this a bugfix, new feature, refactor, or migration?
- This understanding shapes whether findings are actual issues or intentional trade-offs

---

## Code Mode: Review Criteria

Review in order of severity. For each finding, check the full file context to avoid false positives.

### CRITICAL (阻塞合并)
1. **Security** — injection (SQL/XSS/command), hardcoded secrets, auth bypass, mass assignment, sensitive data leaks in responses
2. **Data Loss / Corruption** — unsafe writes, missing transactions, race conditions on shared state

### HIGH (强烈建议修复)
3. **Logic Errors** — off-by-one, incorrect conditionals, null/undefined access, unhandled promise rejections
4. **Missing Validation** — trusting user input at system boundaries without sanitization

### MEDIUM (建议改进)
5. **Performance** — N+1 queries, unnecessary allocations, missing indexes for common queries
6. **Error Handling** — missing try/catch at I/O boundaries, generic error swallowing, stack traces leaking to client
7. **Architecture** — tight coupling, misplaced responsibilities, violating existing project patterns

### LOW (可选)
8. **Naming & Readability** — only flag genuinely confusing names, not style preferences
9. **Best Practices** — idiomatic patterns for the language, but only when deviation causes concrete harm

**Anti-patterns in code review:**
- Don't flag issues already handled by middleware/framework (check first!)
- Don't suggest fixes without verifying they match the project's ORM/library
- Don't nitpick formatting — that's linter territory
- Don't speculate — if unsure whether something is a bug, read the surrounding code

---

## Writing Mode: Review Criteria

Review as a substantive editor, not just a proofreader.

### Content Level (内容层面) — most important
1. **论证质量 / Argument Quality** — claims without evidence, logical fallacies, one-sided arguments, unfulfilled promises (title says X but content doesn't deliver)
2. **受众匹配 / Audience Fit** — is the depth appropriate for the target reader? Inconsistent register (switching between casual and formal)?
3. **结构 / Structure** — does the piece flow? Are sections parallel? Are transitions smooth?

### Language Level (语言层面)
4. **语法与用词 / Grammar & Word Choice** — 的/得/地 errors, redundant phrases, imprecise terminology, word misuse (e.g., "开发" vs "开发者")
5. **流畅度 / Fluency** — awkward sentences, unnecessary filler, overly long sentences that lose the reader

### Surface Level (表面层面) — least important
6. **排版 / Formatting** — heading hierarchy, inline code formatting for technical terms, spacing
7. **错别字 / Typos** — spelling errors, punctuation mistakes

**For every language/surface issue:** provide the original text AND a suggested rewrite.

**Anti-patterns in writing review:**
- Don't just check mechanics and call it a review — content quality matters more
- Don't impose your style preferences — flag issues only when they harm clarity or credibility
- Don't praise generic things ("good opening") — be specific about what works and why

---

## Output Format

```markdown
## Review Summary
Mode: [Code / Writing / Mixed]
Files: N files changed
Intent: [Brief description of what this change does]

---

## [filename]

### 🔴 CRITICAL / HIGH
- **[Category]**: [Specific issue with line reference]
  - Context: [Why this is a problem in this specific codebase]
  - Fix: [Concrete suggestion matching project patterns]

### 🟡 MEDIUM / LOW
- **[Category]**: [Issue description]
  - Fix: [Suggestion]

### 🟢 Good (mandatory — always include at least one)
- [Specific thing done well and why it matters — helps author know what to preserve]

---

## Overall Assessment
[1-3 sentences: Can this be merged/published as-is? What must be fixed first? What's the overall quality level?]
```

---

## Key Rules

- **ALWAYS read full files for context** — never review a diff in isolation
- **DO NOT** run `git add`, `git commit`, or `git push`
- **DO NOT** modify any source files
- **Verify before flagging** — if you suspect an issue, check the full file to confirm it's real
- **Match severity to impact** — a typo in a variable name is not the same severity as SQL injection
- **Be actionable** — every finding must include a concrete fix suggestion that works with the project's actual patterns
- **Respect intent** — if a change is clearly a quick prototype/WIP, adjust tone accordingly
