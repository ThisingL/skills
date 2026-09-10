# Learner State Policy

Policy ID: `artifact-evidence-v0.1`

This file is the single source of truth for converting knowledge-base evidence into transformation strength. V0 is an artifact-evidence heuristic, not a memory model: it has no forgetting curve, review history, quiz score, embedding store, or claim about present recall.

## Stable contract

For each source knowledge unit, consume:

- any explicit current-familiarity statement from this run;
- matched evidence path and heading;
- evidence area: `notes` or `references`;
- semantic relation: `equivalent`, `similar`, `extends`, `differs`, or `conflicts`;
- match confidence and a short evidence summary.

Return:

- learner state;
- confidence;
- allowed transformation;
- evidence and knowledge delta for the companion audit.

## V0 state rules

| Observable evidence | Learner state | Default confidence | Allowed transformation |
|---|---|---:|---|
| The user explicitly says in this run that the material is currently familiar or mastered | `confirmed-current` | high | Deep compression with a minimal bridge |
| An equivalent claim appears in `notes/` | `documented-understanding` | medium historical evidence | Deep compression with a compact recall cue and argument bridge |
| An equivalent claim appears only in `references/` | `documented-exposure` | medium-low | Moderate compression: concise reactivation before the delta |
| Evidence is merely similar rather than equivalent | `inferred-familiarity` | low | Do not compress as mastered; retain the explanation and use a bounded analogy if useful |
| No relevant textual evidence is found | `novel` | unknown | Preserve the reasoning chain; add scaffolding or a familiar example when useful |

The presence of a file, filename match, or semantically nearby topic never proves current mastery. Only `confirmed-current` permits present-tense wording such as `you already know`. For `documented-understanding`, say that the notes record or previously frame the idea; do not claim the user currently remembers it.

## Relation overrides

- `extends`: preserve every new condition, mechanism, consequence, and scope change even when the base claim is documented.
- `differs`: retain both formulations and make the difference easy to inspect.
- `conflicts`: retain both claims, their source locations, assumptions, and applicability conditions. Do not silently replace the note or describe either claim as `more accurate`, `more precise`, a `correction`, `wrong`, or a `misconception` unless independent verification was requested and performed. If the source itself makes such a judgment, attribute it explicitly as the source's position.
- Low-confidence or incomplete evidence always reduces compression strength.
- A content match outranks a title or keyword match. Evidence must come from the note body.

## Unit granularity and mixed evidence

Learner state applies to one minimal claim; semantic relation is a separate field. Do not label an entire extended claim `documented-understanding` merely because one premise is documented.

- For `extends`, split the documented premise from the extension whenever each can stand as a meaningful unit. Classify the equivalent premise from its evidence and classify the unmatched extension as `novel`.
- For `differs` or `conflicts`, classify each side's evidence separately and record the cross-source relation in the delta.
- If a mixed unit cannot be split without distorting its meaning, use the least compressive applicable state and explain the documented subpart in `Evidence`.

## Meaning of transformation strengths

### Deep compression

Replace repeated exposition with the smallest coherent bridge that preserves:

1. a retrieval cue for the prior idea;
2. its role in the current argument;
3. all source details that extend, qualify, or conflict with it.

Deep compression is never deletion solely because a note exists.

### Moderate compression

Give a short reactivation of the idea before presenting the delta. Do not assume familiarity with omitted intermediate steps.

### Preserve or expand

Keep definitions and reasoning dependencies. Add scaffolding only when it improves comprehension without inventing facts. Prefer examples already present in the knowledge base; state both the analogy mapping and where it stops.

## Audit requirements

Record this policy ID and one row per material transformation decision. Evidence paths are relative to the normalized knowledge root. Separate `no evidence found` from `evidence that the learner is unfamiliar`—V0 normally has only the former.

Future memory systems may replace how learner state is derived, but they should preserve this input/output contract and publish a new policy ID.
