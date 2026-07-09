# Constitutional Governance: ML & Causal Inference Course

**Immutable principles for the Machine Learning and Causal Inference course at Renmin University of China.**

---

## Why Constitutional Governance?

As this research project grows, some decisions become non-negotiable (to maintain quality, reproducibility, and theoretical consistency). Others remain flexible based on context.

Making this distinction explicit prevents:

- Repeated debates on settled issues
- Inconsistent application of standards
- Uncertainty about when to ask vs. decide

---

## Article I: Code-First Teaching

Every concept must have accompanying executable code in R and/or Python.

**Why this matters:** Students learn by doing. Every theoretical concept must be executable and verifiable.

**Requirements:**

- Code examples for every method (Python and/or R)
- Data provenance documented in `Data/README.md`
- Seeds documented for all stochastic simulations
- Lab exercises with solutions in both languages

**Exceptions:** Purely theoretical concepts (e.g., identification arguments) with clear exposition.

---

## Article II: Clarity Before Complexity

Identification assumptions must be explicitly stated; intuition must precede mathematical formalism.

**Why this matters:** Students need conceptual understanding before technical details. Hidden assumptions lead to misapplication.

**Requirements:**

- Every identification assumption stated with intuition first
- Potential outcomes framework explained before math
- DAGs/visuals precede equations where possible
- Common pitfalls explicitly warned against

**Exceptions:** Advanced topics for graduate students; review material.

---

## Article III: Quality Gate

Nothing commits below 80/100; student-facing materials require 90+.

**Why this matters:** Course materials accumulate errors that confuse students. Quality ensures pedagogical effectiveness.

**Requirements:**

- Quality score >= 80 for instructor materials (drafts)
- Quality score >= 90 for student-facing materials (slides, labs)
- Numerical replication within 1e-6 for code examples
- All code tested before distribution to students

**Exceptions:** Explicit WIP branches tagged `[WIP]`; exploration folder (60/100 threshold).

---

## Article IV: Data Provenance

All datasets documented with source, date, and processing steps in `Data/README.md`.

**Why this matters:** Teaching data must be trustworthy. Students learn reproducibility by example.

**Requirements:**

- Source URL or citation for each dataset
- Download date
- Processing steps documented
- Variable definitions included
- Sample restrictions noted
- Clear licensing for educational use

**Exceptions:** Synthetic/simulated data with DGP documented; classic teaching datasets (LaLonde, Card-Krueger).

---

## Article V: Plan-First Threshold

Enter plan mode for tasks requiring >3 files, >30 minutes, or multi-step lecture creation.

**Why this matters:** Course development requires coordination. Planning prevents pedagogical inconsistencies.

**Requirements:**

- Requirements spec for ambiguous tasks
- Saved plan in `quality_reports/plans/`
- User approval before implementation
- Session log updated at key milestones

**Exceptions:** Exploration folder (fast-track workflow); typo fixes; single-file edits with clear scope.

---

## User Preferences (Override Anytime)

These patterns ARE flexible and can vary by context:

- File naming conventions: `snake_case` for R, `kebab-case` for documentation
- Tolerance thresholds: 1e-6 for point estimates, 1e-4 for aggregates (can tighten for final version)
- Figure aesthetics: Publication-ready, consistent with institutional theme
- Code verbosity: Comments for non-obvious steps, self-documenting variable names
- Citation style: Author-Year (economics standard)

---

## Requesting Amendment

When requesting deviation from an article, specify:

> "Amending Article X (permanent change) or overriding for this task (one-time exception)?"

**Amendment process:**

1. Propose amendment with rationale
2. Discuss implications (what breaks? what improves?)
3. Update this file if approved
4. Document change in session log with `[CONSTITUTIONAL AMENDMENT]` tag

---

## Maintenance

**Review cadence:** Quarterly (or after every 5 research milestones)

**Review questions:**

- Are all articles still relevant?
- Are any being violated repeatedly? (If yes, amend or delete)
- Are any new patterns emerging? (If yes, consider promoting to article)
- Are articles enabling or obstructing work?

---

## Amendment History

| Date | Article | Change | Rationale |
|------|---------|--------|-----------|
| 2026-02-24 | All | Initial adoption | Project initialization |
