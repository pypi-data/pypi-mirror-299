import os
from google.cloud.storage import Client
import dotenv, json

dotenv.load_dotenv()

if os.environ.get("GOOGLE_APPLICATION_CREDENTIALS") is None:
    # Find a credentials file
    # 1. current directory
    _possible_creds = ["./creds.json", "./.creds.json"]
    # 2. home directory
    if home := os.environ.get("HOME"):
        _possible_creds += [
            f"{home}/creds.json",
            f"{home}/.creds.json",
            f"{home}/.config/z-backup/creds.json",
            f"{home}/.config/z-backup/.creds.json",
        ]
    # 3. root directory (for docker container)
    _possible_creds += ["/creds.json", "/.creds.json"]
    for creds in _possible_creds:
        if os.path.exists(creds):
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = creds
            break
    else:
        raise FileNotFoundError("No credentials file found")

_client = Client()

_creds_file = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]

if b := os.environ.get("BUCKET"):
    bucket_name = b
else:
    with open(_creds_file) as f:
        _creds = json.load(f)
        bucket_name = _creds.get("bucket", "archive-z")

BUCKET = _client.get_bucket(bucket_name)
