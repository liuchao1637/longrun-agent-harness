# Failure Modes

## False Completion

The agent marks a task complete because the internal artifact exists, but no user-visible delivery happened.

Mitigation: require a visible delivery receipt before `sent` or `completed` state.

## Lost Handoff

A long task is interrupted and the next session cannot recover the current stage, next action, or required artifact.

Mitigation: require contract, plan, handoff, QA, and evidence pointers.

## Noisy Checkback

A cron or checkback job performs a successful no-op but reports failure because the wrapper, model layer, or session state changed.

Mitigation: separate mechanical status from model reasoning and require structured result envelopes.

## Unverified External Action

The agent prepares a public or external action but does not distinguish local readiness from actual publication.

Mitigation: track external action boundaries and require explicit approval before public side effects.

