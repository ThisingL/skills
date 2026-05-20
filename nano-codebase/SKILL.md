---
name: nano-codebase
description: Use when user wants to learn or understand a new codebase, project, or module they have no context about. Triggers on "help me learn this codebase", "I'm new to this project", "nano-codebase", or when user expresses feeling overwhelmed by unfamiliar code.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Agent
  - AskUserQuestion
---

# Nano-Codebase: Understand a Codebase by Distilling It

Core idea: **Generate a runnable nano version of the project + a creator-perspective guided learning document**, enabling the user to progressively understand the codebase instead of being overwhelmed by massive code.

**The deliverable is not a document — it is a sustainable learning system.**

---

## Language Rules

- **GUIDE.md / conversation / AI-added learning annotations**: Always match the user's language. If the user writes in Chinese, all output must be in Chinese. If English, use English.
- **nano-xxx code itself**: Keep consistent with the original project's language.

---

## Phase 1: Deep Research

### Goal

Deeply read the entire codebase and produce a comprehensive research document (`research.md`). This is the most critical phase — the quality of research.md directly determines the quality of nano-xxx and GUIDE.md.

**The AI must fully understand the entire project before it has any right to judge what is "core" vs "auxiliary".** Do not guess based on file names or directory structure — you must read and understand the implementation before drawing conclusions.

**Shallow reading is unacceptable.** Do not stop at function signatures — read implementations line by line, trace data flows end-to-end, understand every relationship between components.

### Process

1. **Check for existing research.md**: If `research.md` already exists in the project root, read it and assess:
   - Still accurate and comprehensive → Build upon it, update with new findings
   - Outdated or incomplete → Replace with fresh research

2. **Deep read**: Thoroughly explore the code. Do not skim. Do not stop at function signatures — read implementations line by line, trace data flows end-to-end, understand every relationship between components. Investigate:
   - How the system currently works in full detail
   - Existing patterns, conventions, and abstractions in use
   - Dependencies and coupling with other parts of the system
   - Edge cases, error handling, and existing tests
   - Any caching, queuing, or optimization layers
   - Potential bugs or inconsistencies

   Use "thorough", "detailed", "complexity" as your internal bar — if you haven't reached that depth, keep reading.

3. **Timeline archaeology** (best-effort):
   - Check if git history has value (are early commits progressive/incremental?)
   - Valuable → Analyze evolution, record key turning points
   - Not valuable (squash merge / first commit is already complete / shallow clone) → Skip

4. **Assess scale**:
   - Small project (< 5k lines): Prepare to suggest skipping nano generation
   - Medium project (5k - 50k lines): Standard flow
   - Large project / monorepo (> 50k lines): Prepare to ask user to select core modules to focus on

5. **Write research.md**: Save a detailed report to `research.md` in the project root. The document must cover:
   - System overview and architecture
   - Key files and their responsibilities
   - Data flow and control flow (end-to-end)
   - Existing patterns and conventions
   - Discovered constraints, gotchas, and edge cases
   - Any bugs or inconsistencies found
   - Design decisions and their reasoning (why A over B)
   - Clear distinction between core path vs auxiliary code

   **This document is the user's review interface** — they will read it to verify you truly understand the system. If research is wrong, the nano generation will be wrong.

### research.md Content Structure

The document should be **comprehensive and detailed** — there is no length limit. More detail means better AI context recovery and better nano generation. Think of it as a complete project knowledge base that allows someone (or an AI) to fully understand the system without reading all the source code.

Structure inspired by arc42, adapted for our purpose:

