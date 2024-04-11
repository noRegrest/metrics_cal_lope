import logging
from colorlog import ColoredFormatter

# Set up logging with a colored formatter
formatter = ColoredFormatter(
    "[%(asctime)s] [%(log_color)s%(levelname)-s%(reset)s]: %(message)s",
    datefmt='%Y-%m-%d %H:%M:%S',
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red,bg_white',
    }
)

handler = logging.StreamHandler()
handler.setFormatter(formatter)

logger = logging.getLogger()
logger.addHandler(handler)
logger.setLevel(logging.INFO)
