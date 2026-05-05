"""
Run All Tests
"""
import subprocess
import sys


def main():
    """Run pytest with HTML report"""
    cmd = [
        sys.executable, "-m", "pytest",
        "-v",
        "--html=reports/report.html",
        "--self-contained-html",
        "--tb=short"
    ]
    result = subprocess.run(cmd)
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
