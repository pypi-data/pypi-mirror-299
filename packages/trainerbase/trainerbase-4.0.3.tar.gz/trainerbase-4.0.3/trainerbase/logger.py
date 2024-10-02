from logging import ERROR, getLogger
from logging.config import dictConfig

from trainerbase.config import CONFIG_FILE, logging_config


if logging_config is None:
    logging_config = {
        "version": 1,
        "disable_existing_loggers": True,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] <%(levelname)s> %(funcName)s: %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            }
        },
        "handlers": {
            "console": {
                "formatter": "default",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
            }
        },
        "root": {
            "level": "INFO",
            "handlers": ["console"],
        },
    }
    display_no_logger_config_warning = True
else:
    display_no_logger_config_warning = False


dictConfig(logging_config)
getLogger("comtypes").setLevel(ERROR)

logger = getLogger("TrainerBase")

if display_no_logger_config_warning:
    logger.warning(f"No logging config in {CONFIG_FILE}! Use updated trainer template.")
