from io import BytesIO
from pathlib import PurePath, Path

from PIL import ImageFont
from telegram import Update, Sticker
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
import tomllib
from PIL import Image
from PIL.ImageDraw import Draw

STICKER_HEIGHT = 512


async def gen_sticker(update: Update, _) -> None:
    sticker_weight = 1000
    sticker_image = Image.new(mode="RGBA", size=(1000, STICKER_HEIGHT))

    if update.message.forward_from is None:
        user_id = update.message.from_user.id
    else:
        user_id = update.message.forward_from.id

    avatar_bytes_io = BytesIO()

    await (await update.get_bot().get_file(
        (await update.get_bot().get_user_profile_photos(user_id)).photos[0][0].file_id
    )).download_to_memory(avatar_bytes_io)

    avatar_image = Image.open(avatar_bytes_io)
    sticker_image.paste(avatar_image, (0, 0, avatar_image.size[0], avatar_image.size[1]))

    sticker_output_bytes_io = BytesIO()
    sticker_image.save(sticker_output_bytes_io, format="PNG")
    sticker_output_bytes_io.seek(0)

    await update.message.reply_sticker(sticker=sticker_output_bytes_io)


try:
    config_raw_toml = Path(PurePath(__file__).parent, "settings.toml").read_text()
except FileNotFoundError:
    exit(f"Config file settings.toml not found in {Path(PurePath(__file__).parent)}")

config_options = tomllib.loads(config_raw_toml)

bot_token = config_options.get("TG_BOT_TOKEN")

if bot_token is None:
    exit("TG_BOT_TOKEN not set in settings.toml")

app = ApplicationBuilder().token(bot_token).build()

app.add_handler(MessageHandler(filters=filters.TEXT & ~ filters.FORWARDED,
                               callback=gen_sticker))

app.run_polling()
