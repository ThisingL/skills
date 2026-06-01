# Adaptive Tutor — Skill Design Summary

## Overview

A personalized learning companion skill for Claude Code, focused on computer science and mathematics. Core differentiator: persistent learner profile enabling truly personalized teaching — connecting new knowledge to what the user already knows, adapting teaching style to user preferences, and emphasizing "how the inventor thought of it" rather than just "what the knowledge is".

---

## Positioning & Scope

- **Type**: Standalone new skill (not replacing or depending on `socratic-teaching-scaffolds`)
- **Domain**: Computer science + mathematics only (v1)
- **Target user**: The author themselves (personal use)
- **Granularity**: One concept per session (e.g., "Fourier Transform", "recursion", "gradient descent")
- **Trigger**: Manual invocation

---

## Naming & Commands

**Skill name**: `adaptive-tutor`

**Commands**:
| Command | Purpose |
|---------|---------|
| `/adaptive-tutor 傅里叶变换` | Learn a new concept |
| `/adaptive-tutor --init` | First-time initialization (assessment test) |
| `/adaptive-tutor --profile` | View/edit learner profile |

---

## File Structure

```
adaptive-tutor/
├── SKILL.md                          # Main prompt file (English)
├── resources/                        # Skill instruction files
│   ├── teaching-methodology.md       # Teaching style: principles + template + examples
│   ├── assessment-guide.md           # How to generate adaptive initial assessment
│   └── feynman-verification.md       # Verification question design & evaluation criteria
└── learner-data/                     # User-specific data (dynamically updated)
    ├── learner-profile.md            # Static profile: background, preferences, personality
    └── knowledge-map.md              # Knowledge points learned + mastery levels + progress
```

---

## Learner Profile System

### Content Dimensions

- **Academic background**: Degree, major, year, work experience
- **Knowledge base**: Core subjects studied, self-assessed level per area
- **Learning style preferences**: Likes self-discovery, enjoys history, prefers life-example analogies
- **Personality traits**: Patience level, abstract thinking ability, preference for rigor vs intuition

### Construction Method

1. **First-time (`--init`)**: 10-15 adaptive, dynamically generated diagnostic questions
   - Adaptive: correct → harder, wrong → easier (GRE-style)
   - Mixed format: multiple choice (fast) + 1-2 open-ended (depth)
   - Goal: Roughly position user across core dimensions (math foundation, programming experience, CS theory)
   - Not exhaustive — just enough to establish a baseline
2. **Per-session**: Each time user learns a new concept, the skill generates targeted prerequisite diagnostic questions for that specific knowledge chain
3. **Post-session**: Automatically append newly mastered concepts to `knowledge-map.md`
4. **Explicit editing**: User can modify via `--profile`

### Storage

- Located in `adaptive-tutor/learner-data/`
- `learner-profile.md`: Static info (background, preferences) — rarely changes
- `knowledge-map.md`: Dynamic record (concepts learned, mastery level, date, progress notes) — grows over time

---

## Core Teaching Flow

### Default Session Flow

```
1. 直觉开场 (Intuitive Opening)
   └── 漫士沉思录 style: interesting life example / phenomenon → curiosity → why do we need this?

2. 历史/思维背景 (History & Thought Process)
   └── Layer 1: Historical context (who, when, why, what failed before)
   └── Layer 2: Thought reconstruction ("if you faced this problem...")
   └── Layer 3: Guided re-invention (Socratic discovery — when appropriate)

3. 苏格拉底引导式发现 (Guided Discovery)
   └── Core teaching: Questions that lead user to derive the concept themselves

4. 深化理解 (Deepening)
   └── Edge cases, limitations, "why not another way?"

5. 费曼验证 (Feynman Verification)
   └── User explains back to AI; gradient-discriminating questions assess depth
```

### Flow Rules

- **Mandatory steps**: #3 (Guided Discovery) + #5 (Feynman Verification) — never skip
- **Optional steps**: #1, #2, #4 — adjusted based on profile preferences and knowledge point complexity
- **Knowledge association**: NOT a fixed step, but a tool used throughout — whenever user gets stuck and profile contains related knowledge that can help explain via analogy. Never forced.
- **Depth confirmation**: At session start, ask user "想了解到什么程度？（直觉理解 / 能用 / 能推导）"

