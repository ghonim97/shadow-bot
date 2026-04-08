import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

# إعداد السجلات (Logs) لمعرفة ما يحدث داخل البوت
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# ضع التوكن الخاص بك هنا
TOKEN = '8785291349:AAEPeEGhgCKkUIKYkOt-xg53mLkT91N83AA'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """أمر البداية"""
    user = update.effective_user
    await update.message.reply_html(
        rf"أهلاً بك يا {user.mention_html()} في <b>Shadow V99</b>! 🚀"
        "\n\nأرسل لي أي رابط فيديو (TikTok, YouTube) وسأقوم بمعالجته فوراً."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """الرد على الروابط بإظهار الأزرار"""
    url = update.message.text
    
    # التأكد أن الرسالة تحتوي على رابط (تحقق بسيط)
    if "http" in url:
        keyboard = [
            [InlineKeyboardButton("بدون علامة مائية 🎬", callback_data='no_wm')],
            [InlineKeyboardButton("صدى صوت (Capriccio) 🎶", callback_data='echo')],
            [InlineKeyboardButton("إحصائيات البوت 📊", callback_data='stats')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text('تم استلام الرابط بنجاح! اختر ماذا تريد أن أفعل:', reply_markup=reply_markup)
    else:
        await update.message.reply_text('من فضلك أرسل رابطاً صحيحاً ليتمكن Shadow من مساعدتك. 🧐')

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """التعامل مع ضغطات الأزرار"""
    query = update.callback_query
    await query.answer()
    
    if query.data == 'no_wm':
        await query.edit_message_text(text="جاري بدء التحميل بدون علامة مائية... انتظر قليلاً. ⏳")
    elif query.data == 'echo':
        await query.edit_message_text(text="جاري معالجة الصوت وإضافة تأثير الصدى... 🎙️")
    elif query.data == 'stats':
        await query.edit_message_text(text="إحصائيات Shadow V99 حالياً: البوت في طور التجربة! 📈")

def main():
    """تشغيل البوت"""
    # بناء التطبيق باستخدام التوكن
    application = Application.builder().token(TOKEN).build()

    # إضافة الأوامر والمستقبلات
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(CallbackQueryHandler(button_click))

    # بدء العمل
    print("Shadow V99 is now Live on Railway! 🚀")
    application.run_polling()

if __name__ == '__main__':
    main()
