import os 
import logging

APP_DIR = os.path.abspath(os.path.dirname(__file__))
os.getenv('APP_DIR',APP_DIR)
logging.info(os.getenv('APP_DIR'))
LOG_DIR = os.path.join(APP_DIR,'logs')
os.getenv('LOGS_DIR',LOG_DIR)
logging.info(os.getenv('LOG_DIR'))
TEST_DIR = os.path.join(APP_DIR,'test')
os.getenv('TEST_DIR',TEST_DIR)
logging.info(os.getenv('TEST_DIR'))
MAIN_DIR = os.path.join(APP_DIR,'main')
os.getenv('MAIN_DIR',MAIN_DIR)
logging.info(os.getenv('MAIN_DIR'))
DATA_DIR = os.path.join(APP_DIR,'data')
os.getenv('DATA_DIR',DATA_DIR)
logging.info(os.getenv('DATA_DIR'))