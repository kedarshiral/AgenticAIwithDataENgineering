import subprocess
from datetime import datetime


def run(cmd):
    subprocess.run(
        cmd,
        shell=True,
        check=True
    )


commit_msg = (
    f"Auto data refresh "
    f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
)

run("git add data/source_github")

run(
    f'git commit -m "{commit_msg}"'
)

run("git push")

print("GitHub push completed")