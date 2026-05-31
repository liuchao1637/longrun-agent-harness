# Contributing

Longrun Agent Harness is intentionally small. Contributions should improve practical safety for long-running agent workflows without turning the project into a general agent platform.

## Good Contributions

- validators for common failure modes
- small schemas with clear examples
- synthetic task packages
- documentation that helps maintainers recover from interrupted work
- tests that reproduce real workflow risks

## Avoid

- provider-specific private integrations
- credentials or personal runtime data
- large framework abstractions
- examples copied from private systems

## Local Checks

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
PYTHONPATH=src python -m longrun_harness.cli check examples/coding-task/task.json
```

