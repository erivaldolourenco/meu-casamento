import telepot

from config.config_util import ConfigUtil

ConfigUtil.load_env()

BOT_TELEGRAM_TOKEN = ConfigUtil.get_token_telegram()
PESSOAL_TELEGRAM_ID = ConfigUtil.get_pessoa_telegram()
bot = telepot.Bot(BOT_TELEGRAM_TOKEN)

def enviar_telegram(mensagem):
    bot.sendMessage(PESSOAL_TELEGRAM_ID, mensagem)