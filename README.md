# monitoring-notifier-bot

App sends notifications to telegram upon reaching 90% or above disk usage on host <br> 
And sends notifications about resolving such usage

## How to install

### Requirements

#### Linux

* Python 3+
* SQLite 3

### Setting up local environment

* Copy `.env.dist` contents to `.env` and set your environment variables.
* Install requirements from file, like so: `pip install -r requirements.txt`
* Create logs folder if not exists already, example: `mkdir logs`
* Create and initialize database, example: 
    * `sqlite3 monitoring.db`
    * `python3 -c "from modules.database import Executor; Executor().create_table()"`
* Run `python3 core.py` from project root

## Configuration

### Run as a service:

If `/root/monitoring_notifier` is project root, then

* Create service config file, example `/lib/systemd/system/monitoring-notifier.service`:

    ```
    [Unit]
    Description=Monitoring Notifier Service
    After=multi-user.target
    Conflicts=getty@tty1.service

    [Service]
    Type=simple
    ExecStart=/usr/bin/python3 /root/monitoring_notifier/core.py
    StandardInput=tty-force

    [Install]
    WantedBy=multi-user.target
    ```
* Reload daemon to apply changes: `sudo systemctl daemon-reload`
* Enable service by running: `sudo systemctl enable monitoring-notifier.service`
* Start service: `sudo systemctl start monitoring-notifier.service` 

### Environment variables

* `HOST` _(string)_ - desired hostname for telegram message and database records
* `CHAT_ID` _(string)_ - id of telegram chat or channel
* `BOT_TOKEN` _(string)_ - telegram bot token
* `DB_PATH` _(string)_ - path to sqlite3 database
* `LOG_PATH` _(string)_ - path to notifier log life
* `LOCATION` _(string)_ - path to scan for large files
