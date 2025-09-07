import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
import json

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Получаем настройки из переменных окружения
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8285221140:AAEzqIyXzdNlj5dQhmQD2uIWCUG_mooTBrg")
WEB_APP_URL = os.environ.get("WEB_APP_URL", "https://aadesign.store/")
ADMIN_ID = int(os.environ.get("ADMIN_ID", "1240742785"))

# Проверяем наличие токена
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не установлен!")

# Тексты сообщений
WELCOME_MESSAGE = """
🎀 Добро пожаловать в A&A Design!

Мы создаем уникальные кастомные журналы - идеальный подарок для ваших близких ❤️

📖 Персонализированные журналы от 2799₽
⏱ Изготовление от 1 до 14 дней
🚚 Доставка по всей России

✨ Новинка: Интерактивные 3D книги с кейсами!

Нажмите кнопку "🛍 Магазин" ниже, чтобы оформить заказ!
"""

HELP_MESSAGE = """
📋 Как заказать журнал:

1. Нажмите кнопку "🛍 Магазин"
2. Выберите размер журнала
3. Нажмите "Заказать"
4. Мы свяжемся с вами для уточнения деталей

📖 В разделе "Кейсы" смотрите наши 3D книги:
• Нажмите на книгу, чтобы перелистнуть страницы
• Изучите примеры наших работ
• Вдохновляйтесь идеями для своего заказа

💬 По всем вопросам пишите @cosmeticsourc
📸 Наши работы: @aadesingmag
"""

CONTACT_MESSAGE = """
📞 Наши контакты:

📱 Менеджер: @cosmeticsourc
📷 Instagram: @aadesingmag
📢 Канал: @aadesingmag

Пишите в любое время!
Ответим в течение 30 минут в рабочее время (10:00-20:00 МСК)

🎀 Более 100 довольных клиентов с 2023 года
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
        ],
        [InlineKeyboardButton("📖 Посмотреть 3D кейсы", callback_data="cases_info")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Отправляем сообщение
    await update.message.reply_text(
        WELCOME_MESSAGE,
        reply_markup=reply_markup,
        parse_mode='HTML'
    )
    
    logger.info(f"User {update.message.from_user.username} started bot")

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
    elif query.data == "cases_info":
        cases_info = """
📖 <b>Интерактивные 3D книги с нашими кейсами!</b>

В разделе "Кейсы" вы найдете 4 интерактивные 3D книги:

📚 <b>Наши проекты:</b>
• 🌸 Журнал для мамы
• 💕 Love Story
• 👭 Лучшей подруге  
• 👨‍👩‍👧‍👦 Семейная история

<b>Как пользоваться:</b>
1. Перейдите в раздел "Кейсы"
2. Нажмите на любую книгу
3. Страницы перелистнутся, показав детали проекта
4. Нажмите снова, чтобы вернуться к обложке

