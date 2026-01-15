import sys
import subprocess


def main():
    cmd = [
        sys.executable, "-m", "pytest", "tests",
        "-vv",                      # hiển thị rất chi tiết từng test
        "-s",                       # cho phép print / log ra terminal
        "-o", "log_cli=true",       # bật log realtime
        "-o", "log_cli_level=INFO", # mức log INFO
    ]

    subprocess.run(cmd)


if __name__ == "__main__":
    main()
