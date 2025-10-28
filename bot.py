import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
import json
from datetime import datetime

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
🎀 <b>Добро пожаловать в A&A Design!</b>

Мы создаем уникальные кастомные журналы - идеальный подарок для ваших близких.

✨ <b>Что нового:</b>
• Современный liquid glass дизайн
• Интерактивная 3D книга с примерами работ
• Карта наших типографий по всей России
• Удобная навигация

<b>Наши услуги:</b>
📖 Персонализированные журналы от 2800₽
⏱ Изготовление от 1 до 9 дней
🚚 Доставка по всей России

<b>Откройте веб-приложение ниже!</b>
"""

HELP_MESSAGE = """
📋 <b>Как пользоваться приложением:</b>

<b>🛍 Магазин</b>
• Выберите размер журнала
• Нажмите "Заказать"
• Вы будете перенаправлены к менеджеру

<b>📖 Кейсы</b>
• Посмотрите интерактивную 3D книгу
• Кликайте на книгу, чтобы перелистывать страницы
• 18 страниц примеров наших работ

<b>❓ FAQ</b>
• Ответы на частые вопросы
• Карта наших типографий
• Выберите ближайший город

<b>👤 Контакты</b>
• Свяжитесь с менеджером
• Подпишитесь на канал
• Режим работы: 10:00-20:00 МСК

💬 <b>Менеджер:</b> @aadesignmagg
📢 <b>Канал:</b> @aadesignmag
"""

CONTACT_MESSAGE = """
📞 <b>Наши контакты:</b>

📱 <b>Менеджер:</b> @aadesignmagg
📢 <b>Канал:</b> @aadesignmag

<b>Режим работы:</b>
🕐 10:00 - 20:00 МСК
⚡ Ответим в течение 30 минут

<b>Статистика:</b>
🎀 Более 100 довольных клиентов
📅 Работаем с 2023 года
🚚 Доставка по всей России

Пишите в любое время - мы всегда рады помочь!
"""

ABOUT_MESSAGE = """
🎀 <b>О A&A Design</b>

<b>Кастомный журнал</b> — это уникальный и запоминающийся подарок, который покажет вашу любовь и внимание к человеку.

💝 <b>Почему выбирают нас:</b>
• Индивидуальный подход к каждому клиенту
• Профессиональный дизайн и верстка
• Качественная печать на плотной бумаге
• Быстрые сроки изготовления
• Доставка по всей России

🎨 <b>Что мы создаем:</b>
• Журналы для мамы, папы, друзей
• Love Story для пары
• Travel Book о путешествиях
• Семейные истории
• Тематические постеры

📦 <b>Типографии в городах:</b>
Москва • Санкт-Петербург • Казань • Екатеринбург • Новосибирск • Нижний Новгород • Самара • Ростов-на-Дону

