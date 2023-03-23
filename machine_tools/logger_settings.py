from service.logger_settings import config

config['loggers'] = {
    'MachineToolsFinder': {
        'handlers': ['consoleHandler', 'fileHandler'],
        'level': 'CRITICAL',
        'propagate': False
    },
    'MachineToolsCreator': {
        'handlers': ['consoleHandler', 'fileHandler'],
        'level': 'ERROR',
        'propagate': False
    }
}
