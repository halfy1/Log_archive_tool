import click
import os
import sys
from datetime import datetime
import tarfile

@click.group()
def cli():
    """Log Archive Tool — утилита для архивации логов"""
    pass

def write_log(message: str):
    os.makedirs("logs", exist_ok=True)
    human_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("logs/archive_log.txt", "a") as log_file:
        log_file.write(f"[{human_time}] {message}\n")

@cli.command()
@click.argument("indir", type=click.Path(exists=True, file_okay=False))
@click.option("-v", "--verbose", is_flag=True, help="Подробный вывод (печать каждого файла).")
@click.option("-i", "--ignore-permissions", is_flag=True, help="Пропускать файлы без доступа, не прерывая архивацию.")
def archive(indir, verbose, ignore_permissions):
    """Архивирует логи из указанной директории."""
    log_dir = os.path.abspath(indir)
    click.echo(f"Архивируем логи из директории: {log_dir}")

    files = []
    for root, _, filenames in os.walk(log_dir):
        for name in filenames:
            files.append(os.path.join(root, name))

    click.echo(f"Найдено файлов: {len(files)}")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_name = f"log_archive_{timestamp}.tar.gz"
    os.makedirs("archives", exist_ok=True)
    archive_path = os.path.join("archives", archive_name)

    click.echo(f"Имя архива: {archive_name}")
    click.echo(f"Путь до архива: {archive_path}")

    skipped = 0

    try:
        with tarfile.open(archive_path, "w:gz") as tar:
            if verbose:
                for fpath in files:
                    rel = os.path.relpath(fpath, start=os.path.dirname(log_dir))
                    try:
                        click.echo(f"[+] {fpath}")
                        tar.add(fpath, arcname=rel)
                    except PermissionError:
                        skipped += 1
                        msg = f"[!] Пропущен (нет доступа): {fpath}"
                        click.secho(msg, fg="yellow")
                        if not ignore_permissions:
                            raise
            else:
                with click.progressbar(files, label="Архивация", show_percent=True) as bar:
                    for fpath in bar:
                        rel = os.path.relpath(fpath, start=os.path.dirname(log_dir))
                        try:
                            tar.add(fpath, arcname=rel)
                        except PermissionError:
                            skipped += 1
                            if not ignore_permissions:
                                raise
    except PermissionError as e:
        click.secho(f"[Error] Permission denied: {e}", fg="red", err=True)
        sys.exit(1)

    write_log(f"[archive] Архив создан: {archive_path} из {log_dir}. Всего файлов: {len(files)}, пропущено: {skipped}")

@cli.command()
def history():
    log_file_path = "logs/archive_log.txt"
    if not os.path.exists(log_file_path):
        click.echo("История пуста")
        return
    with open(log_file_path, "r") as log_file:
        click.echo(log_file.read())

@cli.command()
@click.option("-v", "--verbose", is_flag=True, help="Подробный вывод")
def clean(verbose):
    archive_path = "archives"
    
    if not os.path.exists(archive_path):
        click.echo(f"Архивы отсутствуют")
        return
    
    removed_count = 0
    for entry in os.scandir(archive_path):
        if entry.is_file():
            try:
                os.remove(entry.path)
                removed_count +=1
                if verbose:
                    click.echo(f"Удалён: {entry.path}")
            except Exception as e:
                click.echo(f"Ошибка удаления файла {entry.path}: {e}", err=True)

    click.secho(f"Удалено архивов: {removed_count}", fg="green")

    write_log(f"[clean] Удалено архивов: {removed_count} из {archive_path}")

def main():
    cli()

if __name__ == "__main__":
    main()
