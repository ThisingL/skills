---
name: personalizing-learning-content
description: Use when a user wants pasted text, Markdown, plain-text files, or PDFs adapted against their own knowledge base, especially to reduce repeated material, surface knowledge differences, or personalize explanations.
---

# Personalizing Learning Content

Transform source material into a coherent learning document whose detail is calibrated by explicit evidence in a user-provided Markdown knowledge base. This is knowledge-conditioned rewriting, not generic summarization.

## Knowledge-base path gate

A knowledge-base path explicitly supplied for the current run is a hard precondition. Run this gate before inspecting the source, searching files, or writing output.

If the path is absent, respond only with: `Please provide the knowledge-base path (either a project root containing knowledge/, or a direct knowledge root containing notes/ and/or references/).` Then stop.

An obvious `knowledge/` directory, a path from another task or earlier run, a README hint, the current project layout, or a directory found by search does not count as user-supplied. Even when the request says `find it yourself`, `do not ask`, or suggests there is only one likely directory, do not scan, guess, auto-select, or reuse a path.

Red flags that mean the gate has failed: `I can locate it`, `the project clearly uses ...`, `the previous run used ...`, or beginning any filesystem search before a path was supplied.

## Required inputs

- Accept one primary source per run: pasted text, `.md`, `.txt`, or `.pdf`.
- Require a knowledge-base path on every run and apply the gate above.
- Accept either a project root containing `knowledge/` or a direct knowledge root containing `notes/` and/or `references/`; normalize it before reading.
- Treat the entire normalized knowledge root as read-only.
- Use an explicit output path when supplied. Otherwise resolve the output root as: Codex workspace root, then Git root, then current working directory. Ask when multiple roots make this ambiguous.

The optional learning goal defaults to fast comprehension: compress repetition, preserve the reasoning chain, and emphasize real knowledge delta. Follow an explicit exam, review, research, or depth goal instead. Default the output language to the user's current language and retain useful original technical terms.

## Workflow

1. Pass the knowledge-base path gate. Do not continue until it passes.
2. Inspect the source before rewriting. For PDFs, read [references/pdf-ingestion.md](references/pdf-ingestion.md) and complete its extraction checks.
3. Inventory Markdown evidence under `notes/` and `references/`. For a manageable knowledge base, read it fully. For a large one, first inspect filenames and headings, then search source concepts, synonyms, and related terms; read candidate sections with enough surrounding context to classify the relationship. A filename alone is not evidence.
4. Build a global outline of the source, then divide it into semantic knowledge units such as definitions, claims, mechanisms, examples, conditions, counterexamples, and conclusions. Preserve source locators and dependencies between premises and conclusions.
5. For every run, read [references/learner-state-policy.md](references/learner-state-policy.md). Map each relevant unit to knowledge evidence using `equivalent`, `similar`, `extends`, `differs`, or `conflicts`, then apply the policy's state, confidence, and allowed transformation. Do not equate a written note with current recall.
6. Recompose the material around learning value rather than mechanically following chunk order. Deep compression still retains a recall cue, the unit's role in the present argument, and every novel qualifier needed for coherence. Similar knowledge may supply an analogy only when the mapping and its stopping point are clear.
7. Preserve source uncertainty, qualifications, tables, figures, citations, and meaningful conflicts. Unless the user asks for fact-checking, a conflict is a comparison between claims, not permission to declare either source correct. Attribute judgments made by the source, and avoid unverified verdict language such as `more accurate`, `more precise`, `corrects`, `wrong`, or `misconception` in both artifacts.
8. Create the paired Markdown artifacts below. Never modify the knowledge base.

## Main artifact

Write a standalone, natural reading experience. It may reorganize and synthesize the source, but it must preserve the source's logical dependencies and knowledge delta. Do not expose learner-state labels, retrieval diagnostics, or an `already known / unknown` processing outline in the prose. Use headings only when they improve the subject's explanation.

Do not say `you know`, `you remember`, or an equivalent present-tense mastery claim unless the user explicitly stated current familiarity in this run. Historical evidence can instead be bridged neutrally, for example: `Your notes previously framed this as ...`.

## Companion knowledge diff

Make the companion human-readable and auditable, not a debug dump. Include:

- source label and processed scope;
- normalized knowledge-base shape without its absolute path;
- learner-state policy ID;
- knowledge evidence used, with paths relative to the normalized knowledge root;
- a table with `Knowledge unit | Learner state | Confidence | Evidence | Transformation | Knowledge delta`;
- additions, refinements, conflicts, low-confidence matches, extraction limitations, and optional knowledge-base update suggestions;
- a statement that the knowledge base was not modified.

Use source page/section locators where available. `No match found` means only that this run found no evidence; it does not prove the user has never learned the material.

## Filenames and writes

Choose a lowercase ASCII English kebab-case slug that captures the material's main meaning rather than copying its source title.

- Main: `<meaning-slug>.md`
- Companion: `<meaning-slug>-knowledge-diff.md`

Avoid generic names such as `summary`, `notes`, `final`, and numbered suffixes. Before writing, check both target paths. Never silently overwrite. Resolve a collision with a meaningful English concept, source, or year qualifier; ask if no honest qualifier is available. Write both files directly under the resolved output root.

In the final response, link both generated files and briefly state the knowledge evidence used, the most important delta, and any extraction uncertainty.

## Boundaries

Do not use this skill for ordinary summarization, standalone PDF Q&A, or teaching that does not use a personal knowledge base. Do not browse for external facts unless the user requests verification or outside enrichment.
