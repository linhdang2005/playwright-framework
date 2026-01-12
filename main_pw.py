import os
import sys
import subprocess

sys.path.extend([
    os.path.join(os.getcwd(), "utils"),
    os.path.join(os.getcwd(), "tests"),
    os.getcwd(),
])
from utils import common

def main_pw():
    os.makedirs("reports/html", exist_ok=True)

    cmd = [
        sys.executable, "-m", "pytest", "tests",
        "-vv",                         
        "-s",                 
        "-o", "log_cli=true",
        "-o", "log_cli_level=INFO",
        "--html=reports/html/report.html", "--self-contained-html",
    ]
    
    # Add CI-specific options
    if os.getenv("GITHUB_ACTIONS"):
        cmd.extend([
            "--tb=short",  # Shorter traceback for CI
            "--maxfail=5", # Stop after 5 failures to save time
        ])

    print("Running:", " ".join(cmd))
    try:
        # capture_output=True để in được stderr khi fail
        result = subprocess.run(cmd, check=False, text=True, capture_output=True)
        # In realtime output (tùy bạn)
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)

        print("HTML report:", os.path.abspath("reports/html/report.html"))

        if result.returncode == 0:
            common.exit_program(common.success)
        else:
            print(f"Pytest failed with exit code {result.returncode}")
            common.exit_program(common.failure)

    except Exception as e:
        print(f"Unexpected error when running pytest: {e}")
        print(f"Error output: {e.output}")
        print("Please check the test logs for more details.")
        common.exit_program(common.failure)

if __name__ == "__main__":
    main_pw()