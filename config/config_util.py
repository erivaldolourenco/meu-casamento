import os
import environ
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent



class ConfigUtil:
    env = environ.Env()

    @staticmethod
    def load_env(env_path=None):
        if env_path is None:
            env_path = os.path.join(BASE_DIR, 'config/.env')
        ConfigUtil.env.read_env(env_path)

    @staticmethod
    def get_secret_key():
        return ConfigUtil.env('SECRET_KEY', default='default-secret-key')

    @staticmethod
    def is_debug():
        return ConfigUtil.env.bool('DEBUG', default=False)

    @staticmethod
    def get_hosts():
        dominio = ConfigUtil.env('DOMINIO', default='0.0.0.0,localhost')
        return dominio

    @staticmethod
    def get_token_mercadopago():
        return ConfigUtil.env('TOKEN_MERCADO_PAGO', default='xxxxxxxxxxxxxxxxxx')
