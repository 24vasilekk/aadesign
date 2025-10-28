# A&A Design - Modern Liquid Glass Web App 🎨

Современное веб-приложение для Telegram Bot магазина кастомных журналов A&A Design с интерактивными 3D кейсами и картой типографий.

![Version](https://img.shields.io/badge/version-3.0-success)
![Design](https://img.shields.io/badge/design-Liquid%20Glass-blue)
![Status](https://img.shields.io/badge/status-Production-green)

---

## 🎨 О проекте

A&A Design специализируется на создании персонализированных журналов - уникальных подарков, которые сохраняют воспоминания в красивой печатной форме.

### ✨ Версия 3.0 - Liquid Glass Edition

Полностью обновленный дизайн в современном стиле **Liquid Glass** (жидкое стекло):
- 🌊 Полупрозрачные элементы с размытием фона
- 💎 Мягкие градиенты и плавные переходы
- 🎯 Минималистичная элегантность
- 📱 Интуитивная bottom navigation в стиле iOS

---

## 🚀 Основные функции

### 📱 **Bottom Navigation**
- Фиксированная нижняя панель в стиле Apple Dashboard
- 4 раздела: Магазин, Кейсы, FAQ, Контакты
- Liquid glass эффект с размытием
- Плавные анимации переходов
- Haptic обратная связь

### 🛍 **Магазин (Shop)**
- 8 услуг в glass-карточках
- Современные SVG иконки
- Размеры S/M/L/XL (3800₽ - 7800₽)
- Travel Book (3800₽)
- Постер (2000₽)
- Express заказ (9800₽)
- Готовые шаблоны (2800₽)
- Прямое перенаправление к менеджеру

### 📖 **3D Интерактивная книга**
- **18 страниц** примеров работ (9 разворотов)
- Реалистичное 3D перелистывание
- Физически точные тени и освещение
- Адаптивность под все устройства
- Плавные CSS3 анимации
- Клик/тап для перелистывания

### 🗺 **Карта типографий** ⭐ NEW
- Интеграция с **Яндекс.Картами**
- **8 городов России:**
  - Москва
  - Санкт-Петербург
  - Казань
  - Екатеринбург
  - Новосибирск
  - Нижний Новгород
  - Самара
  - Ростов-на-Дону
- Интерактивные метки на карте
- Кнопки выбора города
- **Функции:**
  - Копирование адреса типографии
  - Построение маршрута (Яндекс.Карты)
  - Zoom на выбранный город
  - Glass-карточка с информацией

### ❓ **FAQ**
- Accordion в glass-стиле
- Ответы на частые вопросы
- Информация о журналах
- Процесс заказа

### 👤 **Контакты**
- Glass-карточки для каждого контакта
- Telegram менеджер (@aadesignmagg)
- Telegram канал (@aadesignmag)
- Режим работы: 10:00-20:00 МСК
- Статистика: 100+ клиентов с 2023 года

---

## 📂 Структура проекта

```
aadesign-web/
├── index.html              # Главная страница (Liquid Glass)
├── css/
│   └── styles.css          # Modern CSS с glass-эффектами
├── js/
│   └── main.js             # Модульный JavaScript
├── assets/
│   ├── icons/
│   │   └── favicon.png     # Иконка сайта
│   └── images/
│       ├── logo.png        # Логотип (floating)
│       └── cases/          # 19 PNG для 3D книги
│           ├── cover.png
│           ├── page-1.png
│           ├── page-2.png
│           └── ... (до page-18.png)
├── bot.py                  # Telegram Bot с аналитикой
├── package.json            # Настройки проекта
├── .gitignore              # Игнорируемые файлы
└── README.md               # Документация
```

---

## 🎨 Дизайн система

### Цветовая палитра

```css
--primary-pink: #FFB5C5      /* Основной розовый */
--accent-red: #F01030        /* Акцентный красный */
--light-pink: #FFF0F3        /* Светло-розовый фон */
--black: #1a1a1a             /* Текст */
--white: #ffffff             /* Белый */

/* Glass эффекты */
--glass-bg: rgba(255, 255, 255, 0.7)
--glass-border: rgba(255, 189, 200, 0.3)
--glass-shadow: 0 8px 32px rgba(240, 16, 48, 0.1)
```

### Типографика
- Основной шрифт: San Francisco (Apple System Font)
- Заголовки: 700 weight
- Текст: 400-600 weight
- Адаптивные размеры

### Компоненты
- **Glass Cards** - полупрозрачные карточки
- **Bottom Nav** - фиксированная навигация
- **Floating Logo** - плавающий логотип
- **3D Book** - интерактивная книга
- **Map** - Яндекс.Карты
- **Buttons** - кнопки с градиентами

---

## 🛠 Технологии

### Frontend
- **HTML5** - семантическая разметка
- **CSS3** - modern features:
  - `backdrop-filter` для glass-эффекта
  - CSS Grid & Flexbox
  - Custom Properties (переменные)
  - 3D Transforms
  - Animations & Transitions
- **Vanilla JavaScript** - модульная архитектура
- **Telegram Web App API** - интеграция с Telegram
- **Yandex Maps API** - интерактивная карта

### Backend
- **Python 3.10+**
- **python-telegram-bot** - Telegram Bot API
- **JSON** - обмен данными

### Design
- **Liquid Glass** aesthetic
- **Mobile-first** подход
- **iOS-inspired** UI/UX
- **Haptic feedback**

---

## 📱 Адаптивность

### Desktop (>768px)
- 3-4 колонки для карточек
- Полноразмерная карта
- Расширенные glass-эффекты

### Tablet (768px)
- 2 колонки
- Адаптированная навигация
- Оптимизированные размеры

### Mobile (<480px)
- 1-2 колонки
- Компактные карточки
- Touch-оптимизация
- Bottom navigation

---

## 🚀 Установка и запуск

### Требования
- Python 3.10+
- Node.js 16+ (опционально, для dev server)
- Yandex Maps API Key

### 1. Клонирование репозитория
```bash
git clone https://github.com/aadesign/web-app.git
cd web-app
```

### 2. Настройка Telegram Bot

#### Установка зависимостей:
```bash
pip install python-telegram-bot
```

#### Настройка переменных окружения:
```bash
export BOT_TOKEN="your_bot_token"
export WEB_APP_URL="https://aadesign.store/"
export ADMIN_ID="your_admin_id"
```

#### Запуск бота:
```bash
python bot.py
```

### 3. Настройка Web App

#### Обновите Yandex Maps API Key в `index.html`:
```html
<script src="https://api-maps.yandex.ru/2.1/?apikey=YOUR_API_KEY&lang=ru_RU"></script>
```

#### Загрузите изображения для 3D книги:
- Формат: PNG
- Размер: 400px × 560px (рекомендуемый)
- Количество: 19 файлов (cover.png + page-1.png до page-18.png)
- Путь: `assets/images/cases/`

#### Разместите файлы на веб-сервере:
```bash
# Пример с Nginx
sudo cp -r * /var/www/html/aadesign/

# Или используйте serve для разработки
npx serve -s . -l 3000
```

---

## 🔧 Конфигурация

### Добавление новых типографий

Отредактируйте `js/main.js` → `TypographyMap.typographies`:

```javascript
'new_city': {
    name: 'Название города',
    coords: [широта, долгота],
    address: 'Полный адрес типографии',
    zoom: 13
}
```

### Изменение цен

Отредактируйте `index.html` → секция Shop → `.card-price`

### Обновление контактов

Отредактируйте:
- `index.html` → секция Contacts
- `bot.py` → константы с контактами

---

## 📊 Аналитика

### Отслеживаемые события:
- ✅ Переходы между разделами
- ✅ Клики по кнопкам заказа
- ✅ Перелистывание 3D книги
- ✅ Выбор города на карте
- ✅ Копирование адреса
- ✅ Построение маршрута
- ✅ Клики по контактам
- ✅ Время сессии
- ✅ Производительность

### Просмотр аналитики:
```bash
# В консоли браузера
AADesignApp.Analytics.getSessionSummary()
```

---

## 🎯 Особенности реализации

### 3D Книга
- **18 страниц** = 9 разворотов
- Состояния: 0 (закрыто) → 1-9 (развороты) → 0 (закрыто)
- CSS 3D transforms с `preserve-3d`
- Плавные transitions с cubic-bezier
- Адаптивные размеры

### Liquid Glass
- `backdrop-filter: blur(10px) saturate(180%)`
- Полупрозрачные фоны: `rgba(255, 255, 255, 0.7)`
- Мягкие тени: `0 8px 32px rgba(...)`
- Плавные градиенты

### Bottom Navigation
- `position: fixed; bottom: 0`
- Адаптивная высота: `70px`
- Активная кнопка с индикатором сверху
- Haptic feedback при нажатии

### Yandex Maps
- API v2.1
- Кастомные метки (красные)
- Popup с информацией
- Построение маршрутов
- Адаптивный контейнер

---

## 🐛 Известные проблемы

1. **Safari < 14**: ограниченная поддержка `backdrop-filter`
   - Решение: graceful degradation с обычным фоном

2. **iOS < 12**: могут быть проблемы с 3D transforms
   - Решение: упрощенная анимация для старых версий

3. **Медленный интернет**: карта может грузиться долго
   - Решение: показывать loading state

---

## 📝 TODO

- [ ] Добавить базу данных пользователей
- [ ] Реализовать broadcast-рассылки
- [ ] Добавить корзину с несколькими товарами
- [ ] Интеграция с платежными системами
- [ ] PWA support (offline mode)
- [ ] Больше городов на карте
- [ ] A/B тестирование дизайна
- [ ] Мультиязычность (EN, ES)

---

## 🔒 Безопасность

- ✅ Использование переменных окружения для токенов
- ✅ Валидация входящих данных
- ✅ Обработка ошибок с логированием
- ✅ Защита от XSS атак
- ✅ HTTPS обязателен для Web App

---

## 📞 Контакты

- **Менеджер**: [@aadesignmagg](https://t.me/aadesignmagg)
- **Канал**: [@aadesignmag](https://t.me/aadesignmag)
- **Email**: info@aadesign.store
- **Сайт**: https://aadesign.store

---

## 📄 Лицензия

© 2024 A&A Design. Создаем журналы с любовью 🎀

---

## 🙏 Благодарности

- Telegram Web App API
- Yandex Maps API
- Apple Design Guidelines
- Modern CSS Community

---

## 🚀 Changelog

### v3.0.0 - Liquid Glass Edition (2024)
- ✨ Полностью новый дизайн в стиле Liquid Glass
- ✨ Bottom Navigation в стиле iOS
- ✨ Floating Logo
- ✨ Интеграция Яндекс.Карт с 8 городами
- ✨ Улучшенная 3D книга (18 страниц)
- ✨ Расширенная аналитика
- ✨ Haptic feedback
- 🐛 Исправлены баги с навигацией
- ⚡ Улучшена производительность

### v2.1.0 - 3D Books Edition (2023)
- ✨ Добавлены интерактивные 3D книги
- ✨ 4 детализированных кейса
- ✨ Модульная JavaScript архитектура
- ✨ Telegram Bot интеграция

### v2.0.0 - Initial Release (2023)
- 🎉 Первый релиз
- 📱 Telegram Web App
- 🛍 Система заказов
- 📖 Базовые кейсы

---

**Готово к запуску! 🚀**

Интерактивная 3D книга + карта типографий + liquid glass дизайн = современное веб-приложение нового поколения! ✨📖🗺