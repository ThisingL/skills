<div align="center">

<h1>Agent Skills</h1>

<p>把开发、学习与日常工作的经验，整理成可复用的 Agent 技能。</p>

<p><sub>21 SKILLS &nbsp; / &nbsp; 3 COLLECTIONS</sub></p>

<p>
  <a href="#catalog">技能目录</a> &nbsp;·&nbsp;
  <a href="#usage">使用方式</a> &nbsp;·&nbsp;
  <a href="#contributing">添加技能</a>
</p>

</div>

---

<a id="catalog"></a>

## 技能目录

按工作场景组织的个人技能库。点击 skill 名称查看入口文件，了解触发条件、工作流程与工具要求。

| 分类 | 用途 | 数量 |
|:-----|:-----|-----:|
| [coding/](#coding) | 开发工作流、代码审查与前端设计 | 5 |
| [learning/](#learning) | 代码库理解、个性化学习与引导教学 | 3 |
| [tools/](#tools) | 思维追问、文档处理、工程方法与技能管理 | 13 |

<a id="coding"></a>

### Coding · 开发

| Skill | 说明 |
|:------|:-----|
| [ai-commit](./coding/ai-commit/SKILL.md) | 从暂存的 git 变更自动生成符合 Conventional Commits 规范的提交信息 |
| [code-flow](./coding/code-flow/SKILL.md) |【企业内部需求开发】结构化开发工作流：Research → Plan（含 Grill 追问）→ Annotate → Todo → Implement →Feedback  |
| [diff-review](./coding/diff-review/SKILL.md) | 深度审查暂存区变更，读取完整文件上下文，自适应代码/写作模式 |
| [frontend-design](./coding/frontend-design/SKILL.md) | 前端设计模式与最佳实践，摆脱千篇一律的 AI 前端 UI |
| [karpathy-guidelines](./coding/karpathy-guidelines/SKILL.md) |【开发一个完整项目】 Karpathy 风格 coding 指南，适合开发完整项目时使用 |

<a id="learning"></a>

### Learning · 学习

| Skill | 说明 |
|:------|:-----|
| [nano-codebase](./learning/nano-codebase/SKILL.md) | 【nano-xxx】将陌生代码库蒸馏为 nano 版本 + 路径追踪式学习指南 |
| [personalizing-learning-content](./learning/personalizing-learning-content/SKILL.md) | 根据用户提供的知识库改写文本、Markdown 或 PDF 学习材料，输出正文与知识差异说明 |
| [socratic-teaching-scaffolds](./learning/socratic-teaching-scaffolds/SKILL.md) | 【自学】苏格拉底式教学：引导提问与渐退支架，帮助学习者自主发现知识 |

<a id="tools"></a>

### Tools · 通用工具

#### 思维追问与决策

| Skill | 说明 |
|:------|:-----|
| [grilling](./tools/grilling/SKILL.md) | 核心追问流程：围绕计划、决策或想法，按决策依赖逐轮检验假设、澄清分歧 |
| [grill-me](./tools/grill-me/SKILL.md) | 【AI 拷打你】针对计划或设计方案逐一追问，直到达成共识 |
| [grill-with-docs](./tools/grill-with-docs/SKILL.md) | 组合 `grilling` 与 `domain-modeling`，在追问过程中同步记录领域术语与架构决策 |

#### 文档、知识管理与论文

| Skill | 说明 |
|:------|:-----|
| [defuddle](./tools/defuddle/SKILL.md) | 使用 Defuddle CLI 将网页提取为干净的 Markdown，去除导航和页面杂项 |
| [domain-modeling](./tools/domain-modeling/SKILL.md) | 梳理项目领域模型与统一术语，维护 `CONTEXT.md` 和架构决策记录（ADR） |
| [obsidian-markdown](./tools/obsidian-markdown/SKILL.md) | 创建和编辑 Obsidian Markdown，支持双链、嵌入、callout、属性与标签 |
| [thesis-polish](./tools/thesis-polish/SKILL.md) | 【中文毕业论文】理工科论文写作与审校双模式，基于范例论文风格指纹，去除 AI 痕迹 |
| [ustc-se-thesis](./tools/ustc-se-thesis/SKILL.md) | 中国科学技术大学软件学院专硕论文指南，覆盖章节组织、排版、UML 建模与规范自查 |

#### 工程执行方法

| Skill | 说明 |
|:------|:-----|
| [subagent-driven-development](./tools/subagent-driven-development/SKILL.md) | 在当前会话中按计划分派独立任务给子代理，并审查实现结果 |
| [test-driven-development](./tools/test-driven-development/SKILL.md) | 实现功能或修复缺陷时遵循先写失败测试、再实现、再重构的 TDD 流程 |

#### 技能发现与创建

| Skill | 说明 |
|:------|:-----|
| [find-skills](./tools/find-skills/SKILL.md) | 发现和安装 agent skills，寻找可扩展功能时触发 |
| [nuwa-skill](./tools/nuwa-skill/SKILL.md) | 【女娲】输入人名或模糊需求，自动深度调研并提炼思维框架，生成可运行的人物 Skill  |
| [writing-skills](./tools/writing-skills/SKILL.md) | 创建、编辑、验证 skills 的元技能，遵循 TDD 流程 |


---

<a id="usage"></a>

## 使用方式

选择所需 skill，按所用 Agent 的方式加载完整目录。参考资料、脚本和配置应与入口文件一起保留。

以下是 Claude Code 加载 skill 后的调用示例：

```text
# 自动生成规范的 commit message
/ai-commit

# 深度审查暂存区代码
/diff-review

# 启动结构化开发工作流
/code-flow
```

---

<a id="contributing"></a>

## 添加技能

先按用途选择 `coding/`、`learning/` 或 `tools/`，再在分类目录下添加 skill：

```text
<category>/my-skill/
├── SKILL.md          # 入口文件：frontmatter + 指令正文
├── README.md         # （可选）使用说明
├── references/       # （可选）参考资料，也可放在 skill 目录下
├── scripts/          # （可选）辅助脚本
└── agents/           # （可选）代理配置
```

1. 在对应分类下创建以 skill 名称命名的目录。
2. 添加 `SKILL.md`，frontmatter 至少包含 `name` 和 `description`；按需补充 `version`、`allowed-tools` 等字段，并编写完整指令。
3. 将参考资料、脚本等配套文件放在该 skill 目录内，使用相对路径引用。
4. 更新本 README 对应分类的清单、分类数量和顶部技能总数，并检查链接。
