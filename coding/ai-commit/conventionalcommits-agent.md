# Conventional Commits 1.0.0 — Agent Reference

## Format

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

## Structural Elements

1. **fix:** patches a bug (correlates with PATCH in SemVer)
2. **feat:** introduces a new feature (correlates with MINOR in SemVer)
3. **BREAKING CHANGE:** a footer `BREAKING CHANGE:`, or `!` after type/scope, introduces a breaking API change (correlates with MAJOR in SemVer). Can be part of any type.
4. Other types allowed: `build:`, `chore:`, `ci:`, `docs:`, `style:`, `refactor:`, `perf:`, `test:`, and others.
5. Footers other than `BREAKING CHANGE:` follow [git trailer format](https://git-scm.com/docs/git-interpret-trailers).

A scope may be provided after type in parentheses: `feat(parser): add ability to parse arrays`

## Examples

```
feat: allow provided config object to extend other configs

BREAKING CHANGE: `extends` key in config file is now used for extending other config files
```

```
feat(api)!: send an email to the customer when a product is shipped
```

```
docs: correct spelling of CHANGELOG
```

```
feat(lang): add Polish language
```

```
fix: prevent racing of requests

Introduce a request id and a reference to latest request. Dismiss
incoming responses other than from latest request.

Reviewed-by: Z
Refs: #123
```

## Specification Rules

1. Commits MUST be prefixed with a type (noun: `feat`, `fix`, etc.), followed by OPTIONAL scope, OPTIONAL `!`, and REQUIRED terminal colon and space.
2. `feat` MUST be used for new features; `fix` MUST be used for bug fixes.
3. Scope: OPTIONAL noun in parentheses after type, e.g., `fix(parser):`
4. Description MUST immediately follow the colon and space — short summary of code changes.
5. Body MAY follow after one blank line. Free-form, any number of newline-separated paragraphs.
6. Footers MAY follow after one blank line. Each: word token + `:<space>` or `<space>#` separator + string value.
7. Footer tokens MUST use `-` in place of whitespace (exception: `BREAKING CHANGE`).
8. Footer value MAY contain spaces and newlines; parsing terminates at next valid token/separator pair.
9. Breaking changes MUST be indicated in type/scope prefix (`!`) or as footer entry.
10. If `!` is used, `BREAKING CHANGE:` MAY be omitted from footer; commit description SHALL describe the breaking change.
11. Types other than `feat` and `fix` MAY be used.
12. Conventional Commits MUST NOT be treated as case-sensitive, except `BREAKING CHANGE` (uppercase).
13. `BREAKING-CHANGE` is synonymous with `BREAKING CHANGE` as footer token.
