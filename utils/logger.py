import logging
import sys
import os

def setup_logger(name=__name__, log_file='automation.log'):
    """
    Configures a logger to output to both console and a file.
    """
    logger = logging.getLogger(name)
    
    # Avoid adding handlers multiple times if logger is already configured
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        
        # Format: Time - Level - Message
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        
        # Console Handler (Stdout)
        ch = logging.StreamHandler(sys.stdout)
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        
        # File Handler
        fh = logging.FileHandler(log_file)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        
    return logger
