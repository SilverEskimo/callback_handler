import sys
import logging

logger = logging.getLogger("callback_handler")
logger.setLevel(logging.DEBUG)

stdout_handler = logging.StreamHandler(stream=sys.stdout)
err_handler = logging.FileHandler("log/error.log")

stdout_handler.setLevel(logging.DEBUG)
err_handler.setLevel(logging.ERROR)

formatter = logging.Formatter(
    "%(name)s: %(asctime)s | %(filename)s:%(lineno)d | %(levelname)s: %(message)s"
)

stdout_handler.setFormatter(formatter)
err_handler.setFormatter(formatter)

logger.addHandler(stdout_handler)
logger.addHandler(err_handler)