import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
import json

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ВАЖНО: Замените на ваш токен от @BotFather
BOT_TOKEN = "8285221140:AAEzqIyXzdNlj5dQhmQD2uIWCUG_mooTBrg"
# Замените на ваш URL сайта
WEB_APP_URL = "https://aadesign.store/"
# ID администратора (ваш Telegram ID)
ADMIN_ID = 1240742785  # Замените на ваш ID

# Тексты сообщений
WELCOME_MESSAGE = """
🎀 Добро пожаловать в A&A Design!

Мы создаем уникальные кастомные журналы - идеальный подарок для ваших близких ❤️

📖 Персонализированные журналы от 2799₽
⏱ Изготовление от 1 до 14 дней
🚚 Доставка по всей России

Нажмите кнопку "🛍 Магазин" ниже, чтобы оформить заказ!
"""

HELP_MESSAGE = """
📋 Как заказать журнал:

1. Нажмите кнопку "🛍 Магазин"
2. Выберите размер журнала
3. Нажмите "Заказать"
4. Мы свяжемся с вами для уточнения деталей

💬 По всем вопросам пишите @aa_design
📸 Наши работы: @aa_design_channel
"""

CONTACT_MESSAGE = """
📞 Наши контакты:

📱 Telegram: @aa_design
📷 Instagram: @aa.design.journals
📢 Канал: @aa_design_channel

Пишите в любое время!
Ответим в течение 30 минут в рабочее время (10:00-20:00 МСК)
"""

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отправляет приветственное сообщение с кнопкой Web App"""
    
    # Создаем кнопку для открытия Web App
    keyboard = [
        [InlineKeyboardButton(
            text="🛍 Магазин",
            web_app=WebAppInfo(url=WEB_APP_URL)
        )],
        [
            InlineKeyboardButton("📞 Контакты", callback_data="contacts"),
            InlineKeyboardButton("❓ Помощь", callback_data="help")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Отправляем сообщение с фото (если есть)
    await update.message.reply_text(
        WELCOME_MESSAGE,
        reply_markup=reply_markup,
        parse_mode='HTML'
    )

# Команда /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показывает справку"""
    await update.message.reply_text(HELP_MESSAGE)

