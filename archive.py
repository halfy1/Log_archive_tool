import argparse
import os
import sys
from datetime import datetime
import tarfile

parser = argparse.ArgumentParser(description="Log archive tool")
parser.add_argument("indir", help="directory to logs")
args = parser.parse_args()

log_dir = args.indir
print(f"Архивируем логи из директории: {log_dir}")

if not os.path.isdir(log_dir):
    print(f"[Error] Директории {log_dir} не существует")
    sys.exit(1)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
archive_name = f"log_archive_{timestamp}.tar.gz"
archive_path = os.path.join("archives", archive_name)

print(f"Имя архива {archive_name}")
print(f"Путь для архива {archive_path}")

os.makedirs("archives", exist_ok=True)

with tarfile.open(archive_path, "w:gz") as tar:
    tar.add(log_dir, arcname=os.path.basename(log_dir))

os.makedirs("logs", exist_ok=True)

human_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
log_line = f"[{human_time}] Архив создан: {archive_path} из {log_dir}\n"

with open("logs/archive_log.txt", "a") as log_file:
    log_file.write(log_line)

