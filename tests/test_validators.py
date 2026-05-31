import tempfile
import unittest
from pathlib import Path

from longrun_harness.validators import (
    check_task_package,
    validate_final_delivery_state,
    validate_visible_receipt,
)


class ValidatorTests(unittest.TestCase):
    def test_check_task_package_requires_core_pointers(self):
        with tempfile.TemporaryDirectory() as root:
            tmp_path = Path(root)
            task = {
                "id": "demo-task",
                "harness_level": "L4",
                "contract_file": str(tmp_path / "contract.md"),
                "plan_file": str(tmp_path / "plan.md"),
                "handoff_file": str(tmp_path / "handoff.md"),
                "qa_file": str(tmp_path / "qa.md"),
                "evidence_dir": str(tmp_path / "evidence"),
                "validator_status": "pending",
                "evaluator_status": "pending",
            }
            for name in ("contract.md", "plan.md", "handoff.md", "qa.md"):
                (tmp_path / name).write_text("# demo\n")
            (tmp_path / "evidence").mkdir()

            result = check_task_package(task)

            self.assertTrue(result.ok)
            self.assertEqual(result.issues, [])

    def test_check_task_package_reports_missing_files(self):
        with tempfile.TemporaryDirectory() as root:
            tmp_path = Path(root)
            task = {
                "id": "demo-task",
                "harness_level": "L4",
                "contract_file": str(tmp_path / "missing-contract.md"),
                "plan_file": str(tmp_path / "plan.md"),
                "handoff_file": str(tmp_path / "handoff.md"),
                "qa_file": str(tmp_path / "qa.md"),
                "evidence_dir": str(tmp_path / "evidence"),
                "validator_status": "pending",
                "evaluator_status": "pending",
            }

            result = check_task_package(task)

            self.assertFalse(result.ok)
            self.assertTrue(any("contract_file" in issue for issue in result.issues))

    def test_validate_final_delivery_state_rejects_pending_send_without_receipt(self):
        state = {
            "task_id": "demo-task",
            "delivery_status": "pending_send",
            "visible_delivery_receipt": None,
        }

        result = validate_final_delivery_state(state)

        self.assertFalse(result.ok)
        self.assertTrue(any("visible_delivery_receipt" in issue for issue in result.issues))

    def test_validate_final_delivery_state_accepts_sent_with_receipt(self):
        state = {
            "task_id": "demo-task",
            "delivery_status": "sent",
            "visible_delivery_receipt": {
                "surface": "telegram",
                "message_id": "123",
                "sent_at": "2026-05-31T11:35:00+08:00",
            },
        }

        result = validate_final_delivery_state(state)

        self.assertTrue(result.ok)
        self.assertEqual(result.issues, [])

    def test_validate_visible_receipt_accepts_required_fields(self):
        receipt = {
            "surface": "telegram",
            "message_id": "123",
            "sent_at": "2026-05-31T11:50:00+08:00",
        }

        result = validate_visible_receipt(receipt)

        self.assertTrue(result.ok)
        self.assertEqual(result.issues, [])


if __name__ == "__main__":
    unittest.main()
