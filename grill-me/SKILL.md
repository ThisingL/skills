---
name: grill-me
description: Interview the user relentlessly about a plan or design until reaching shared understanding, resolving each branch of the decision tree. Use when user wants to stress-test a plan, get grilled on their design, or mentions "grill me".
---

Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.

Ask the questions one at a time.

If a question can be answered by exploring the codebase, explore the codebase instead.

## Output

When all branches are resolved (or the user says to wrap up), write a complete summary document to the current directory as `grill-summary-{topic}.md`.

The document must be **a complete picture of the final plan**, including:

1. **Already-clear parts** — things the user stated upfront that needed no further questioning
2. **Consensus from grilling** — decisions reached through discussion, including key reasoning and trade-offs considered

Structure it as a self-contained document that someone could pick up and execute from, not a conversation transcript. Organize by topic/domain, not by "what was obvious vs what we discussed".

Before writing, briefly confirm with the user that you're ready to generate the summary (in case they want to add anything). If the conversation ends naturally and all branches are resolved, proactively offer to write it.
