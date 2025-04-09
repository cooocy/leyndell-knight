import os

from tools import logger
from config import oss_helper_cfs

dir_name = os.path.dirname(__file__)
logger_filename = f"{dir_name}/{oss_helper_cfs['log']}"
mine_logger = logger.Logger(logger_filename)

__all__ = ['mine_logger', 'logger_filename']
