from zbackup.gcs import BUCKET
import io
from datetime import datetime, timezone
from pathlib import Path
import tarfile
from dataclasses import dataclass
import os
import logging


def upload(name: str, data: io.BytesIO, meta: dict[str, str]):
    blob = BUCKET.blob(name, chunk_size=16 * 1024 * 1024)
    if blob.exists():
        raise FileExistsError(f"File {name} already exists")
    blob.upload_from_file(data)
    blob.patch()
    blob.metadata = meta
    blob.patch()
    return blob.id


POSSIBLE_BACKUP_DIRS = [
    "/backup",
    "/backups",
    "./backup",
    "./backups",
    "./_backup",
    "./_backups",
]


@dataclass
class SystemInfo:
    scope: str | None

    @staticmethod
    def get() -> "SystemInfo":
        scope = os.environ.get("SCOPE")
        return SystemInfo(scope=scope)

    def get_scope(self) -> str | None:
        return self.scope

    def get_backup_dir(self) -> Path | None:
        for backup_dir in POSSIBLE_BACKUP_DIRS:
            if os.path.exists(backup_dir):
                return Path(backup_dir)
        return None


def backup_all():
    try:
        sys_info = SystemInfo.get()
        folder = sys_info.get_backup_dir()
        if folder is None:
            logging.error("No backup folder found")
            return
        date = datetime.now(timezone.utc).isoformat()
        for path in folder.iterdir():
            if not path.is_dir():
                continue
            __do_backup(sys_info, date, path)
    except Exception as e:
        logging.error(e)


def backup_one_folder(folder: Path):
    try:
        sys_info = SystemInfo.get()
        date = datetime.now(timezone.utc).isoformat()
        __do_backup(sys_info, date, folder)
    except Exception as e:
        logging.error(e)


def __do_backup(sysinfo: SystemInfo, date: str, path: Path) -> bool:
    try:
        project_name = path.name
        data = io.BytesIO()
        with tarfile.open(fileobj=data, mode="w:gz") as tar:
            tar.add(path, arcname=project_name)
        data.seek(0)
        if scope := sysinfo.get_scope():
            meta = {"scope": scope}
            target = f"{project_name}/{scope}/{date}.tar.gz"
        else:
            meta = {}
            target = f"{project_name}/{date}.tar.gz"
        file_id = upload(target, data, meta)
        logging.info(f"✔ Uploaded {file_id}")
        return True
    except Exception as e:
        logging.error(e)
        return False
