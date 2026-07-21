import ast
import os
import sys
import unittest
from pathlib import Path


PLATFORM_SPECIFIC_MODULES = {
    "ctypes", "fcntl", "termios", "msvcrt",
    "win32api", "win32con", "win32gui", "win32process",
    "pwd", "grp", "resource", "nis", "crypt",
    "posixpath", "ntpath",
}


class TestPortability(unittest.TestCase):
    def test_compatible_with_python_3_11_or_later(self):
        self.assertGreaterEqual(sys.version_info[:2], (3, 11))

    def test_no_platform_specific_imports_in_src(self):
        src_dir = Path(__file__).resolve().parent.parent.parent / "src"
        violations = []

        for py_file in src_dir.rglob("*.py"):
            try:
                tree = ast.parse(py_file.read_text())
            except SyntaxError:
                continue

            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        module = alias.name.split(".")[0]
                        if module in PLATFORM_SPECIFIC_MODULES:
                            violations.append(
                                f"{py_file.relative_to(src_dir)}:{node.lineno} "
                                f"imports '{alias.name}'"
                            )
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        module = node.module.split(".")[0]
                        if module in PLATFORM_SPECIFIC_MODULES:
                            violations.append(
                                f"{py_file.relative_to(src_dir)}:{node.lineno} "
                                f"imports from '{node.module}'"
                            )

        self.assertEqual(
            violations, [],
            msg="Platform-specific imports found:\n" + "\n".join(violations),
        )


if __name__ == "__main__":
    unittest.main()