# Команда /contacts
async def contacts_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показывает контакты"""
    await update.message.reply_text(CONTACT_MESSAGE)

# Обработка callback кнопок
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обрабатывает нажатия на inline кнопки"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "help":
        await query.message.reply_text(HELP_MESSAGE)
    elif query.data == "contacts":
        await query.message.reply_text(CONTACT_MESSAGE)

# Обработка данных из Web App
async def web_app_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обрабатывает данные, полученные из Web App"""
    
    # Получаем данные из Web App
    web_app_data = update.message.web_app_data.data
    
    try:
        # Парсим JSON данные
        data = json.loads(web_app_data)
        
        # Определяем тип действия
        if data.get('action') == 'order':
            # Обработка заказа
            service = data.get('service', 'Неизвестная услуга')
            price = data.get('price', 'Не указана')
            details = data.get('details', '')
            time = data.get('time', '')
            
            # Формируем сообщение о заказе
            order_message = f"""
✅ <b>Новый заказ!</b>

👤 Клиент: {update.message.from_user.first_name} {update.message.from_user.last_name or ''}
🆔 Username: @{update.message.from_user.username or 'не указан'}
📦 Услуга: {service}
💰 Цена: {price}
📝 Детали: {details}
⏱ Время: {time}

Свяжитесь с клиентом для уточнения деталей заказа.
"""
            
            # Отправляем клиенту подтверждение
            confirmation_message = f"""
✅ <b>Ваш заказ принят!</b>

Вы заказали: {service}
Стоимость: {price}
{time}

Наш менеджер свяжется с вами в течение 30 минут для уточнения деталей.

Если у вас есть вопросы, пишите @aa_design
"""
            await update.message.reply_text(
                confirmation_message,
                parse_mode='HTML'
            )
            
            # Отправляем уведомление администратору
            try:
                await context.bot.send_message(
                    chat_id=ADMIN_ID,
                    text=order_message,
                    parse_mode='HTML'
                )
            except Exception as e:
                logger.error(f"Не удалось отправить сообщение админу: {e}")
        
        elif data.get('action') == 'checkout':
            # Обработка оформления корзины
            cart = data.get('cart', [])
            total = data.get('total', 0)
            
            # Формируем список заказов
            items_list = "\n".join([f"• {item['service']} - {item['price']}" for item in cart])
            
            checkout_message = f"""
🛒 <b>Оформление заказа</b>

👤 Клиент: {update.message.from_user.first_name}
🆔 @{update.message.from_user.username or 'не указан'}

<b>Заказ:</b>
{items_list}

<b>Итого: {total}₽</b>

Свяжитесь с клиентом для оформления заказа.
"""
            
            # Отправляем подтверждение клиенту
            await update.message.reply_text(
                f"✅ Заказ на сумму {total}₽ принят!\nМенеджер свяжется с вами в ближайшее время.",
                parse_mode='HTML'
            )
            
            # Отправляем админу
            try:
                await context.bot.send_message(
                    chat_id=ADMIN_ID,
                    text=checkout_message,
                    parse_mode='HTML'
                )
            except Exception as e:
                logger.error(f"Не удалось отправить сообщение админу: {e}")
        
        elif data.get('action') == 'contact_click':
            # Отслеживание клика по контактам
            platform = data.get('platform', 'unknown')
            logger.info(f"Пользователь {update.message.from_user.username} кликнул на {platform}")
        
        elif data.get('action') == 'idea_selected':
            # Пользователь выбрал идею для журнала
            idea = data.get('idea', '')
            
            await update.message.reply_text(
                f"Отличная идея! Мы добавим '{idea}' в ваш журнал. 💡",
                parse_mode='HTML'
            )
            
    except json.JSONDecodeError:
        logger.error(f"Не удалось распарсить данные: {web_app_data}")
        await update.message.reply_text(
            "Произошла ошибка при обработке данных. Пожалуйста, попробуйте еще раз."
        )

# Обработка обычных сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обрабатывает обычные текстовые сообщения"""
    
    text = update.message.text.lower()
    
    if "заказ" in text or "купить" in text or "цена" in text:
        # Если спрашивают про заказ
        keyboard = [[InlineKeyboardButton(
            text="🛍 Открыть магазин",
            web_app=WebAppInfo(url=WEB_APP_URL)
        )]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "Для оформления заказа откройте наш магазин:",
            reply_markup=reply_markup
        )
    
    elif "контакт" in text or "связь" in text:
        await update.message.reply_text(CONTACT_MESSAGE)
    
    elif "помощь" in text or "как" in text:
        await update.message.reply_text(HELP_MESSAGE)
    
    else:
        # Дефолтный ответ
        await update.message.reply_text(
            "Я могу помочь вам заказать кастомный журнал!\n"
            "Используйте команды:\n"
            "/start - Главное меню\n"
            "/help - Помощь\n"
            "/contacts - Контакты"
        )

# Команда для получения ID пользователя (для админа)
async def get_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показывает ID пользователя"""
    user_id = update.message.from_user.id
    await update.message.reply_text(f"Ваш Telegram ID: `{user_id}`", parse_mode='Markdown')

def main():
    """Запуск бота"""
    # Создаем приложение
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Регистрируем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("contacts", contacts_command))
    application.add_handler(CommandHandler("id", get_id))
    
    # Обработчик callback кнопок
    application.add_handler(CallbackQueryHandler(button_callback))
    
    # Обработчик данных из Web App
    application.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, web_app_data))
    
    # Обработчик обычных сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Запускаем бота
    print("🤖 Бот запущен!")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()