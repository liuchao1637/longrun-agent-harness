# Migration Guide

## From Prompt-Only Workflows

1. Create a task package with `longrun-harness init`.
2. Move the goal and safety boundaries into `contract.md`.
3. Move the step plan into `plan.md`.
4. Keep recovery notes in `handoff.md`.
5. Put command output and receipts in `evidence/`.
6. Run `longrun-harness check` before claiming completion.

## From Cron Scripts

Separate three things:

- actual script result
- wrapper/transport result
- user-visible notification result

Do not treat a model or session wrapper error as proof that the underlying mechanical job failed.

