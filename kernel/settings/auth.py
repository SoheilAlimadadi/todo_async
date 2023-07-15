from .base import config


SECRET_KEY = config.get_value('settings.auth', 'SECRET_KEY')
ALGORITHM = config.get_value('settings.auth', 'ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = config.get_value(
    'settings.auth', 'ACCESS_TOKEN_EXPIRE_MINUTES'
)
