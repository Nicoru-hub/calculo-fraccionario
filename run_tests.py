#!/usr/bin/env python
"""Run all tests for the calculus project."""

import subprocess
import sys

if __name__ == "__main__":
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-v", "--tb=short"],
        cwd="."
    )
    sys.exit(result.returncode)
