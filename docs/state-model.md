# State Model

## Task Package

A task package is a directory with:

- `contract.md`
- `plan.md`
- `handoff.md`
- `qa.md`
- `evidence/`
- `task.json`

## Harness Levels

L2: recoverable task with persistent artifacts.

L3: task with validators and stronger QA.

L4: complex or public-facing workflow that needs evaluator tracking and explicit external-action boundaries.

## Delivery State

`not_ready`: artifacts are not ready for delivery.

`pending_send`: delivery is prepared but has not been visibly sent.

`sent`: visible delivery happened and has a receipt.

`completed`: work and delivery are complete, with evidence.

