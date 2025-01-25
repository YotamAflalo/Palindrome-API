import logging
from pathlib import Path
from datetime import datetime
from pathlib import Path
from config.config import log_mode
import sys
import os
project_root = str(Path(__file__).parent)

class Logger:
    """
    Singleton logger class that handles both file logging and CloudWatch logging.
    Creates a new log file daily in the logs directory.
    """

    def __init__(self,log_mode='DEBUG'):
        # Create logs directory if it doesn't exist
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        # Create logger
        self.logger = logging.getLogger("palindrom api")
        self.logger.setLevel(log_mode)
        
        # Create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        # Create file handler
        current_time = datetime.now().strftime("%Y%m%d")
        file_handler = logging.FileHandler(os.path.join(project_root, "logs", f"palindrom_api_{current_time}.log"))
        file_handler.setFormatter(formatter)
        
        # Add handler to logger
        self.logger.addHandler(file_handler)
    def getLogger(self):
        return self.logger
    def debug(self, message: str) -> None:
         """Log debug level message."""
         self.logger.debug(message)
    def info(self, message: str) -> None:
         """Log info level message."""
         self.logger.info(message)
    def eror(self, message: str) -> None:
         """Log error level message."""
         self.logger.error(message)

# Create a singleton instance
logger = Logger(log_mode=log_mode)#.getLogger()
