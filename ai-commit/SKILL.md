---
name: ai-commit
description: |
  Use when user wants to generate a commit message from staged git changes,
  or invokes /ai-commit. Triggers on phrases like "help me commit",
  "generate commit message", "write a commit".
allowed-tools:
  - Bash
  - Read
  - AskUserQuestion
---

# AI Commit

Generate high-quality commit messages from staged changes, strictly following the Conventional Commits 1.0.0 specification.

## Reference

Read `conventionalcommits-agent.md` in this skill's directory before generating messages.
Full specification for human reference: `conventionalcommits.md`.

## Workflow

### Step 1: Read Staged Changes

```bash
git diff --cached --stat
```

If NO staged changes:
> No staged changes found. Please run `git add` first.

Then **stop**.

If there ARE staged changes, write the diff to a temp file and read it (avoids truncation for large diffs):

```bash
git diff --cached > /tmp/.ai-commit-diff.tmp
```

Then use the Read tool to read `/tmp/.ai-commit-diff.tmp`.

### Step 2: Read Git History

```bash
git log --oneline -20
```

Detect the project's existing style as **implicit input** — match it automatically without asking:

- **Language**: English, Chinese, or mixed?
- **Scope usage**: With/without? Naming conventions?
- **Body usage**: Single-line or multi-line common?
- **Capitalization**: First letter uppercase or lowercase?

### Step 3: Analyze Changes

Determine:
1. **Type** — using the table below
2. **Scope** — from file paths (match style from git history)
3. **Breaking change?** — API changes, removed exports, changed signatures
4. **Motivation** — why was this change made?

#### Type Inference

| Type | Indicators |
|------|------------|
| **feat** | New files with functionality, new exports, new API endpoints |
| **fix** | Error handling changes, logic corrections, crash fixes |
| **docs** | README, markdown, comments, documentation-only |
| **style** | Formatting, whitespace, no logic changes |
| **refactor** | Renaming, restructuring, no behavior change |
| **perf** | Optimization, caching, algorithm improvements |
| **test** | Test files, test utilities, mocks |
| **build** | Package config, build scripts, dependencies |
| **ci** | CI/CD config, GitHub Actions, workflows |
| **chore** | Config files, .gitignore, maintenance |
| **revert** | Reverting previous commits |

#### Scope Detection

Extract from file paths:
- `src/api/*` → `api`, `src/components/*` → `ui`, `src/auth/*` → `auth`
- `src/db/*` → `db`, `tests/*` → `test`, `docs/*` → `docs`
- `.github/workflows/*` → `ci`
- Root config files only → omit scope
- Multiple directories equally affected → omit scope

### Step 4: Generate 3 Commit Messages

**Format rules:**
- Type: lowercase noun from table above
- Scope: optional, noun in parentheses
- `!`: append after type/scope for breaking changes
- Description: imperative mood, lowercase first letter, no period, max 50 chars
- Body (if git history shows multi-line is common): one blank line after description, wrapped at 72 chars, explain motivation and contrast with previous behavior
- Footer: git trailer format (`BREAKING CHANGE: ...`, `Refs: #123`)

**Three options should vary in angle and wording:**
- Different type interpretations when reasonable (e.g., `refactor` vs `fix`)
- Different scope choices (with vs without, different nouns)
- Different descriptions emphasizing different aspects
- If body included: different angles (the "what", the "why", the contrast)

**Quality:**
- Be specific: "add login endpoint" not "add new feature"
- Imperative mood: "add" not "added"
- No redundancy: don't repeat type in description
- Reflect the actual diff, not assumptions

### Step 5: Present Options

Use `AskUserQuestion`:
- Question: `选择 commit message:`
- Option 1-3: First line as `label`. If message has body/footer, show full message in `preview`.
- Option 4: label = "Regenerate", description = "Generate 3 new options"

If user selects **Regenerate** or provides custom instructions via "Other", go back to Step 4 with their guidance. Do not repeat previous options.

### Step 6: Commit

Single-line:
```bash
git commit -m "<selected message>"
```

Multi-line (with body/footer):
```bash
git commit -m "$(cat <<'EOF'
<type>[scope]: <description>

<body>

<footer>
EOF
)"
```

After commit, clean up:
```bash
rm -f /tmp/.ai-commit-diff.tmp
```

Report: commit hash (short) + message used.

## Example

**Staged diff:** New file `src/auth/login.ts` (45 lines), git history is Chinese

**Generated options:**
1. `feat(auth): 添加用户登录接口`
2. `feat: 添加 JWT 登录认证端点`
3. `feat(auth): 实现用户登录功能` + body: "新增 POST /auth/login 接口，接收邮箱和密码，校验凭证并返回签名 JWT token。"

## Constraints

- **DO NOT** run `git add` — only work with what is already staged
- **DO NOT** run `git push` — only commit locally
- **DO NOT** modify any source files
- **DO NOT** append `Co-Authored-By` or any trailer unless the user explicitly asks
- **DO NOT** create or initialize git repositories