<i>С таким подарком вы надолго оставите яркие эмоции не только в памяти, но и на бумаге!</i>
"""

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отправляет приветственное сообщение с кнопкой Web App"""
    
    # Создаем кнопку для открытия Web App
    keyboard = [
        [InlineKeyboardButton(
            text="🎨 Открыть приложение",
            web_app=WebAppInfo(url=WEB_APP_URL)
        )],
        [
            InlineKeyboardButton("📞 Контакты", callback_data="contacts"),
            InlineKeyboardButton("❓ Помощь", callback_data="help")
        ],
        [InlineKeyboardButton("🎀 О нас", callback_data="about")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Отправляем сообщение
    await update.message.reply_text(
        WELCOME_MESSAGE,
        reply_markup=reply_markup,
        parse_mode='HTML'
    )
    
    user = update.message.from_user
    logger.info(f"User {user.username or user.id} started bot")
    
    # Уведомление админу о новом пользователе
    try:
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"🆕 <b>Новый пользователь!</b>\n\n"
                 f"👤 {user.first_name} {user.last_name or ''}\n"
                 f"🆔 @{user.username or 'без username'}\n"
                 f"ID: {user.id}",
            parse_mode='HTML'
        )
    except Exception as e:
        logger.error(f"Failed to notify admin: {e}")

# Команда /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показывает справку"""
    keyboard = [[InlineKeyboardButton(
        text="🎨 Открыть приложение",
        web_app=WebAppInfo(url=WEB_APP_URL)
    )]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        HELP_MESSAGE,
        reply_markup=reply_markup,
        parse_mode='HTML'
    )

# Команда /contacts
async def contacts_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показывает контакты"""
    await update.message.reply_text(CONTACT_MESSAGE, parse_mode='HTML')

# Команда /about
async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показывает информацию о компании"""
    await update.message.reply_text(ABOUT_MESSAGE, parse_mode='HTML')

# Обработка callback кнопок
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обрабатывает нажатия на inline кнопки"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "help":
        keyboard = [[InlineKeyboardButton(
            text="🎨 Открыть приложение",
            web_app=WebAppInfo(url=WEB_APP_URL)
        )]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text(HELP_MESSAGE, reply_markup=reply_markup, parse_mode='HTML')
        
    elif query.data == "contacts":
        await query.message.reply_text(CONTACT_MESSAGE, parse_mode='HTML')
        
    elif query.data == "about":
        await query.message.reply_text(ABOUT_MESSAGE, parse_mode='HTML')

# Обработка данных из Web App
async def web_app_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обрабатывает данные, полученные из Web App"""
    
    # Получаем данные из Web App
    web_app_data = update.message.web_app_data.data
    user = update.message.from_user
    
    try:
        # Парсим JSON данные
        data = json.loads(web_app_data)
        action = data.get('action')
        
        logger.info(f"WebApp data from {user.username}: {action}")
        
        # ============================================
        # ОБРАБОТКА ЗАКАЗОВ
        # ============================================
        if action == 'order':
            service = data.get('service', 'Неизвестная услуга')
            price = data.get('price', 'Не указана')
            product = data.get('product', 'unknown')
            
            # Эмодзи для разных типов услуг
            service_emoji = {
                'size-s': '📕',
                'size-m': '📗',
                'size-l': '📘',
                'size-xl': '📙',
                'travel-book': '🗺',
                'poster': '🖼',
                'express': '⚡',
                'template': '📄'
            }
            
            emoji = service_emoji.get(product, '📖')
            
            # Формируем сообщение о заказе для админа
            order_message = f"""
{emoji} <b>НОВЫЙ ЗАКАЗ!</b>

<b>Клиент:</b>
👤 {user.first_name} {user.last_name or ''}
🆔 @{user.username or 'без username'}
ID: <code>{user.id}</code>

<b>Заказ:</b>
📦 {service}
💰 {price}

<b>Время:</b> {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}

<i>Свяжитесь с клиентом для уточнения деталей.</i>
"""
            
            # Отправляем клиенту подтверждение
            confirmation_message = f"""
✅ <b>Ваш заказ принят!</b>

{emoji} <b>Вы заказали:</b> {service}
💰 <b>Стоимость:</b> {price}

Наш менеджер свяжется с вами в течение 30 минут для уточнения деталей.

💡 <b>Пока ждете:</b>
• Посмотрите 3D кейсы для вдохновения
• Подготовьте фотографии для журнала
• Подумайте о тематике и стиле

Если у вас есть вопросы, пишите @aadesignmagg
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
                logger.info(f"Order notification sent to admin for {service}")
            except Exception as e:
                logger.error(f"Failed to send message to admin: {e}")
        
        # ============================================
        # ОБРАБОТКА ВЗАИМОДЕЙСТВИЯ С 3D КНИГОЙ
        # ============================================
        elif action == 'book_flip':
            book = data.get('data', {}).get('book', 'unknown')
            flip_action = data.get('data', {}).get('action', 'unknown')
            
            if flip_action == 'open':
                response = f"📖 <b>Отлично!</b>\n\nВы открыли интерактивную книгу с примерами наших работ.\n\nПродолжайте кликать, чтобы перелистывать страницы!"
                
                keyboard = [[InlineKeyboardButton(
                    text="🛒 Заказать похожий журнал",
                    web_app=WebAppInfo(url=WEB_APP_URL + "#shop")
                )]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                await update.message.reply_text(
                    response,
                    reply_markup=reply_markup,
                    parse_mode='HTML'
                )
            
            logger.info(f"Book flip: book={book}, action={flip_action} by {user.username}")
        
        # ============================================
        # ОБРАБОТКА ВЗАИМОДЕЙСТВИЯ С КАРТОЙ
        # ============================================
        elif action == 'analytics':
            event = data.get('event', {})
            event_name = event.get('name', 'unknown')
            event_data = event.get('data', {})
            
            # Логируем аналитику
            logger.info(f"Analytics: {event_name} by {user.username} - {event_data}")
            
            # Отправляем админу важные события
            important_events = ['map_city_select', 'route_requested', 'address_copied', 'order', 'contact_click']
            
            if event_name in important_events:
                analytics_message = f"""
📊 <b>Аналитика</b>

<b>Пользователь:</b> @{user.username or user.id}
<b>Событие:</b> {event_name}
<b>Данные:</b> {json.dumps(event_data, ensure_ascii=False, indent=2)}
<b>Время:</b> {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}
"""
                
                try:
                    await context.bot.send_message(
                        chat_id=ADMIN_ID,
                        text=analytics_message,
                        parse_mode='HTML'
                    )
                except Exception as e:
                    logger.error(f"Failed to send analytics to admin: {e}")
            
            # Специальная обработка для карты
            if event_name == 'map_city_select':
                city = event_data.get('city', 'неизвестный город')
                await update.message.reply_text(
                    f"📍 Вы выбрали типографию в городе: <b>{city}</b>\n\n"
                    f"Скопируйте адрес или постройте маршрут в приложении!",
                    parse_mode='HTML'
                )
            
            elif event_name == 'route_requested':
                city = event_data.get('city', 'неизвестный город')
                await update.message.reply_text(
                    f"🗺 Маршрут до типографии в городе <b>{city}</b> открыт в Яндекс.Картах!",
                    parse_mode='HTML'
                )
            
            elif event_name == 'address_copied':
                await update.message.reply_text(
                    f"✅ Адрес типографии скопирован в буфер обмена!"
                )
        
        # ============================================
        # ОБРАБОТКА КЛИКОВ ПО КОНТАКТАМ
        # ============================================
        elif action == 'contact_click':
            platform = data.get('platform', 'unknown')
            url = data.get('url', '')
            
            platform_names = {
                'manager': 'Менеджер',
                'channel': 'Канал'
            }
            
            platform_name = platform_names.get(platform, platform)
            
            logger.info(f"User {user.username} clicked on {platform}: {url}")
            
            # Благодарность пользователю
            thanks_messages = {
                'manager': "📱 Спасибо! Вы переходите к нашему менеджеру. Он ответит в течение 30 минут!",
                'channel': "📢 Отлично! Присоединяйтесь к нашему каналу и следите за новостями!"
            }
            
            if platform in thanks_messages:
                await update.message.reply_text(thanks_messages[platform])
            
            # Уведомление админу
            try:
                await context.bot.send_message(
                    chat_id=ADMIN_ID,
                    text=f"👆 <b>Клик по контакту</b>\n\n"
                         f"Пользователь: @{user.username or user.id}\n"
                         f"Платформа: {platform_name}\n"
                         f"Время: {datetime.now().strftime('%H:%M:%S')}",
                    parse_mode='HTML'
                )
            except Exception as e:
                logger.error(f"Failed to notify admin: {e}")
        
        # ============================================
        # ОБРАБОТКА НАВИГАЦИИ
        # ============================================
        elif action == 'navigation':
            to_section = data.get('to', 'unknown')
            logger.info(f"User {user.username} navigated to: {to_section}")
        
        # ============================================
        # НЕИЗВЕСТНОЕ ДЕЙСТВИЕ
        # ============================================
        else:
            logger.warning(f"Unknown action: {action} from {user.username}")
        
    except json.JSONDecodeError:
        logger.error(f"Failed to parse WebApp data: {web_app_data}")
        await update.message.reply_text(
            "❌ Произошла ошибка при обработке данных. Пожалуйста, попробуйте еще раз."
        )
    except Exception as e:
        logger.error(f"Error processing WebApp data: {e}")
        await update.message.reply_text(
            "❌ Произошла ошибка. Пожалуйста, попробуйте еще раз или свяжитесь с поддержкой."
        )

# Обработка обычных сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обрабатывает обычные текстовые сообщения"""
    
    text = update.message.text.lower()
    
    # Ключевые слова для разных разделов
    order_keywords = ["заказ", "купить", "цена", "журнал", "книга", "стоимость", "сколько"]
    cases_keywords = ["кейс", "пример", "работы", "посмотреть", "портфолио", "образец"]
    contact_keywords = ["контакт", "связь", "менеджер", "телефон", "написать"]
    help_keywords = ["помощь", "как", "инструкция", "что", "где"]
    map_keywords = ["типография", "адрес", "карта", "город", "где находится"]
    
    if any(word in text for word in order_keywords):
        # Если спрашивают про заказ
        keyboard = [[InlineKeyboardButton(
            text="🛍 Открыть магазин",
            web_app=WebAppInfo(url=WEB_APP_URL + "#shop")
        )]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "🛍 <b>Оформить заказ</b>\n\n"
            "Откройте наш магазин и выберите подходящий размер журнала:\n\n"
            "📕 Размер S - от 3800₽\n"
            "📗 Размер M - от 4800₽\n"
            "📘 Размер L - от 5800₽\n"
            "📙 Размер XL - от 7800₽\n"
            "🗺 Travel Book - 3800₽\n"
            "🖼 Постер - 2000₽\n"
            "⚡ Express - 9800₽",
            reply_markup=reply_markup,
            parse_mode='HTML'
        )
    
    elif any(word in text for word in cases_keywords):
        # Если интересуются кейсами
        keyboard = [[InlineKeyboardButton(
            text="📖 Посмотреть 3D книгу",
            web_app=WebAppInfo(url=WEB_APP_URL + "#cases")
        )]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "📖 <b>Интерактивная 3D книга</b>\n\n"
            "Посмотрите нашу интерактивную книгу с примерами работ!\n\n"
            "Нажмите на книгу, чтобы перелистывать страницы. "
            "18 страниц с реальными примерами наших журналов!",
            reply_markup=reply_markup,
            parse_mode='HTML'
        )
    
    elif any(word in text for word in map_keywords):
        # Если спрашивают про типографии
        keyboard = [[InlineKeyboardButton(
            text="🗺 Посмотреть карту типографий",
            web_app=WebAppInfo(url=WEB_APP_URL + "#faq")
        )]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "🗺 <b>Наши типографии</b>\n\n"
            "Мы работаем с типографиями в 8 городах России:\n\n"
            "📍 Москва\n"
            "📍 Санкт-Петербург\n"
            "📍 Казань\n"
            "📍 Екатеринбург\n"
            "📍 Новосибирск\n"
            "📍 Нижний Новгород\n"
            "📍 Самара\n"
            "📍 Ростов-на-Дону\n\n"
            "Откройте карту, чтобы увидеть адреса и построить маршрут!",
            reply_markup=reply_markup,
            parse_mode='HTML'
        )
    
    elif any(word in text for word in contact_keywords):
        await update.message.reply_text(CONTACT_MESSAGE, parse_mode='HTML')
    
    elif any(word in text for word in help_keywords):
        keyboard = [[InlineKeyboardButton(
            text="🎨 Открыть приложение",
            web_app=WebAppInfo(url=WEB_APP_URL)
        )]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(HELP_MESSAGE, reply_markup=reply_markup, parse_mode='HTML')
    
    else:
        # Дефолтный ответ
        keyboard = [
            [InlineKeyboardButton(
                text="🎨 Открыть приложение",
                web_app=WebAppInfo(url=WEB_APP_URL)
            )],
            [
                InlineKeyboardButton("📞 Контакты", callback_data="contacts"),
                InlineKeyboardButton("❓ Помощь", callback_data="help")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "👋 Здравствуйте! Я помогу вам заказать кастомный журнал.\n\n"
            "<b>Что я могу:</b>\n"
            "🛍 Показать магазин и цены\n"
            "📖 Показать примеры работ (3D книга)\n"
            "🗺 Показать карту типографий\n"
            "📞 Дать контакты менеджера\n\n"
            "Просто напишите что вас интересует или откройте приложение!",
            reply_markup=reply_markup,
            parse_mode='HTML'
        )

# Команда для получения ID пользователя (для админа)
async def get_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показывает ID пользователя"""
    user_id = update.message.from_user.id
    username = update.message.from_user.username
    await update.message.reply_text(
        f"<b>Ваши данные:</b>\n\n"
        f"🆔 ID: <code>{user_id}</code>\n"
        f"👤 Username: @{username or 'не указан'}",
        parse_mode='HTML'
    )

# Команда статистики (только для админа)
async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показывает статистику бота (только для админа)"""
    if update.message.from_user.id != ADMIN_ID:
        await update.message.reply_text("⛔ У вас нет прав для использования этой команды.")
        return
    
    stats_message = """
📊 <b>Статистика A&A Design Bot v3.0</b>

🎨 <b>Дизайн:</b>
✅ Modern Liquid Glass
✅ Bottom Navigation
✅ Floating Logo

📱 <b>Функции:</b>
✅ Интерактивная 3D книга (18 страниц)
✅ Карта типографий (8 городов)
✅ Система заказов
✅ Аналитика взаимодействий
✅ Haptic обратная связь

🗺 <b>Типографии:</b>
Москва • СПб • Казань • Екатеринбург
Новосибирск • Н.Новгород • Самара • Ростов

🛍 <b>Услуги:</b>
• Размеры S/M/L/XL (3800-7800₽)
• Travel Book (3800₽)
• Постер (2000₽)
• Express (9800₽)
• Готовые шаблоны (2800₽)

<b>Веб-приложение:</b> {url}
<b>Версия:</b> 3.0 - Liquid Glass Edition
"""
    
    await update.message.reply_text(
        stats_message.format(url=WEB_APP_URL),
        parse_mode='HTML'
    )

# Команда broadcast (только для админа)
async def broadcast_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отправляет сообщение всем пользователям (только для админа)"""
    if update.message.from_user.id != ADMIN_ID:
        await update.message.reply_text("⛔ У вас нет прав для использования этой команды.")
        return
    
    await update.message.reply_text(
        "📢 <b>Функция broadcast</b>\n\n"
        "Для массовой рассылки необходимо добавить базу данных пользователей.\n"
        "В текущей версии эта функция не реализована.",
        parse_mode='HTML'
    )

def main():
    """Запуск бота"""
    logger.info(f"🚀 Starting A&A Design Bot v3.0 - Liquid Glass Edition")
    logger.info(f"🔑 Bot token: {BOT_TOKEN[:10]}...")
    logger.info(f"🌐 Web App URL: {WEB_APP_URL}")
    logger.info(f"👤 Admin ID: {ADMIN_ID}")
    
    # Создаем приложение
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Регистрируем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("contacts", contacts_command))
    application.add_handler(CommandHandler("about", about_command))
    application.add_handler(CommandHandler("id", get_id))
    application.add_handler(CommandHandler("stats", stats_command))
    application.add_handler(CommandHandler("broadcast", broadcast_command))
    
    # Обработчик callback кнопок
    application.add_handler(CallbackQueryHandler(button_callback))
    
    # Обработчик данных из Web App
    application.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, web_app_data))
    
    # Обработчик обычных сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Запускаем бота
    logger.info("🎀 A&A Design Bot is starting...")
    print("=" * 60)
    print("🎀 A&A Design Bot v3.0 - Liquid Glass Edition")
    print("=" * 60)
    print(f"📱 Web App: {WEB_APP_URL}")
    print("📖 Features:")
    print("  • Modern Liquid Glass Design")
    print("  • Bottom Navigation")
    print("  • 3D Interactive Book (18 pages)")
    print("  • Yandex Maps (8 cities)")
    print("  • Order System")
    print("  • Analytics")
    print("=" * 60)
    print("✅ Bot is running!")
    print("Press Ctrl+C to stop")
    print("=" * 60)
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()