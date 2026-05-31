from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping


@dataclass(frozen=True)
class ValidationResult:
    ok: bool
    issues: list[str]

    def to_dict(self) -> dict[str, Any]:
        return {"ok": self.ok, "issues": self.issues}


REQUIRED_L4_FILE_POINTERS = (
    "contract_file",
    "plan_file",
    "handoff_file",
    "qa_file",
)


def check_task_package(task: Mapping[str, Any]) -> ValidationResult:
    issues: list[str] = []
    task_id = task.get("id", "<unknown>")
    level = task.get("harness_level")

    if level not in {"L2", "L3", "L4"}:
        issues.append(f"{task_id}: harness_level must be L2, L3, or L4")

    for key in REQUIRED_L4_FILE_POINTERS:
        path_value = task.get(key)
        if not path_value:
            issues.append(f"{task_id}: missing {key}")
            continue
        if not Path(path_value).is_file():
            issues.append(f"{task_id}: {key} does not exist: {path_value}")

    evidence_dir = task.get("evidence_dir")
    if not evidence_dir:
        issues.append(f"{task_id}: missing evidence_dir")
    elif not Path(evidence_dir).is_dir():
        issues.append(f"{task_id}: evidence_dir does not exist: {evidence_dir}")

    if level == "L4":
        for key in ("validator_status", "evaluator_status"):
            if task.get(key) in {None, "", "missing", "not_required"}:
                issues.append(f"{task_id}: {key} must be tracked for L4 tasks")

    return ValidationResult(ok=not issues, issues=issues)


def validate_final_delivery_state(state: Mapping[str, Any]) -> ValidationResult:
    issues: list[str] = []
    task_id = state.get("task_id", state.get("id", "<unknown>"))
    delivery_status = state.get("delivery_status")
    receipt = state.get("visible_delivery_receipt")

    if delivery_status in {"pending_send", "sent", "completed"} and not receipt:
        issues.append(f"{task_id}: visible_delivery_receipt is required for {delivery_status}")

    if receipt:
        for key in ("surface", "message_id", "sent_at"):
            if not receipt.get(key):
                issues.append(f"{task_id}: visible_delivery_receipt missing {key}")

    return ValidationResult(ok=not issues, issues=issues)


def validate_visible_receipt(receipt: Mapping[str, Any]) -> ValidationResult:
    issues: list[str] = []
    for key in ("surface", "message_id", "sent_at"):
        if not receipt.get(key):
            issues.append(f"visible receipt missing {key}")
    return ValidationResult(ok=not issues, issues=issues)
