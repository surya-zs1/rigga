import os
import subprocess
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.environ.get("BOT_TOKEN")

DOWNLOAD_DIR = "/downloads"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send /leech <url>")


async def leech(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = context.args[0]

    msg = await update.message.reply_text("Downloading...")

    cmd = ["aria2c", "-d", DOWNLOAD_DIR, url]
    subprocess.run(cmd)

    files = os.listdir(DOWNLOAD_DIR)

    if not files:
        await msg.edit_text("Download failed")
        return

    file_path = os.path.join(DOWNLOAD_DIR, files[0])

    await msg.edit_text("Uploading...")

    await update.message.reply_document(document=open(file_path, "rb"))

    os.remove(file_path)


async def ytdl(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = context.args[0]

    msg = await update.message.reply_text("Downloading video...")

    cmd = [
        "yt-dlp",
        "-o",
        f"{DOWNLOAD_DIR}/%(title)s.%(ext)s",
        url
    ]

    subprocess.run(cmd)

    files = os.listdir(DOWNLOAD_DIR)

    if not files:
        await msg.edit_text("Download failed")
        return

    file_path = os.path.join(DOWNLOAD_DIR, files[0])

    await msg.edit_text("Uploading...")

    await update.message.reply_document(document=open(file_path, "rb"))

    os.remove(file_path)


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("leech", leech))
app.add_handler(CommandHandler("yt", ytdl))

app.run_polling()
