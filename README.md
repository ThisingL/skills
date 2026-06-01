<div align="center">

# 🛠️ Claude Code Skills

[![Claude Code](https://img.shields.io/badge/Claude_Code-Skills-blueviolet?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9IndoaXRlIiBzdHJva2Utd2lkdGg9IjIiPjxwYXRoIGQ9Ik0xMiAyTDIgN2wxMCA1IDEwLTV6Ii8+PHBhdGggZD0iTTIgMTdsMTAgNSAxMC01Ii8+PHBhdGggZD0iTTIgMTJsMTAgNSAxMC01Ii8+PC9zdmc+)](https://github.com/ThisingL/skills)
[![License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)](./LICENSE)
[![Skills](https://img.shields.io/badge/skills-11-orange?style=for-the-badge)](#-可用-skills)

**一套可复用的 Claude Code 自定义 Skills，覆盖开发工作流、代码审查、学习辅导等场景。**

[快速开始](#-快速开始) · [Skills 列表](#-可用-skills) · [贡献指南](#-添加新-skill)

</div>

---

## ✨ 特性

- 🔄 **开发工作流** — 从 commit 到 code review，全链路覆盖
- 🧠 **思维增强** — 苏格拉底式追问、Karpathy 编程哲学、需求澄清
- 📚 **学习加速** — 陌生代码库速览、概念自适应教学
- 🧬 **技能生成** — 输入人名即可蒸馏其思维框架为可运行 Skill

---

## 🚀 快速开始

在 Claude Code 中直接通过斜杠命令调用：

```bash
# 自动生成规范的 commit message
/ai-commit

# 深度审查暂存区代码
/diff-review

# 启动结构化开发工作流
/code-flow
```

---

## 📦 可用 Skills

### 🔧 开发工具

| Skill | 说明 |
|:------|:-----|
| [ai-commit](./ai-commit/) | 从暂存的 git 变更自动生成符合 Conventional Commits 规范的提交信息 |
| [diff-review](./diff-review/) | 深度审查暂存区变更，读取完整文件上下文，自适应代码/写作模式 |
| [code-flow](./code-flow/) |【企业内部需求开发】结构化开发工作流：Research → Plan（含 Grill 追问）→ Annotate → Todo → Implement →Feedback  |
| [karpathy-guidelines](./karpathy-guidelines/) |【开发一个完整项目】 Karpathy 风格 coding 指南，适合开发完整项目时使用 |
| [frontend-design](./frontend-design/) | 前端设计模式与最佳实践，摆脱千篇一律的 AI 前端 UI |

### 💡 思维与决策

| Skill | 说明 |
|:------|:-----|
| [grill-me](./grill-me/) | 【AI 拷打你】针对计划或设计方案逐一追问，直到达成共识并生成总结文档 |
| [nuwa-skill](./nuwa-skill/) | 【女娲】输入人名或模糊需求，自动深度调研并提炼思维框架，生成可运行的人物 Skill  |

### 📖 学习与教学

| Skill | 说明 |
|:------|:-----|
| [nano-codebase](./nano-codebase/) | 【nano-xxx】将陌生代码库蒸馏为 nano 版本 + 路径追踪式学习指南 |
| [socratic-teaching-scaffolds](./socratic-teaching-scaffolds/) | 【自学】苏格拉底式教学：引导提问与渐退支架，帮助学习者自主发现知识 |

### 🏗️ 元技能

| Skill | 说明 |
|:------|:-----|
| [writing-skills](./writing-skills/) | 创建、编辑、验证 skills 的元技能，遵循 TDD 流程 |
| [find-skills](./find-skills/) | 发现和安装 agent skills，寻找可扩展功能时触发 |

---

## 📝 添加新 Skill

```
my-skill/
├── SKILL.md          # 主文件：frontmatter + prompt
├── README.md         # (可选) skill 说明文档
└── *.md              # (可选) 参考资料
```

1. 创建以 skill 名称命名的目录
2. 添加 `SKILL.md`，包含 frontmatter（`name`、`version`、`description`、`allowed-tools`）和完整 prompt
3. 将 skill 需要的参考文件放在同一目录下
4. 更新本 README 的 Skills 列表

---

## 📄 License

[MIT](./LICENSE)

