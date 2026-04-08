import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
import yt_dlp
from pydub import AudioSegment

# إعداد السجلات
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TOKEN = '8785291349:AAEPeEGhgCKkUIKYkOt-xg53mLkT91N83AA'

# وظيفة إضافة صدى الصوت
def apply_reverb(input_path):
    audio = AudioSegment.from_file(input_path)
    # محاكاة الصدى عن طريق دمج الصوت مع نفسه بتأخير بسيط
    reverb = audio.overlay(audio, position=120) 
    output_path = input_path.replace(".mp3", "_capriccio.mp3")
    reverb.export(output_path, format="mp3")
    return output_path

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلاً بك في Shadow V99! 🚀 أرسل رابط يوتيوب لتحويله لصوت.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if "youtube.com" in url or "youtu.be" in url:
        context.user_data['url'] = url
        keyboard = [
            [InlineKeyboardButton("صوت عادي 🎵", callback_data='normal')],
            [InlineKeyboardButton("صدى صوت (Capriccio) 🎙️", callback_data='reverb')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text('اختر نوع المعالجة المطلوبة:', reply_markup=reply_markup)
    else:
        await update.message.reply_text('من فضلك أرسل رابط يوتيوب صحيح.')

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    url = context.user_data.get('url')
    
    await query.edit_message_text(text="جاري التحميل والمعالجة... انتظر قليلاً ⏳")

    # إعدادات التحميل
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}],
        'outtmpl': 'downloaded_audio.%(ext)s',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    
    file_path = "downloaded_audio.mp3"

    if query.data == 'reverb':
        file_path = apply_reverb(file_path)

    await context.bot.send_audio(chat_id=update.effective_chat.id, audio=open(file_path, 'rb'))
    
    # تنظيف الملفات بعد الإرسال
    if os.path.exists(file_path): os.remove(file_path)

def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(CallbackQueryHandler(button_click))
    application.run_polling()

if __name__ == '__main__':
    main()
