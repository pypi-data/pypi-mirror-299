# Auto Backup Service

# Use as a docker compose service

Add the following to your compose.yml:

```yaml
services:
  # Other services...
  backup:
    image: wenyuzhao/backup:latest
    container_name: my-backup
    restart: always
    volumes:
      - ./path/to/your/data/folder:/backup/example
      - ./.creds.json:/.creds.json # Google cloud service account key file
    environment:
      - BACKUP_INTERVAL=daily-17:00 # Daily at 3:00 AM AEST
      - BUCKET=your-bucket-name # Alternatively, add a "bucket" field to .creds.json
```

_To trigger backup once immediately, run `docker compose run backup now`._

# Use as a command-line tool for one-time backup

Make sure there is a `creds.json` or `.creds.json` under either `$PWD` or `$HOME/.config/z-backup`

1. Install the executable: `pipx install z-backup`
2. Run `z-backup ./path/to/your/data/folder`

# Push New Image

```bash
docker buildx build --push --platform linux/arm64,linux/amd64 --tag wenyuzhao/backup:latest .
```