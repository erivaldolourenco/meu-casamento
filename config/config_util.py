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

    @staticmethod
    def get_token_telegram():
        return ConfigUtil.env('BOT_TELEGRAM_TOKEN', default='xxxxxxxxxxxxxxxxxx')

    @staticmethod
    def get_pessoa_telegram():
        return ConfigUtil.env('PESSOAL_TELEGRAM_ID', default='xxxxxxxxxxxxxxxxxx')

    @staticmethod
    def get_db_name():
        return ConfigUtil.env('DATABASE_NAME', default='database')

    @staticmethod
    def get_db_user():
        return ConfigUtil.env('DATABASE_USER', default='user')

    @staticmethod
    def get_db_password():
        return ConfigUtil.env('DATABASE_PASSWORD', default='password')

    @staticmethod
    def get_db_host():
        return ConfigUtil.env('DATABASE_HOST', default='localhost')

    @staticmethod
    def get_port():
        return ConfigUtil.env('DATABASE_PORT', default='3306')

    @staticmethod
    def get_csrf_trusted():
        return ConfigUtil.env('CSRF_TRUSTED_ORIGINS', default='3306')
