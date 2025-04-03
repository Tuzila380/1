from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, ConversationHandler

TOKEN = "7885759155:AAHYE5TfoEhc4eWtE4Tss3Ro6GtkgdyRJwE"
ADMIN_GROUP_CHAT_ID = -4735156605  # ID группы админов
TARGET_USER_ID = 987654321  # ID пользователя, которому пересылать сообщения

# Этапы разговора
WAITING_FOR_COMPLAINT = 1
WAITING_FOR_BID = 2

async def start(update: Update, context: CallbackContext):
    keyboard = [
        ["Varnix Group", "Varnix Games"],
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Выберите действие:", reply_markup=reply_markup)

async def ask_for_complaint(update: Update, context: CallbackContext):
    await update.message.reply_text("Опишите вашу жалобу текстом.", reply_markup=ReplyKeyboardRemove())
    return WAITING_FOR_COMPLAINT

async def receive_complaint(update: Update, context: CallbackContext):
    user = update.message.from_user
    user_text_complaint = update.message.text  

    username = f"(@{user.username})" if user.username else "(без username)"
    message_to_admins = f"🔹 Жалоба от {user.full_name} {username}:\n{user_text_complaint}"

    await context.bot.send_message(chat_id=ADMIN_GROUP_CHAT_ID, text=message_to_admins)
    await update.message.reply_text("Ваша жалоба отправлена администраторам.", reply_markup=ReplyKeyboardMarkup([["🔙 Назад"]], resize_keyboard=True))

    return ConversationHandler.END  

async def ask_for_bid(update: Update, context: CallbackContext):
    await update.message.reply_text("1. Назваите куда хотите попасть \n2. Напишите почему именно вы должны попасть на эту должность", reply_markup=ReplyKeyboardRemove())
    return WAITING_FOR_BID

async def receive_bid(update: Update, context: CallbackContext):
    user_text_bid = update.message.text  
    user = update.message.from_user
    await update.message.reply_text(f"Ваша заявка: {user_text_bid}", reply_markup=ReplyKeyboardMarkup([["🔙 Назад"]], resize_keyboard=True))

    username = f"(@{user.username})" if user.username else "(без username)"
    message_to_admins = f"📩 Заявка от {user.full_name} {username}:\n{user_text_bid}"

    await context.bot.send_message(chat_id=ADMIN_GROUP_CHAT_ID, text=message_to_admins)
    await update.message.reply_text("Ваша заявка отправлена администраторам.", reply_markup=ReplyKeyboardMarkup([["🔙 Назад"]], resize_keyboard=True))
    return ConversationHandler.END  

async def forward_admin_messages(update: Update, context: CallbackContext):
    """Пересылка всех сообщений из группы админов определённому пользователю"""
    if update.message.chat_id == ADMIN_GROUP_CHAT_ID:  
        user_message = update.message.text  
        await context.bot.send_message(chat_id=TARGET_USER_ID, text=f"📩 Сообщение от админов:\n{user_message}")

async def receive_complaint(update: Update, context: CallbackContext):
    user = update.message.from_user
    user_text_complaint = update.message.text  

    username = f"(@{user.username})" if user.username else "(без username)"
    message_to_admins = f"🔹 Жалоба от {user.full_name} {username}:\n{user_text_complaint}"

    # Отправляем жалобу в группу админов и запоминаем ID пользователя
    sent_message = await context.bot.send_message(chat_id=ADMIN_GROUP_CHAT_ID, text=message_to_admins)
    context.bot_data[sent_message.message_id] = user.id  # Запоминаем ID пользователя по ID сообщения

    await update.message.reply_text("Ваша жалоба отправлена администраторам.", reply_markup=ReplyKeyboardMarkup([["🔙 Назад"]], resize_keyboard=True))

    return ConversationHandler.END  

async def forward_admin_reply(update: Update, context: CallbackContext):
    """Отправляет ответ администратора обратно пользователю"""
    if update.message.reply_to_message:  # Проверяем, есть ли ответ на сообщение
        original_message_id = update.message.reply_to_message.message_id
        user_id = context.bot_data.get(original_message_id)  # Получаем ID пользователя

        if user_id:
            await context.bot.send_message(chat_id=user_id, text=f"Ответ от администрации:\n{update.message.text}")



async def receive_bid(update: Update, context: CallbackContext):
    user = update.message.from_user
    user_text_bid = update.message.text  

    username = f"(@{user.username})" if user.username else "(без username)"
    message_to_admins = f"📩 Заявка от {user.full_name} {username}:\n{user_text_bid}"

    # Отправляем жалобу в группу админов и запоминаем ID пользователя
    sent_message = await context.bot.send_message(chat_id=ADMIN_GROUP_CHAT_ID, text=message_to_admins)
    context.bot_data[sent_message.message_id] = user.id  # Запоминаем ID пользователя по ID сообщения

    await update.message.reply_text("Ваша заявка отправлена администраторам.", reply_markup=ReplyKeyboardMarkup([["🔙 Назад"]], resize_keyboard=True))

    return ConversationHandler.END  

async def forward_admin_reply(update: Update, context: CallbackContext):
    """Отправляет ответ администратора обратно пользователю"""
    if update.message.reply_to_message:  # Проверяем, есть ли ответ на сообщение
        original_message_id = update.message.reply_to_message.message_id
        user_id = context.bot_data.get(original_message_id)  # Получаем ID пользователя

        if user_id:
            await context.bot.send_message(chat_id=user_id, text=f"Ответ от администрации:\n{update.message.text}")


async def message_handler(update: Update, context: CallbackContext):
    text = update.message.text

    if text == "Varnix Group":
        keyboard = [["Вакансии", "Хочу к Вам"], ["🔙 Назад"]]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text("Выберите действие:", reply_markup=reply_markup)

    elif text == "Вакансии":
        await update.message.reply_text("Список вакансий: ...")

    elif text == "Хочу к Вам":
        await update.message.reply_text("Оставьте свои контакты и мы с вами свяжемся")

    elif text == "Varnix Games":
        keyboard = [["Rust Сервер"], ["🔙 Назад"]]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text("Выберите действие:", reply_markup=reply_markup)

    elif text == "Rust Сервер":
        keyboard = [["Жалоба"], ["🔙 Назад"]]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text("Выберите действие:", reply_markup=reply_markup)

    elif text == "🔙 Назад":
        await start(update, context)

def main():
    app = Application.builder().token(TOKEN).build()

    complaint_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("^Жалоба$"), ask_for_complaint)],
        states={WAITING_FOR_COMPLAINT: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_complaint)]},
        fallbacks=[]
    )

    bid_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("^Хочу к Вам$"), ask_for_bid)],
        states={WAITING_FOR_BID: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_bid)]},
        fallbacks=[]
    )

    app.add_handler(MessageHandler(filters.REPLY & filters.TEXT, forward_admin_reply))
    app.add_handler(MessageHandler(filters.REPLY & filters.TEXT, forward_admin_reply))


    app.add_handler(CommandHandler("start", start))
    app.add_handler(complaint_handler)
    app.add_handler(bid_handler)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    
    # Добавляем обработчик пересылки сообщений из группы админов
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, forward_admin_messages))

    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()
