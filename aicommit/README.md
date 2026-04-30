# aicommit

从暂存的 git 变更自动生成符合 [Conventional Commits 1.0.0](https://www.conventionalcommits.org/) 规范的提交信息。

## 功能

- 读取 `git diff --cached`，分析变更内容
- 自动推断 type（feat、fix、docs 等）和 scope
- 生成 3 条风格不同的 commit message 供选择
- 支持中文 / English 提交信息
- 选定后自动执行 `git commit`

## 使用方式

```
/aicommit
```

**前提：** 需要先 `git add` 暂存变更。本 skill 不会执行 `git add` 或 `git push`。

## 工作流程

1. 询问语言偏好（中文 / English）
2. 读取暂存区 diff
3. 分析变更，生成 3 条候选 commit message
4. 用户选择一条（或要求重新生成 / 自定义指令）
5. 执行 commit 并报告结果

## 文件结构

```
aicommit/
├── SKILL.md                 # Skill 定义（prompt + 配置）
├── conventionalcommits.md   # Conventional Commits 规范参考
└── README.md                # 本文件（不会被模型读取）
```

---

## English

Generate [Conventional Commits 1.0.0](https://www.conventionalcommits.org/) compliant commit messages from staged git changes.

### Features

- Reads `git diff --cached` and analyzes changes
- Infers type (feat, fix, docs, etc.) and scope automatically
- Generates 3 commit message options with varying detail levels
- Supports Chinese / English messages
- Commits automatically after selection

### Usage

```
/aicommit
```

**Prerequisite:** Stage changes with `git add` first. This skill will not run `git add` or `git push`.

### Workflow

1. Ask language preference (Chinese / English)
2. Read staged diff
3. Analyze changes, generate 3 candidate messages
4. User selects one (or requests regeneration / custom instructions)
5. Execute commit and report result
