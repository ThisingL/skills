# Skills

Claude Code 自定义 Skills。

## 可用 Skills

| Skill | 说明 |
|-------|------|
| [aicommit](./aicommit/) | 从暂存的 git 变更自动生成 Conventional Commits 规范的提交信息 |
| [review](./review/) | 审查暂存区变更，自动检测代码/写作模式，分别给出审查意见 |
| [code-flow](./code-flow/) | 结构化开发工作流：Research → Plan → Annotate → Todo → Implement → Feedback |

## 使用方式

在 Claude Code 中通过斜杠命令调用：

```
/aicommit
```

## 添加新 Skill

1. 创建以 skill 名称命名的目录（如 `my-skill/`）
2. 在目录中添加 `SKILL.md`，包含 frontmatter（`name`、`version`、`description`、`allowed-tools`）和完整 prompt
3. 将 skill 需要的参考文件放在同一目录下
4. 更新本 README 的列表

---

## English

Custom skills for Claude Code.

### Available Skills

| Skill | Description |
|-------|-------------|
| [aicommit](./aicommit/) | Generate conventional commit messages from staged git changes |
| [review](./review/) | Review staged changes with auto-detection of code vs writing mode |
| [code-flow](./code-flow/) | Structured dev workflow: Research → Plan → Annotate → Todo → Implement → Feedback |

### Usage

Invoke a skill via slash command in Claude Code:

```
/aicommit
```

### Adding a New Skill

1. Create a directory named after the skill (e.g., `my-skill/`)
2. Add a `SKILL.md` with frontmatter (`name`, `version`, `description`, `allowed-tools`) and the full prompt
3. Place any reference files in the same directory
4. Update this README
