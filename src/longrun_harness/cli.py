from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .validators import (
    check_task_package,
    validate_final_delivery_state,
    validate_visible_receipt,
)


def _load_json(path: str) -> dict:
    return json.loads(Path(path).read_text())


def _init_task_package(task_id: str, root: str) -> dict:
    task_dir = Path(root) / task_id
    task_dir.mkdir(parents=True, exist_ok=True)
    (task_dir / "evidence").mkdir(exist_ok=True)

    templates = {
        "contract.md": f"# {task_id} Contract\n\nDefine goal, scope, boundaries, and success criteria.\n",
        "plan.md": f"# {task_id} Plan\n\n1. Gather context.\n2. Make the smallest safe change.\n3. Verify.\n4. Update handoff.\n",
        "handoff.md": f"# {task_id} Handoff\n\nStatus: initialized.\n\nNext action: fill the task contract and plan.\n",
        "qa.md": f"# {task_id} QA\n\nValidation commands and evidence go here.\n",
    }
    for name, content in templates.items():
        path = task_dir / name
        if not path.exists():
            path.write_text(content)

    task = {
        "id": task_id,
        "harness_level": "L4",
        "contract_file": str(task_dir / "contract.md"),
        "plan_file": str(task_dir / "plan.md"),
        "handoff_file": str(task_dir / "handoff.md"),
        "qa_file": str(task_dir / "qa.md"),
        "evidence_dir": str(task_dir / "evidence"),
        "validator_status": "pending",
        "evaluator_status": "pending",
    }
    (task_dir / "task.json").write_text(json.dumps(task, indent=2) + "\n")
    return task


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="longrun-harness")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="Create a resumable task package")
    init_parser.add_argument("task_id")
    init_parser.add_argument("--root", default="tasks")

    check_parser = subparsers.add_parser("check", help="Validate a task package JSON file")
    check_parser.add_argument("task_json")

    delivery_parser = subparsers.add_parser(
        "validate-final-delivery",
        help="Validate visible delivery state JSON",
    )
    delivery_parser.add_argument("state_json")

    receipt_parser = subparsers.add_parser(
        "validate-receipt",
        help="Validate a visible delivery receipt JSON",
    )
    receipt_parser.add_argument("receipt_json")

    args = parser.parse_args(argv)

    if args.command == "init":
        task = _init_task_package(args.task_id, args.root)
        result = check_task_package(task)
    elif args.command == "check":
        result = check_task_package(_load_json(args.task_json))
    elif args.command == "validate-final-delivery":
        result = validate_final_delivery_state(_load_json(args.state_json))
    elif args.command == "validate-receipt":
        result = validate_visible_receipt(_load_json(args.receipt_json))
    else:
        parser.error(f"unknown command: {args.command}")

    print(json.dumps(result.to_dict(), indent=2))
    return 0 if result.ok else 1


if __name__ == "__main__":
    sys.exit(main())
