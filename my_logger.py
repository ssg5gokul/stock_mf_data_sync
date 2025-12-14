import logging

# logger_name = __file__.split("\\")[-1].split(".")[0]

#Configure custom logger
def config_logger(name: str, level = logging.DEBUG, fname = "my_app.log"):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    if not logger.handlers:
        file_handler = logging.FileHandler(fname, encoding="utf-8")
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    logger.propagate = False
    return logger