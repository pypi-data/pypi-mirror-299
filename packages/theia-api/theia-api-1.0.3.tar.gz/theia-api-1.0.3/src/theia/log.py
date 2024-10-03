import logging
import sys
from loguru import logger
from pydantic_settings import BaseSettings


def log_init(config: BaseSettings) -> logger:

    # intercept everything at the root logger
    logging.root.handlers = [InterceptHandler()]
    logging.root.setLevel(config.log_level)

    # remove every other logger's handlers
    # and propagate to root logger
    for name in logging.root.manager.loggerDict.keys():
        logging.getLogger(name).handlers = []
        logging.getLogger(name).propagate = True

    handlers = []

    if config.debug:
        import sys
        handlers.append({"sink": sys.stdout})

    handlers.append({"sink": config.log_path, "rotation": "00:00",
                     "retention": config.log_retention, "compression": "gz", "enqueue": config.log_async})

    # configure loguru
    logger.configure(handlers=handlers)

    return logger


class InterceptHandler(logging.Handler):

    def emit(self, record):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())

