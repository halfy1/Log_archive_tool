import click
import os
import sys
from datetime import datetime
import tarfile

@click.group()
def cli():
    """Log Archive Tool - утилита для архивации логов"""
    pass

@cli.command()
@click.argument("indir", type=click.Path(exists=True, file_okay=False))
def archive(indir):
    """Logs from path"""
    log_dir = os.path.abspath(indir)
    click.echo(f"Архивируем логи из директории: {indir}")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_name=f"log_archive_{timestamp}.tar.gz"
    os.makedirs("archives", exist_ok=True)
    archive_path = os.path.join("archives", archive_name)

    click.echo(f"Имя архива: {archive_name}")
    click.echo(f"Путь до архива: {archive_path}")

    try:
        with tarfile.open(archive_path, "w:gz") as tar:
            tar.add(log_dir, arcname=os.path.basename(log_dir))
    except PermissionError as e:
        click.secho(f"[Error] Permission Denied: {e}", fg="red", err=True)
        sys.exit(1)
    
    os.makedirs("logs", exist_ok=True)
    human_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{human_time}] Архив создан : {archive_path} из {log_dir}\n"
    with open("logs/archive_log.txt", "a") as log_file:
        log_file.write(log_line)

    click.secho("Архивация завершена!", fg="green")

@cli.command()
def history():
    log_file_path = "logs/archive_log.txt"
    if not os.path.exists(log_file_path):
        click.echo("История пуста")
        return
    with open(log_file_path, "r") as log_file:
        click.echo(log_file.read())

def main():
    cli()

if __name__ == "__main__":
    main()