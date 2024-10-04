import schedule
import time, os
import typer
from zbackup import backup
import dotenv
import logging
import signal, sys
from pathlib import Path


def start_cli(path: str):
    folder = Path(path)
    if not folder.exists():
        raise FileNotFoundError(f"Path not found: {path}")
    if not folder.is_dir():
        raise ValueError(f"Path is not a directory: {path}")
    backup.backup_one_folder(folder)


def start_docker(now: bool = False):
    if now:
        backup.backup_all()
        return
    logging.info("Starting backup server ...")
    if "BACKUP_INTERVAL" not in os.environ:
        raise ValueError("BACKUP_INTERVAL environment variable is not set")
    intervals = os.environ["BACKUP_INTERVAL"].split(";")
    action = backup.backup_all
    for interval in intervals:
        interval = interval.strip()
        if interval.startswith("daily-"):
            time_str = interval.split("-")[1]
            schedule.every().day.at(time_str).do(action)
        else:
            raise ValueError(f"Invalid interval: {interval}")
    while True:
        n = max(schedule.idle_seconds() or 3600, 1)
        time.sleep(n)
        schedule.run_pending()


def terminate(signal, frame):
    sys.exit(0)


def main():
    # Setup logging and env
    signal.signal(signal.SIGTERM, terminate)
    logging.basicConfig(
        level=logging.INFO, format="[%(asctime)s %(levelname)s %(name)s] %(message)s"
    )
    dotenv.load_dotenv()
    # Start the server
    is_docker = os.environ.get("DOCKER", "false").lower() in ["true", "1"]
    if is_docker:
        typer.run(start_docker)
    else:
        typer.run(start_cli)


if __name__ == "__main__":
    main()