```markdown
# {Project Name} — Deep Research

## 1. Introduction and Goals

### What This Project Is
[What problem it solves, who uses it, why it exists — the "elevator pitch"]

### Core Quality Goals
[What the system optimizes for — performance? reliability? extensibility? What trade-offs were made?]

### Key Stakeholders
[Who cares about this system — users, operators, dependent services, etc.]

## 2. Context and Scope

### System Boundary
[What is inside this project vs what is external. Draw a clear line.]

### External Interfaces
[Other systems this project talks to — upstream callers, downstream dependencies, databases, message queues, external APIs, etc. For each: what protocol, what data is exchanged, which direction]

### Runtime Environment
[Where and how this runs — container? bare metal? JVM version? OS assumptions? Resource requirements?]

## 3. Solution Strategy

### Fundamental Technical Decisions
[The 3-5 biggest "why did they do it this way" decisions. e.g., "Java over Go because...", "LevelDB over SQLite because...", "sidecar pattern because..."]

### Top-Level Decomposition
[How the system is broken into major parts and why that particular decomposition]

## 4. Building Block View

### Level 1: Top-Level Modules
[The major modules/packages and their responsibilities. Include a diagram or structured description of how they relate]

### Level 2: Key Internal Structures
[For each core module, its internal structure — main classes, their relationships, inheritance/composition hierarchies]

### Key Files and Responsibilities
[Every important file — not a flat list, but organized by module, explaining what role each plays in the whole system. Include file paths.]

## 5. Runtime View

### Scenario A: {Most important runtime scenario}
[End-to-end trace: what happens when X occurs, step by step through the code. Which files, which methods, what data flows where]

### Scenario B: {Second important scenario}
[Same format]

### Scenario N: ...
[As many scenarios as needed to cover the important runtime behaviors]

### State Machines
[Any important state transitions in the system — document states, transitions, and triggers]

## 6. Crosscutting Concepts

### Patterns Used
[Design patterns employed across the codebase — Factory, Template Method, Observer, etc. Where each is used and why]

### Error Handling Strategy
[How errors are handled across the system — exceptions? error codes? retry policies? fallback strategies?]

### Concurrency Model
[Threads, locks, queues, async patterns — how the system handles concurrent operations]

### Configuration Strategy
[Where config comes from, how it's loaded, how different environments are handled]

### Coding Conventions
[Naming rules, package organization principles, code style patterns observed]

## 7. Architecture Decisions

### Decision 1: {Title}
- **Context**: What situation led to this decision
- **Decision**: What was chosen
- **Alternatives considered**: What was rejected and why
- **Consequences**: What this decision enables and constrains

### Decision 2: ...
[Document all significant architectural decisions]

## 8. Core Path vs Auxiliary Code

### Core Path (for nano)
[Explicitly list which code constitutes the essential logic — the minimum needed to understand what this system does]

### Auxiliary Code (strip for nano)
[What can be stripped: edge case handling, compatibility layers, performance optimizations, monitoring/logging, multi-variant support beyond 1-2 examples]

### The Boundary
[Why the line is drawn here — what principles determined "core" vs "auxiliary"]

## 9. Design Evolution (if git history is valuable)

### Timeline
[Key phases of the project's evolution — what was added when and why]

### Turning Points
[Moments where the architecture changed significantly — what triggered the change]

### Legacy / Historical Artifacts
[Code that exists for historical reasons but may be confusing to newcomers]

## 10. Risks, Gotchas, and Tricky Parts

### Easy to Misunderstand
[Parts of the code that look simple but have subtle complexity]

### Implicit Dependencies
[Hidden coupling, assumed initialization order, things that break if you change them in isolation]

### Known Issues / Technical Debt
[Things that are "wrong" but intentional, or known problems not yet fixed]
```

### Deep Read Standard

You've truly understood a module when you can answer:
- What **root problem** does this module solve?
- What is its **core algorithm/logic**? (Summarizable in 3-5 lines of pseudocode)
- Why was **this approach** chosen over alternatives? (Name at least 1 rejected alternative)
- What are the **implicit constraints or assumptions**?
- What **breaks** if you remove a specific piece of code?

### Phase Exit

