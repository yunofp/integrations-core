import logging
def configure_logging(app):

    log_format = '[%(asctime)s] [%(levelname)s] - %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'
    
    logging.basicConfig(level=logging.DEBUG,
                        format=log_format,
                        datefmt=date_format,
                        handlers=[
                            logging.StreamHandler(),
                            logging.FileHandler('app.log', mode='w')
                        ])

    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(logging.Formatter(fmt=log_format, datefmt=date_format))
    
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.DEBUG)
    
    file_handler = logging.FileHandler('app.log', mode='w')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(fmt=log_format, datefmt=date_format))
    
    app.logger.addHandler(file_handler)
    app.logger.info("Logging is configured.")