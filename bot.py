import os
import asyncio

from telegram import Update,InlineKeyboardButton,InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder,CommandHandler,CallbackQueryHandler,ContextTypes

from downloader import get_formats,download_video
from database import get_cached,save_cache
from utils import progress_bar


TOKEN=os.environ["BOT_TOKEN"]

DOWNLOAD_DIR="/downloads"

user_links={}
cancel_flags={}


async def start(update:Update,context:ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "Use /yt <url> to download video"
    )


async def yt(update:Update,context:ContextTypes.DEFAULT_TYPE):

    url=context.args[0]

    cached=await get_cached(url)

    if cached:

        await update.message.reply_document(cached["file_id"])
        return

    formats=get_formats(url)

    buttons=[]

    for f in formats:

        buttons.append([
            InlineKeyboardButton(
                f["res"],
                callback_data=f"format|{f['id']}"
            )
        ])

    user_links[update.effective_user.id]=url

    await update.message.reply_text(
        "Select resolution",
        reply_markup=InlineKeyboardMarkup(buttons)
    )


async def button(update:Update,context:ContextTypes.DEFAULT_TYPE):

    query=update.callback_query
    await query.answer()

    data=query.data

    if data=="cancel":

        cancel_flags[query.from_user.id]=True

        await query.message.edit_text("Download cancelled")

        return


    if data.startswith("format"):

        format_id=data.split("|")[1]

        user_id=query.from_user.id

        url=user_links[user_id]

        msg=await query.message.reply_text("Starting download...")


        cancel_flags[user_id]=False

        loop=asyncio.get_event_loop()


        def progress(percent,speed,eta):

            if cancel_flags.get(user_id):

                raise Exception("Cancelled")

            text=f"""
Downloading

{progress_bar(percent)}

Speed: {speed}
ETA: {eta}
"""

            asyncio.run_coroutine_threadsafe(
                msg.edit_text(
                    text,
                    reply_markup=InlineKeyboardMarkup(
                        [[InlineKeyboardButton("Cancel","cancel")]]
                    )
                ),
                loop
            )


        try:

            await loop.run_in_executor(
                None,
                download_video,
                url,
                format_id,
                progress
            )

        except:

            return


        file=os.listdir(DOWNLOAD_DIR)[0]

        path=os.path.join(DOWNLOAD_DIR,file)

        sent=await query.message.reply_document(open(path,"rb"))

        await save_cache(url,sent.document.file_id)

        os.remove(path)

        await msg.delete()


app=ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start",start))
app.add_handler(CommandHandler("yt",yt))
app.add_handler(CallbackQueryHandler(button))

app.run_polling()
