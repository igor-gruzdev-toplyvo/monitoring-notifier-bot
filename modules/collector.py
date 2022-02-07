from hurry.filesize import size
from .database import Executor
import shutil
import os


class Collector:
    """Parsing health check responces
    for telegram bot messages
    """

    def __init__(self) -> None:
        self.total, self.used, self.free = shutil.disk_usage("/")

    def fetch_disk_usage(self, hostname):
        total = size(self.total)
        used = size(self.used)
        free = size(self.free)
        usage_percentage = round(self.used / (self.total / 100))
        Executor().write_entry(hostname, usage_percentage)
        return total, used, free, usage_percentage

    def fetch_large_files(self, location, filesize):
        for folder, subfolders, filenames in os.walk(location):
            for filename in filenames:
                try:
                    size_bytes = os.path.getsize(os.path.join(folder, filename))
                    size_text = "{}/{} -> {}".format(folder, filename, size(size_bytes))
                    if filesize * 1024 * 1024 ** 2 <= size_bytes:
                        yield size_text
                except FileNotFoundError:
                    pass
