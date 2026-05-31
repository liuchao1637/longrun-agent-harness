import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class CliTests(unittest.TestCase):
    def test_cli_check_reads_task_json(self):
        with tempfile.TemporaryDirectory() as root:
            tmp_path = Path(root)
            task_dir = tmp_path / "demo"
            task_dir.mkdir()
            for name in ("contract.md", "plan.md", "handoff.md", "qa.md"):
                (task_dir / name).write_text("# demo\n")
            (task_dir / "evidence").mkdir()
            task_file = tmp_path / "task.json"
            task_file.write_text(
                json.dumps(
                    {
                        "id": "demo-task",
                        "harness_level": "L4",
                        "contract_file": str(task_dir / "contract.md"),
                        "plan_file": str(task_dir / "plan.md"),
                        "handoff_file": str(task_dir / "handoff.md"),
                        "qa_file": str(task_dir / "qa.md"),
                        "evidence_dir": str(task_dir / "evidence"),
                        "validator_status": "pending",
                        "evaluator_status": "pending",
                    }
                )
            )

            completed = subprocess.run(
                [sys.executable, "-m", "longrun_harness.cli", "check", str(task_file)],
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertIn('"ok": true', completed.stdout)

    def test_cli_init_creates_resumable_task_package(self):
        with tempfile.TemporaryDirectory() as root:
            root_path = Path(root)

            completed = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "longrun_harness.cli",
                    "init",
                    "demo-task",
                    "--root",
                    str(root_path),
                ],
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(completed.returncode, 0, completed.stderr)
            task_dir = root_path / "demo-task"
            self.assertTrue((task_dir / "contract.md").is_file())
            self.assertTrue((task_dir / "plan.md").is_file())
            self.assertTrue((task_dir / "handoff.md").is_file())
            self.assertTrue((task_dir / "qa.md").is_file())
            self.assertTrue((task_dir / "evidence").is_dir())
            self.assertTrue((task_dir / "task.json").is_file())

    def test_cli_validate_receipt_rejects_missing_message_id(self):
        with tempfile.TemporaryDirectory() as root:
            receipt_file = Path(root) / "receipt.json"
            receipt_file.write_text(
                json.dumps(
                    {
                        "surface": "telegram",
                        "sent_at": "2026-05-31T11:50:00+08:00",
                    }
                )
            )

            completed = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "longrun_harness.cli",
                    "validate-receipt",
                    str(receipt_file),
                ],
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(completed.returncode, 1)
            self.assertIn("message_id", completed.stdout)


if __name__ == "__main__":
    unittest.main()