---

## Teaching Style: "漫士沉思录" Opening

### Implementation in Prompt

Combine three approaches for stable quality:

1. **Principles**: Start from daily-life intuition, create curiosity, never open with dry definitions
2. **Structure template**: Describe phenomenon/scenario → Pose question → Reveal why this knowledge matters
3. **Good vs Bad examples** (2-3 contrasting pairs in methodology file)

**Good opening example**:
> "你听一首歌的时候，能同时分辨出贝斯、吉他、人声——你的耳朵怎么做到把混在一起的声波拆开的？"

**Bad opening example**:
> "傅里叶变换是一种将时域信号转换为频域表示的数学变换方法。"

---

## "How to Think of It" — Three Layers

| Layer | Name | When to use | Example |
|-------|------|-------------|---------|
| 1 | Historical reconstruction | Always attempt; skip if AI is uncertain | "Fourier was studying heat conduction, tried polynomial series first, failed, then..." |
| 2 | Thought path reconstruction | When history unavailable or as complement | "假设你面对一个复杂周期信号，你会怎么想到用简单信号来拼凑它？" |
| 3 | Guided re-invention | When concept is suitable for discovery | Lead user through questions to "invent" the core idea themselves |

**When AI doesn't know the history**: Use Layer 2 (thought reconstruction) as substitute. Never fabricate historical claims. If truly unsure, honestly state it.

---

## Feynman Verification Design

### Trigger
- Default: automatically enters after teaching phase
- User can skip by saying so

### Question Design
- **Gradient discriminating**: Questions should differentiate depth levels, not just pass/fail
  - Basic concept correct → ~60% mastery
  - Can explain boundary conditions → ~80%
  - Can answer "why not another approach" → ~95%
- Questions should be genuinely challenging — even full understanding requires effort to articulate perfectly

### Feedback Style
- First acknowledge what user explained correctly
- Then use follow-up questions to expose gaps/misconceptions (not direct correction)
- If gaps found: return to mini guided-discovery for that specific weak point

### Recording
- After verification, record in `knowledge-map.md`:
  - Concept name
  - Mastery level (fully mastered / partially mastered / needs revisit)
  - Date learned
  - Depth reached (intuition / application / derivation)
  - Notes on weak points if any

---

## Session Management

### Length Control
- AI proactively segments based on concept complexity
- One session focuses on one core understanding layer
- After each segment: "要继续深入还是今天到这？"

### Mid-session Exit
- If user leaves or says "够了", record progress in `knowledge-map.md`
- Note: "傅里叶变换：completed intuitive understanding, mathematical derivation not yet covered"
- Next session can pick up from where left off

### Depth Control
- At session start, briefly ask target depth
- Options framed as: 直觉理解 / 能实际运用 / 能数学推导

---

## Language

- **Skill files** (SKILL.md, resources/): Written in English
- **Teaching interaction**: Chinese by default
- **Technical terms**: Preserve English originals, don't force-translate (e.g., "Fourier Transform" alongside "傅里叶变换")
- **Configurable**: Profile can specify language preference

---

## Knowledge Association (Cross-Concept Linking)

- Used as a **tool throughout the session**, not a fixed step
- Triggered when: user is stuck on something, and profile's `knowledge-map.md` contains a related concept that could serve as analogy
- Must be genuinely helpful — never force a connection just because one exists
- Example: User learning "gradient descent", already knows "binary search" → "你学过二分查找对吧？梯度下降有点像——都是在缩小搜索范围，只不过..."

---

## V1 Scope (What's NOT included)

- ❌ Review/spaced-repetition mode (`--review`)
- ❌ Active push notifications for review reminders
- ❌ Cross-concept recommendation ("you learned A, B, C — try D")
- ❌ Knowledge graph visualization
- ❌ Multi-domain support (only CS + math)
- ❌ Pre-built question banks (all dynamically generated)

---

## Design Philosophy

> "很多教授能跟你讲清楚，但不能告诉你'怎么才能想到这一点'"

This skill's core mission is to **accelerate the process of developing intuition** — not just transferring knowledge, but helping the learner experience a compressed version of the discovery journey. Teaching the "how to think of it" alongside "what it is".