Present a summary of research.md's key findings to the user, including:
- What the project core is
- Which modules you judge to be core and why (as many as the project warrants — no fixed number)
- If small project: suggest whether to skip nano generation (**must wait for user confirmation**)
- If large project: ask user to select which modules to focus on

Ask the user to review `research.md`. Confirm their understanding is correct, ask if anything was missed.

**DO NOT proceed to Phase 2 until the user confirms research.md is correct. NEVER suggest skipping this phase, regardless of how simple the project appears.**

---

## Phase 2: Generate nano-xxx

### Goal

Based on the deep research, create a distilled runnable project as the user's learning vehicle.

**Key: nano code must be a distillation of the original code, NOT a reimagination.** Preserve the original code's core logic structure — only strip edge cases and auxiliary code.

### nano-xxx Requirements

- **Location**: `nano-{project-name}/` in the project root directory
- **Runnability**: Try to be runnable. Parts that can't run due to complex dependencies should use mocks + clear annotations
- **Content**: Overall skeleton + distilled implementation of the core path
- **Skeleton placeholders**: Unexpanded modules use `// TODO: simplified, see original at <path>`

### Generation Process

1. **Determine core path**: Based on research, select the code path that best represents the project's essence
2. **Reference history** (if git history is valuable): Check if early versions are simpler, use as reference for nano implementation
3. **Distill (not rewrite)**:
   - Start from original code, remove edge cases, compatibility code, optimization tricks
   - **Keep core logic consistent with original** — variable names, method names, call relationships should be traceable
   - If original code is genuinely obscure in places, simplify expression, but keep core algorithm unchanged
   - Add learning annotations (in user's language) explaining key design decisions
4. **Generate GUIDE.md** (see GUIDE.md Specification below)
5. **Generate Mermaid diagrams**: Embed in GUIDE.md, generate as many as needed (architecture, data flow, module interaction, etc. — no limit on quantity)

### Distillation Principles

| Keep | Strip |
|------|-------|
| Core algorithms and data flows | Edge case handling |
| Key design pattern implementations | Excess overloads/polymorphic branches (keep only 1-2 representative implementations) |
| State management and transition logic | Monitoring, logging, metrics reporting |
| Critical concurrency mechanisms | Compatibility code, fallback logic |
| Inter-module interaction patterns | Config parsing (hardcode instead) |

### Phase Exit

Tell the user nano-xxx has been generated, guide them to start reading from GUIDE.md.

---

## GUIDE.md Specification

GUIDE.md is a learning document, NOT a traditional README. **It is a learning journey, not a reference manual.**

### Narrative Structure: Path Tracing

**The organizing unit of learning is NOT a module — it is a PATH (an end-to-end trace of a concrete question through the code).**

You don't start by "understanding the architecture." You start by asking a concrete question and tracing its answer through the code from entry to exit. After tracing a few paths, the architecture emerges naturally in your head.

GUIDE.md is structured as a series of **paths** — each path is a complete story with a start and an end:

```
Path 1: "When X happens, what does the code do from start to finish?"
  → Trace through files A → B → C → D

Path 2: "When Y happens, what does the code do?"
  → Trace through files B → E → F → C

💡 Intersection: Both paths go through B and C — these are the core modules
```

### Within Each Path

Each path uses the **"Question → Trace → Insight → Exercise"** structure:

1. **Pose the question** — A concrete runtime scenario: "A model update command arrives via HTTP. What happens next?"
2. **Trace the path** — Walk through the code step by step, file by file, following the execution flow. **Within the trace, apply creator-perspective narrative principles:**
   - Before introducing a concept, make the reader feel the pain of "what happens without it"
   - At design decision points, let the reader think first (Socratic), then reveal the answer
   - Build progressively — start with the simplest version of what happens, then layer on complexity
3. **Highlight insights** — Design decisions encountered along the path. Why this approach? What's the alternative?
4. **Hands-on exercise** — Modify something along this path and observe the effect. Exercises follow immediately, never bundled elsewhere.

### Socratic Style Within Paths

At design decision points along the trace, pause and engage the reader:

### Socratic Style Within Paths

At design decision points along the trace, pause and engage the reader:

```markdown
> 🤔 The model update needs to download files that could be several GB. The HTTP handler is waiting.
> What would you do?
>
> Pause and think...
>
> You might do it synchronously and increase the HTTP timeout.
> But what if the caller needs to fire-and-forget and check status later?
>
> The author chose async execution: accept the request, return 200 immediately,
> do the actual work in a background thread, report status via heartbeat.
```

**FORBIDDEN:**
```markdown
Q: Why is model update async?
A: Because downloads are slow.
```

### Document Structure Template

```markdown
# Building a {project-name} from Scratch

## Starting Point: What Problem Are We Solving?
[Creator-perspective opening: set up the real-world scenario, make the reader FEEL why
this project needs to exist. Pose the pain points. Then reveal what this project is
as the natural answer to those pain points.]

[Example tone:
"You have an AI inference engine. It can load models and serve predictions.
But you can't just 'run it raw.' Why?
- It crashes at 3am and you don't want to be woken up
- New models are trained and need to be swapped without downtime
- Different engines have different startup commands
This is why serving-agent exists: a process-level sidecar that manages the engine's
entire lifecycle."]

[End with a transition into the paths:
"Let's trace through the code to see how it actually works."]

## Path 1: {Concrete question — the most fundamental/common operation}
[e.g., "An inference request arrives — what happens from HTTP entry to response?"]
[Trace end-to-end through the code, Socratic Q&A at decision points, exercise at end]

## Path 2: {Another concrete question}
[e.g., "A model update command comes in — what happens?"]
[Trace end-to-end, use Socratic style, exercise at end]

## Path N: ...
[As many paths as the project needs — no fixed limit]

## The Big Picture
[NOW show Mermaid diagrams — reader already understands from tracing paths]
[Architecture overview + data flow + per-module interaction as needed]
[The diagrams should feel like "confirmation" of what they already know, not new information]

## Project Structure
[Annotated tree view of nano-xxx/]
```
nano-{project-name}/
├── src/
│   ├── engine/
│   │   ├── EngineRunner.java         # Process lifecycle + exponential backoff
│   │   ├── TFEngineRunner.java       # Template method impl for TF Serving
│   │   └── EngineRunnerFactory.java  # Factory: selects runner by engine type
│   ├── model/
│   │   └── ModelManager.java         # Model hot-update + heartbeat
│   └── ...
└── GUIDE.md
```

## Side Paths (files not covered in main paths)
[For any files in nano-xxx/ that weren't naturally visited by the main paths above]
[Give each a brief exploration — what it does, why it exists, when it gets called]
[Important files get a mini-trace; trivial files (beans, enums, constants) get 1-2 lines]

## From Nano to Real Code
[Comparison table: what nano omits vs what the original has]
```

### Path Selection Strategy

When deciding which paths to trace:
1. **First path**: The most fundamental operation — what this project exists to do (the "happy path")
2. **Subsequent paths**: Other important operations, error/recovery scenarios, etc.
3. **Number of paths depends on the project** — simple projects may need 2, complex ones may need 5+. The goal is: after all main paths, most files in nano-xxx should have been visited at least once.

Files not naturally visited by main paths get covered in "Side Paths."

### When Paths Revisit the Same Code

When a path naturally goes through a file/module already seen in a previous path, briefly note the connection if it adds understanding. Don't force this — only mention it when it genuinely helps the reader see why that module is important.

**Critical: Mermaid diagrams go near the END as summary, NOT at the beginning.** Putting architecture diagrams at the start = traditional README approach that scares readers before they understand anything.

### Required Elements

1. **Path-based narrative** (as many paths as the project needs — each tracing a concrete question end-to-end through the code)
2. **Creator-perspective + Socratic style within paths** (feel the pain first → think → reveal. Make readers understand WHY before showing HOW)
3. **Hands-on exercise at end of each path** (modify something along that path, observe effect)
   - Format: specific code modification + expected observation
   - Example: "Change `config.timeout` to 0, run the program, observe what error occurs — this demonstrates why the timeout mechanism must exist"
4. **Mermaid diagrams** (near end of document as summary. Generate as many as needed: architecture overview, core data flow, module interactions, etc. No limit on quantity)
5. **Annotated project structure tree** (a `tree`-style code block showing nano-xxx/ directory layout, with `#` comments on each entry explaining its role)
6. **Side Paths** (for files not naturally visited by main paths — brief exploration of what they do and when they get called. Important ones get a mini-trace; trivial ones get 1-2 lines)
7. **Nano vs original comparison table** (at the very end, tells reader "what does real code have that nano doesn't")

### Forbidden Styles

- ❌ Module-by-module explanations ("Module A does X, Module B does Y") — organize by paths, not modules
- ❌ Starting with "architecture overview" or "system design" — architecture should emerge from paths
- ❌ Architecture diagrams at the beginning (scares readers who don't understand yet)
- ❌ Traditional README structure ("Installation / Usage / API")
- ❌ FAQ-style Q&A ("Q: Why? A: Because...")
- ❌ Exercises bundled at the end of the document
- ❌ Pure "what" descriptions without "why"
- ❌ Dumping all information at once without a traceable execution flow

---

## Phase 3: Progressive Expansion (User-Driven)

After reading GUIDE.md and nano-xxx, the user can request at any time:

### Expand a Module

User says: "expand X module" / "I want to dive deeper into X"

→ AI replaces the skeleton in nano-xxx with detailed implementation:
1. **Deep read** the full code of that module in the original project (same standard as Phase 1)
2. Distill based on deep read (keep core, strip tricks)
3. Add learning annotations
4. Update GUIDE.md with a new learning chapter for that module

### Socratic Q&A

User says: "grill me on X" / "quiz me on X"

→ Based on nano-xxx's existing content, ask the user questions like a teacher — confirm understanding, expose blind spots.

### Re-explain

User says: "I don't understand this part" / "why is this done this way"

→ Re-explain from a different angle (analogy, diagram, comparison with alternatives).

---

## Resume Learning

When `/nano-codebase` is invoked:

1. **Check** if `research.md` and `nano-{project-name}/` already exist
2. **If they exist** → Read `research.md` to restore understanding of the project, then check nano-xxx's current state:
   - Which modules are already expanded (detailed implementation)
   - Which modules are still skeleton (TODO placeholders)
3. **Tell user current progress**: "Modules A and B are expanded. C, D, E are still skeleton. Which do you want to dive into next, or start over?"
4. User chooses to continue → Enter Phase 3
5. User chooses to start over → Delete old artifacts, begin from Phase 1

**Progress is implicit in nano-xxx itself**: skeleton = not yet learned, detailed = already learned. `research.md` handles restoring the AI's understanding of the project.

---

## Key Rules

- **Each phase must wait for user confirmation before proceeding.** Never auto-skip.
- **Skipping nano generation for small projects requires user consent.** Never decide unilaterally.
- **GUIDE.md is a learning document, not a README.** Narrative must follow "creator perspective".
- **GUIDE.md must cover EVERY file in nano-xxx.** No orphan files allowed — main paths should naturally visit most files; any remaining files must be covered in the "Side Paths" section. Trivial files (beans, enums, constants) can be covered in 1-2 lines.
- **nano-xxx is code, not documentation.** Must be actual source code files, not code blocks inside markdown.
- **Only output current phase content.** Do not dump all analysis results during Phase 1.
- **Git archaeology is best-effort.** When unavailable, gracefully degrade to logical reconstruction ("if you were building from scratch, the first problem you'd face is...").