Это поможет вам выбрать стиль для своего заказа! 🎨
"""
        
        keyboard = [[InlineKeyboardButton(
            text="📖 Открыть кейсы",
            web_app=WebAppInfo(url=WEB_APP_URL + "#cases")
        )]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.message.reply_text(
            cases_info,
            reply_markup=reply_markup,
            parse_mode='HTML'
        )

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

💡 <b>Пока ждете:</b>
• Посмотрите 3D кейсы для вдохновения
• Подготовьте фотографии для журнала
• Подумайте о тематике и стиле

Если у вас есть вопросы, пишите @cosmeticsourc
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
                logger.info(f"Order notification sent to admin")
            except Exception as e:
                logger.error(f"Failed to send message to admin: {e}")
        
        elif data.get('action') == 'book_flip':
            # Обработка взаимодействия с 3D книгами
            book = data.get('data', {}).get('book', 'unknown')
            action = data.get('data', {}).get('action', 'unknown')
            
            if action == 'open':
                book_names = {
                    '1': 'Журнал для мамы',
                    '2': 'Love Story',
                    '3': 'Лучшей подруге',
                    '4': 'Семейная история'
                }
                book_name = book_names.get(book, f'Книга #{book}')
                
                response = f"📖 Вы открыли кейс: <b>{book_name}</b>\n\nПонравился стиль? Закажите похожий журнал!"
                
                keyboard = [[InlineKeyboardButton(
                    text="🛒 Заказать похожий",
                    web_app=WebAppInfo(url=WEB_APP_URL + "#shop")
                )]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                await update.message.reply_text(
                    response,
                    reply_markup=reply_markup,
                    parse_mode='HTML'
                )
            
            logger.info(f"Book flip: {book} - {action} by {update.message.from_user.username}")
        
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
                f"✅ Заказ на сумму {total}₽ принят!\n\nМенеджер свяжется с вами в ближайшее время.\n\n💡 Рекомендуем посмотреть наши 3D кейсы для вдохновения!",
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
                logger.error(f"Failed to send message to admin: {e}")
        
        elif data.get('action') == 'contact_click':
            # Отслеживание клика по контактам
            platform = data.get('platform', 'unknown')
            logger.info(f"User {update.message.from_user.username} clicked on {platform}")
            
            # Отправляем благодарность
            thanks_message = {
                'telegram': "Спасибо! Вы переходите к нашему менеджеру 📱",
                'instagram': "Отлично! Подписывайтесь на наш Instagram 📷", 
                'channel': "Супер! Присоединяйтесь к нашему каналу 📢"
            }
            
            if platform in thanks_message:
                await update.message.reply_text(thanks_message[platform])
        
        elif data.get('action') == 'analytics':
            # Аналитика (логируем для статистики)
            event = data.get('event', {})
            logger.info(f"Analytics: {event.get('name')} by {update.message.from_user.username}")
            
    except json.JSONDecodeError:
        logger.error(f"Failed to parse data: {web_app_data}")
        await update.message.reply_text(
            "Произошла ошибка при обработке данных. Пожалуйста, попробуйте еще раз."
        )

# Обработка обычных сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обрабатывает обычные текстовые сообщения"""
    
    text = update.message.text.lower()
    
    if any(word in text for word in ["заказ", "купить", "цена", "журнал", "книга"]):
        # Если спрашивают про заказ
        keyboard = [[InlineKeyboardButton(
            text="🛍 Открыть магазин",
            web_app=WebAppInfo(url=WEB_APP_URL)
        )]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "Для оформления заказа откройте наш магазин с интерактивными 3D кейсами:",
            reply_markup=reply_markup
        )
    
    elif any(word in text for word in ["кейс", "пример", "работы", "посмотреть"]):
        # Если интересуются кейсами
        keyboard = [[InlineKeyboardButton(
            text="📖 Посмотреть 3D кейсы",
            web_app=WebAppInfo(url=WEB_APP_URL + "#cases")
        )]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "Посмотрите наши интерактивные 3D кейсы! Нажмите на книги, чтобы перелистнуть страницы:",
            reply_markup=reply_markup
        )
    
    elif any(word in text for word in ["контакт", "связь", "менеджер"]):
        await update.message.reply_text(CONTACT_MESSAGE)
    
    elif any(word in text for word in ["помощь", "как", "инструкция"]):
        await update.message.reply_text(HELP_MESSAGE)
    
    else:
        # Дефолтный ответ с 3D кейсами
        keyboard = [
            [InlineKeyboardButton(
                text="🛍 Магазин",
                web_app=WebAppInfo(url=WEB_APP_URL)
            )],
            [InlineKeyboardButton(
                text="📖 3D Кейсы",
                web_app=WebAppInfo(url=WEB_APP_URL + "#cases")
            )]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "Я помогу вам заказать кастомный журнал! 📚\n\n"
            "🛍 Магазин - выберите размер и закажите\n"
            "📖 3D Кейсы - посмотрите примеры работ\n\n"
            "Команды: /help - помощь, /contacts - контакты",
            reply_markup=reply_markup
        )

# Команда для получения ID пользователя (для админа)
async def get_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показывает ID пользователя"""
    user_id = update.message.from_user.id
    await update.message.reply_text(f"Ваш Telegram ID: `{user_id}`", parse_mode='Markdown')

# Команда статистики (только для админа)
async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показывает статистику бота (только для админа)"""
    if update.message.from_user.id != ADMIN_ID:
        await update.message.reply_text("У вас нет прав для использования этой команды.")
        return
    
    stats_message = """
📊 <b>Статистика A&A Design Bot</b>

🎀 Основные показатели:
• Веб-приложение: активно
• 3D кейсы: работают
• Интеграция с Telegram: ✅

📖 Функционал:
• Интерактивные 3D книги
• Система заказов
• Аналитика взаимодействий
• Автоматические уведомления

🛍 Последние обновления:
• Добавлены 3D книги с кейсами
• Улучшена навигация
• Добавлены haptic отклики
"""
    
    await update.message.reply_text(stats_message, parse_mode='HTML')

def main():
    """Запуск бота"""
    logger.info(f"Starting A&A Design bot with 3D cases...")
    logger.info(f"Bot token: {BOT_TOKEN[:10]}...")
    logger.info(f"Web App URL: {WEB_APP_URL}")
    logger.info(f"Admin ID: {ADMIN_ID}")
    
    # Создаем приложение
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Регистрируем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("contacts", contacts_command))
    application.add_handler(CommandHandler("id", get_id))
    application.add_handler(CommandHandler("stats", stats_command))
    
    # Обработчик callback кнопок
    application.add_handler(CallbackQueryHandler(button_callback))
    
    # Обработчик данных из Web App
    application.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, web_app_data))
    
    # Обработчик обычных сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Запускаем бота
    logger.info("🎀 A&A Design Bot with 3D Cases is starting...")
    print("🎀 A&A Design Bot is running!")
    print(f"📱 Web App: {WEB_APP_URL}")
    print("📖 Features: 3D interactive books, order system, analytics")
    print("Press Ctrl+C to stop")
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()