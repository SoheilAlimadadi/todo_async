from .base import config


DATABASE_URL = config.get_value('settings.mongodb', 'DATABASE_URL')
