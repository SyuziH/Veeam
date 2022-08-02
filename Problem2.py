import logging
import threading

from pathlib import Path
from dirsync import sync
from argparse import ArgumentParser


def start(interval: int, source: str, target: str, logger: object):
    """ Start synchronization process

    :param interval: int
    :param source: str
    :param target: str
    :param logger: object

    """
    threading.Timer(interval, start, [interval, source, target, logger]).start()

    sync(source, target, 'sync', logger=logger)


if __name__ == '__main__':
    cmd_parser = ArgumentParser(description='Synchronization script')

    cmd_parser.add_argument(
        '-s',
        '--source',
        help='Source directory',
        type=lambda path: path if Path(path).is_dir() else cmd_parser.error(
            'The source directory "{}" does not exist'.format(path))
    )
    cmd_parser.add_argument(
        '-r',
        '--replica',
        help='Replica directory',
        type=lambda path: path if Path(path).is_dir() else cmd_parser.error(
            'The replica directory "{}" does not exist'.format(path))
    )
    cmd_parser.add_argument(
        '-l',
        '--log',
        help='Log file path'
    )
    cmd_parser.add_argument(
        '-i',
        '--interval',
        help='Synchronization interval'
    )
    cmd_args = cmd_parser.parse_args()
    print(cmd_args)

    # Logger Initialization
    logging.basicConfig(filename=cmd_args.log, level=logging.DEBUG)
    logger = logging.getLogger('dirsync')

    start(
        int(cmd_args.interval),
        cmd_args.source,
        cmd_args.replica,
        logger
    )

# For running code: python3 Problem2.py -s source/ -r repl/ -l logg.log -i 6
