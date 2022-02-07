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
log_file = environ.get("LOG_PATH")


def monitoring_reporter():
    alert_status = False
    telegram_message = None

    def __filelist_generator():
        file_list = []

        for file in Collector().fetch_large_files(location, 2):
            file_list.append(file)

        return file_list

    def __write_log(message):
        current_date = datetime.date(datetime.now())
        current_time = datetime.time(datetime.now()).strftime("%H:%M:%S")

        log = open(log_file, "a")
        log.write("[{} {}] {}".format(current_date, current_time, message))
        log.close()

    def __parse_list():
        return "\n".join(map(str, __filelist_generator()))

    def __send_notification():
        try:
            Notifier().send_notification(telegram_message)
            __write_log("Message was sent\n")
        except Exception as exc:
            __write_log(
                "Something went wrong during message delivery: {}\n".format(str(exc))
            )

    while True:
        total, used, free, usage_percentage = Collector().fetch_disk_usage(host)

        if all(item >= 90 for item in Executor().select_period()) and not alert_status:
            alert_status = True
            message = """
                *{}* disk usage is CRITICAL: *{}%*\n
                ```
                Total | {}
                Used  | {}
                Free  | {}
                ```
                List of largest files in *{}:*\n
                ```
                {}
                ```
                """.format(
                host, usage_percentage, total, used, free, location, __parse_list()
            )
            telegram_message = "\n".join([m.lstrip() for m in message.split("\n")])

            __send_notification()
            sleep(60)

        elif alert_status and Executor().select_period()[-1] < 90:
            alert_status = False
            message = """
                *{}* disk usage was RESOLVED: *{}%*\n
                ```
                Total | {}
                Used  | {}
                Free  | {}
                ```""".format(
                host, usage_percentage, total, used, free
            )
            telegram_message = "\n".join([m.lstrip() for m in message.split("\n")])

            __send_notification()
            sleep(60)

        else:
            sleep(60)

        continue


monitoring_reporter()
