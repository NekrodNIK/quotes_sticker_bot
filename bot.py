from pathlib import PurePath, Path

from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
import tomllib


async def gen_sticker(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')


try:
    config_raw_toml = Path(PurePath(__file__).parent, "settings.toml").read_text()
except FileNotFoundError:
    exit(f"Config file settings.toml not found in {Path(PurePath(__file__).parent)}")

config_options = tomllib.loads(config_raw_toml)

bot_token = config_options.get("TG_BOT_TOKEN")

if bot_token is None:
    exit("TG_BOT_TOKEN not set in settings.toml")

app = ApplicationBuilder().token(bot_token).build()

app.add_handler(MessageHandler(filters=filters.TEXT,
                               callback=gen_sticker))

app.run_polling()
