from environs import Env


env = Env()
env.read_env(path='.env_alerts')

ADMINS_IDS = env.list('ADMINS_IDS')

MAX_LEN_MESSAGE = 4095  # 4096

PATH_LOGS = 'logs'

BOT_CONFIG = {
    'token': env.str('BOT_TOKEN'),
    'channel': env.str('BOT_CHANNEL', default=None)
}

FILE_CONFIG = {
    'path': env.str('FILE_PATH'),
}


PYROGRAM_CONFIG = {
    'api_id': env.str('API_ID'),
    'api_hash': env.str('API_HASH'),
}
