# Skills

Claude Code 自定义 Skills。

## 可用 Skills

| Skill | 说明 |
|-------|------|
| [ai-commit](./ai-commit/) | 从暂存的 git 变更自动生成 Conventional Commits 规范的提交信息 |
| [diff-review](./diff-review/) | 深度审查暂存区变更，读取完整文件上下文，自适应代码/写作模式 |
| [code-flow](./code-flow/) | 结构化开发工作流：Research → Plan（含 Grill 追问）→ Annotate → Todo → Implement → Feedback |
| [grill-me](./grill-me/) | 针对计划或设计方案进行逐一追问，直到达成共识 |
| [find-skills](./find-skills/) | 帮助发现和安装 agent skills，当用户寻找可扩展功能时触发 |
| [writing-skills](./writing-skills/) | 创建、编辑、验证 skills 的元技能，遵循 TDD 流程 |
| [nano-codebase](./nano-codebase/) | 将陌生代码库"蒸馏"为精简可运行的 nano 版本 + 路径追踪式学习指南，渐进式理解项目 |
| [nuwa-skill](./nuwa-skill/) | 输入人名或模糊需求，自动深度调研并提炼思维框架，生成可运行的人物 Skill |
| [socratic-teaching-scaffolds](./socratic-teaching-scaffolds/) | 苏格拉底式教学：通过引导提问和渐退支架帮助学习者自主发现知识 |

## 使用方式

在 Claude Code 中通过斜杠命令调用：

```
/ai-commit
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
| [ai-commit](./ai-commit/) | Generate conventional commit messages from staged git changes |
| [diff-review](./diff-review/) | Deep staged changes review with full-file context, code and writing modes |
| [code-flow](./code-flow/) | Structured dev workflow: Research → Plan (with Grill) → Annotate → Todo → Implement → Feedback |
| [grill-me](./grill-me/) | Interview relentlessly about a plan or design until reaching shared understanding |
| [find-skills](./find-skills/) | Discover and install agent skills when looking for extensible functionality |
| [writing-skills](./writing-skills/) | Meta-skill for creating, editing, and verifying skills using TDD approach |
| [nano-codebase](./nano-codebase/) | Distill an unfamiliar codebase into a runnable nano version + path-tracing learning guide for progressive understanding |
| [nuwa-skill](./nuwa-skill/) | Input a person's name or vague need, auto-research and distill thinking frameworks into a runnable persona Skill |
| [socratic-teaching-scaffolds](./socratic-teaching-scaffolds/) | Socratic teaching: guide learners to discover knowledge through strategic questioning and progressive scaffolding |

### Usage

Invoke a skill via slash command in Claude Code:

```
/ai-commit
```

### Adding a New Skill

1. Create a directory named after the skill (e.g., `my-skill/`)
2. Add a `SKILL.md` with frontmatter (`name`, `version`, `description`, `allowed-tools`) and the full prompt
3. Place any reference files in the same directory
4. Update this README
