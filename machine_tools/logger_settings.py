from service.logger_settings import config

config['loggers'] = {
    'Finder': {
        'handlers': ['consoleHandler', 'fileHandler'],
        'level': 'CRITICAL',
        'propagate': False
    },
    'Creator': {
        'handlers': ['consoleHandler', 'fileHandler'],
        'level': 'ERROR',
        'propagate': False
    }
}
