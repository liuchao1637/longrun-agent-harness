# Longrun Agent Harness

Lightweight validation tools for long-running AI agent workflows.

AI coding and operations agents are useful, but long-running tasks fail in predictable ways: state gets lost, tasks are marked done before visible delivery, cron/checkback jobs emit noisy false alerts, and handoffs are not verifiable.

Longrun Agent Harness provides small schemas, examples, and validators for those failure modes.

## Why This Exists

Most agent workflows start as prompts and shell scripts. That is fine for one-off tasks, but brittle for work that needs to survive:

- multiple sessions
- delayed provider jobs
- cron or checkback loops
- human approval gates
- visible delivery requirements
- independent review

This project gives maintainers a minimal state and validation layer before they need a full platform.

## What It Includes

- task package pointer checks
- final delivery receipt validation
- synthetic examples for coding/release/cron workflows
- a tiny CLI suitable for local checks and CI

## Quick Start

```bash
python -m longrun_harness.cli check examples/coding-task/task.json
python -m unittest discover -s tests -v
```

Create a new resumable task package:

```bash
python -m longrun_harness.cli init my-task --root tasks
```

Validate a visible delivery receipt:

```bash
python -m longrun_harness.cli validate-receipt receipt.json
```

## Core Concepts

Task contract: defines the goal, scope, external action boundaries, and success criteria.

Handoff: tells the next session exactly where to resume.

Evidence directory: keeps validator output, command logs, receipts, and review artifacts.

Visible delivery receipt: proves that a user-facing delivery actually happened, instead of only being marked complete internally.

## Example Task JSON

```json
{
  "id": "example-coding-task",
  "harness_level": "L4",
  "contract_file": "examples/coding-task/contract.md",
  "plan_file": "examples/coding-task/plan.md",
  "handoff_file": "examples/coding-task/handoff.md",
  "qa_file": "examples/coding-task/qa.md",
  "evidence_dir": "examples/coding-task/evidence",
  "validator_status": "pending",
  "evaluator_status": "pending"
}
```

## Project Status

Pre-release local scaffold. The public API may change before `0.1.0`.

## Non-Goals

This is not an official OpenAI project and not a general-purpose agent framework. It is a small operational safety layer for maintainers already using agents.

## Roadmap

See [ROADMAP.md](ROADMAP.md).

