from service.logger_settings import config

config['loggers'] = {
    'Finder': {
        'handlers': ['consoleHandler', 'fileHandler'],
        'level': 'DEBUG',
        'propagate': False
    }
}
