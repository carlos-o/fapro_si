SII_URL = 'https://www.sii.cl/valores_y_fechas/uf/uf{}.htm'


MONTHS_YEAR = {"1": "enero", "2": "febrero", "3": "marzo", "4": "abril", "5": "mayo", "6": "junio", "7": "julio",
               "8": "agosto", "9": "septiembre", "10": "octubre", "11": "noviembre", "12": "diciembre"}

CACHE_TIME = 3600

# logger config
LOGGING_CONFIG = {
    'version': 1,
    'loggers': {
        '': {  # root logger
            'level': 'NOTSET',
            'handlers': ['debug_console_handler'],
        }
    },
    'handlers': {
        'debug_console_handler': {
            'level': 'DEBUG',
            'formatter': 'info',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
        }
    },
    'formatters': {
        'info': {
            'format': '%(asctime)s-%(levelname)s-%(name)s::%(module)s|%(lineno)s:: %(message)s'
        },
        'error': {
            'format': '%(asctime)s-%(levelname)s-%(name)s-%(process)d::%(module)s|%(lineno)s:: %(message)s'
        },
    },
}