# 06 Agent Runbook

## Input expected by agent

An agent run should receive exactly one task type:

```text
GLOBAL_AUDIT
VOCAB_REVIEW
PROJECT_CONTENT_REVIEW
QUERY_REVIEW
FREEZE_RELEASE
```

## Generic output expected

Every agent run must output:

```text
1. report markdown
2. patch JSONL
3. patch manifest JSON
4. optional notes
```

## Agent sequence

Recommended sequence for a full repo round:

```text
1. GLOBAL_AUDIT agent
2. VOCAB_REVIEW agent: Material
3. VOCAB_REVIEW agent: Bauteiltyp
4. VOCAB_REVIEW agent: Huerde
5. VOCAB_REVIEW agent: Actors
6. PROJECT_CONTENT_REVIEW agents, five projects at a time
7. QUERY_REVIEW agents, one theme at a time
8. GLOBAL_AUDIT agent again
9. FREEZE_RELEASE agent
```

## Fail conditions

Agent must stop and report if:

```text
schema files are missing
controlled vocabulary seed is missing
constraints.cypher is missing
patch cannot be made idempotent
relationship endpoint cannot be resolved
a proposed merge would lose source evidence
```

## Human review needed

Mark `NEEDS_REVIEW` when:

```text
source evidence conflicts
two concepts may be distinct
project status is unclear
a component might be Bestandserhalt instead of direct reuse
a metric appears at wrong scale but target scope is uncertain
```
