from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest


class AcceptanceTests(unittest.TestCase):
    def test_optimized_execution_fails_before_accessing_project_files(self):
        # An isolated copy has no workbook or installed CLI: the guard must run first.
        source = Path(__file__).with_name("acceptance.py")
        with TemporaryDirectory() as directory:
            script = Path(directory) / "acceptance.py"
            script.write_bytes(source.read_bytes())
            for flag in ("-O", "-OO"):
                with self.subTest(flag=flag):
                    result = subprocess.run(
                        [sys.executable, flag, str(script)], cwd=directory,
                        capture_output=True, text=True,
                    )
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn("run Python without -O or -OO", result.stderr)
                    self.assertNotIn("PASS:", result.stdout)
                    self.assertEqual(list(Path(directory).iterdir()), [script])
