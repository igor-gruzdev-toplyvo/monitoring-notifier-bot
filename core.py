from modules.collector import Collector
from modules.notifier import Notifier
from modules.database import Executor
from dotenv import load_dotenv
from datetime import datetime
from os import environ
from time import sleep

load_dotenv()

host = environ.get("HOST")
location = environ.get("LOCATION")
total, used, free, usage_percentage = Collector().fetch_disk_usage(host)
log_file = "./var/logs/notifier.log"


def monitoring_reporter():
    alert_status = False
    telegram_message = None

    def __filelist_generator():
        file_list = []

        for file in Collector().fetch_large_files(location, 5):
            file_list.append(file)

        return file_list

    def __write_log(message):
        current_date = datetime.date(datetime.now())
        current_time = datetime.time(datetime.now()).strftime("%H:%M:%S")

        log = open(log_file, "a")
        log.write(f"[{current_date} {current_time}] {message}")
        log.close()

    def __parse_list():
        return "\n".join(map(str, __filelist_generator()))

    def __send_notification():
        try:
            Notifier().send_notification(telegram_message)
            __write_log("Message was sent\n")
        except Exception as exc:
            __write_log(f"Something went wrong during message delivery: {str(exc)}\n")

    while True:
        if all(item >= 90 for item in Executor().select_period()) and not alert_status:
            alert_status = True
            telegram_message = (
                f"*{host}* disk usage is CRITICAL: *{usage_percentage}%*"
                f"```\n\n"
                f"Total | {total}\n"
                f"Used  | {used}\n"
                f"Free  | {free}\n\n"
                f"```"
                f"List of largest files in *{location}:*"
                f"```\n\n"
                f"{__parse_list()}"
                f"```"
            )

            __send_notification()
            sleep(60)

        elif alert_status and Executor().select_period()[-1] < 90:
            alert_status = False
            telegram_message = (
                f"*{host}* disk usage was RESOLVED: *{usage_percentage}%*"
                f"```\n\n"
                f"Total | {total}\n"
                f"Used  | {used}\n"
                f"Free  | {free}\n\n"
                f"```"
            )

            __send_notification()
            sleep(60)

        else:
            Executor().write_entry(host, usage_percentage)
            __filelist_generator()
            sleep(60)

        continue


monitoring_reporter()
