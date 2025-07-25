# Log Archive Tool  
  
**Log Archive Tool** — это утилита командной строки на Python, предназначенная для архивации логов по пути, заданному пользователем.  
  
## Возможности

- Запускается как команда `log-archive`.
- Поддерживает команды:
  - `archive <путь>` — архивирует содержимое указанной директории в `.tar.gz`.
  - `history` — показывает историю архиваций из `logs/archive_log.txt`.
- Архивы сохраняются в поддиректорию `archives/`.
- Имена архивов формируются по шаблону: `log_archive_ГГГГММДД_ЧЧММСС.tar.gz`.
- Записывает дату и время каждой архивации в лог-файл `logs/archive_log.txt`.

  
## Установка и запуск

### 1. Клонируйте репозиторий

```bash
git clone git@github.com:yourusername/log-archive-tool.git
cd log-archive-tool
```

### 2. Установите модуль `venv`

```bash
sudo apt install python3-venv
```

### 3. Создайте и активируйте виртуальное окружение

```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Установите утилиту в режиме разработки
```bash
pip install -e .
```

### После устновки утилита будет доступна
```bash
log-archive archive /путь/к/логам
# Показать историю архиваций:
log-archive history
```

## Расширенные возможности CLI

- Архивация с прогрессом
  По умолчанию команда `archive` показывает прогресс-бар по количеству файлов
- Подробный режим --verbose | -v
  ```bash
  log-archive archive /path/to/logs -v  
  ```
- Игнорирование ошибок доступа --ignore-permissions | -i
  Если в директории есть файлы, к которым нет прав чтения, можно пропустить их без прерывания архивации:
  ```bash
  log-archive archive /var/log -i
  ```

## Установка systemd-сервиса для автоматической архивации
### 1. Перенесите файлы
```bash
mv log-archiver.service /etc/systemd/systemd/
mv log-archiver.timer /etc/systemd/systemd/
```
### 2. Отредактируйте log-archiver.service
Откройте и подставьте:
`WorkingDirectory` — путь до директории с проектом
`ExecStart` — путь до CLI-утилиты log-archive в venv/bin
Аргумент `/path/to/your/logs` — путь до папки с логами
### 3. Перезапустите systemd и включите таймер
```bash
sudo systemctl daemon-reload
sudo systemctl enable --now log-archiver.timer
```

## Что  можно сделать  
- [ ] Отправка архива на удалённый сервер или в облако (например, через SFTP или AWS S3)
- [ ] Автоматическая очистка старых архивов  
- [x] Поддержка расписания (через cron или встроенно)    
- [x] Вывод прогресса архивации (--verbose)  
- [x] Cli работа 
