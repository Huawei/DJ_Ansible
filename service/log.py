import logging
import logging.handlers
import os


def _get_log_file_path(conf, logfile):
    logdir = conf['LOGGING']['path']

    if logfile and not logdir:
        return logfile

    if logfile and logdir:
        return os.path.join(logdir, logfile)

    return None


def _set_up_logging_from_conf(conf, service_name):
    log_root = logging.getLogger()

    # Remove all handlers
    for handler in list(log_root.handlers):
        log_root.removeHandler(handler)

    logpath = _get_log_file_path(conf, service_name + ".log")
    if logpath:
        file_handler = logging.handlers.RotatingFileHandler
        max_bytes = 50 * 1024 ** 2  # 20M
        filelog = file_handler(logpath,
                               maxBytes=max_bytes,
                               backupCount=5)
        log_root.addHandler(filelog)

    # user stdout
    log_root.addHandler(logging.StreamHandler())

    for handler in log_root.handlers:
        handler.setFormatter(logging.Formatter(
            fmt=conf['LOGGING']['format'],
            datefmt=conf['LOGGING']['datefmt']))

    log_root.setLevel(conf['LOGGING']['level'])


def setup(conf, service_name):
    _set_up_logging_from_conf(conf, service_name)
