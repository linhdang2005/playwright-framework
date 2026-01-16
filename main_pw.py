import sys
import subprocess


def main():
    cmd = [
        sys.executable, "-m", "pytest", "tests",
        "-vv",                      
        "-s",                      
        "-o", "log_cli=true",      
        "-o", "log_cli_level=INFO",
    ]

    subprocess.run(cmd)


if __name__ == "__main__":
    main()
