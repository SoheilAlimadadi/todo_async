from kernel.settings.logging import setup_logging




if __name__ == '__main__':
    import logging
    setup_logging()
    coreLogger = logging.getLogger('core')
    coreLogger.info('hello')