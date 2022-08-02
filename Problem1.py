import csv
import psutil
import platform
import threading

from pathlib import Path


def write_result(system: str, data: dict):
    file_name = f'log_{system}.csv'
    if Path(file_name).is_file():
        file = open(file_name, 'a')
        writer = csv.writer(file)
    else:
        file = open(file_name, 'w')
        writer = csv.writer(file)
        writer.writerow(data.keys())

    writer.writerow(data.values())
    file.close()


def windows():
    """ Method to log WINDOWS system log

    """
    memory = psutil.Process().memory_info()
    write_result(
        'windows',
        {
            'cpu': psutil.cpu_percent(),
            'wset': memory.wset,
            'vms': memory.vms,
            'open_handles': len(psutil.pids())
        }
    )


def linux():
    """ Method to log LINUX system log

    """
    memory = psutil.Process().memory_info()
    write_result(
        'linux',
        {
            'cpu': psutil.cpu_percent(),
            'rss': memory.rss,
            'vms': memory.vms,
            'open_handles': len(psutil.pids())
        }
    )


def incorrect_platform():
    """ Raise exception if system is not supported

    """
    raise Exception('Incorrect system')


def log_data(interval: int):
    """ Log system data

    :param interval: int

    """
    threading.Timer(interval, log_data, [interval]).start()

    globals().get(platform.system().lower(), incorrect_platform)()


if __name__ == '__main__':
    interval = 60  # 1 min
    log_data(interval)
