import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

from data.config import PATH_LOGS

formatter = logging.Formatter('%(filename)-15s %(name)-8s LINE:%(lineno)-4d '
                              f'%(levelname)-8s [%(asctime)s] >  %(message)s')


def create_logger(name, logger='', level=logging.INFO, console=True):
    Path(PATH_LOGS).mkdir(parents=True, exist_ok=True)

    handler = logging.handlers.TimedRotatingFileHandler(
        filename=f'{PATH_LOGS}/{name}.log', when='W0'
    )
    handler.setFormatter(formatter)

    logger = logging.getLogger(logger)
    logger.setLevel(level)

    logger.addHandler(handler)

    if console:
        console_out = logging.StreamHandler()
        console_out.setFormatter(formatter)
        logger.addHandler(console_out)

    return logger


bot_log = create_logger('alerts_bot', 'alerts_bot')
