/**
 * A&A Design - Custom Journals
 * Main JavaScript File v3.1 - UPDATED
 * Features: Bottom Nav, Yandex Maps, 3D Books, Glass UI
 */

// ================================
// Telegram Web App Initialization
// ================================
const TelegramApp = {
    tg: null,
    
    init() {
        if (window.Telegram && window.Telegram.WebApp) {
            this.tg = window.Telegram.WebApp;
            this.tg.ready();
            this.tg.expand();
            this.setupMainButton();
            this.setThemeColors();
        }
    },
    
    setupMainButton() {
        if (this.tg) {
            this.tg.MainButton.text = "Оформить заказ";
            this.tg.MainButton.color = "#F01030";
            this.tg.MainButton.textColor = "#ffffff";
        }
    },
    
    setThemeColors() {
        if (this.tg) {
            this.tg.setHeaderColor('#F01030');
            this.tg.setBackgroundColor('#ffffff');
        }
    },
    
    sendData(data) {
        if (this.tg) {
            this.tg.sendData(JSON.stringify(data));
        }
    },
    
    showAlert(message) {
        if (this.tg) {
            this.tg.showAlert(message);
        } else {
            alert(message);
        }
    },
    
    showConfirm(message, callback) {
        if (this.tg) {
            this.tg.showConfirm(message, callback);
        } else {
            const result = confirm(message);
            callback(result);
        }
    },
    
    hapticFeedback(type = 'light') {
        if (this.tg && this.tg.HapticFeedback) {
            switch(type) {
                case 'light':
                    this.tg.HapticFeedback.impactOccurred('light');
                    break;
                case 'medium':
                    this.tg.HapticFeedback.impactOccurred('medium');
                    break;
                case 'heavy':
                    this.tg.HapticFeedback.impactOccurred('heavy');
                    break;
                case 'success':
                    this.tg.HapticFeedback.notificationOccurred('success');
                    break;
                case 'warning':
                    this.tg.HapticFeedback.notificationOccurred('warning');
                    break;
                case 'error':
                    this.tg.HapticFeedback.notificationOccurred('error');
                    break;
            }
        }
    },
    
    openLink(url) {
        if (this.tg) {
            this.tg.openTelegramLink(url);
        } else {
            window.open(url, '_blank');
        }
    }
};

// ================================
// Bottom Navigation System
// ================================
const Navigation = {
    currentSection: 'shop',
    
    init() {
        this.setupBottomNav();
        this.updateActiveSection('shop');
        this.setupScrollBehavior();
    },
    
    setupBottomNav() {
        const navItems = document.querySelectorAll('.nav-item');
        
        navItems.forEach(item => {
            item.addEventListener('click', (e) => {
                e.preventDefault();
                const targetSection = item.dataset.section;
                this.navigateTo(targetSection);
                TelegramApp.hapticFeedback('light');
            });
        });
    },
    
    navigateTo(sectionId) {
        if (this.currentSection !== sectionId) {
            // Close all books when leaving cases section
            if (this.currentSection === 'cases' && window.Books3D) {
                Books3D.closeAllBooks();
            }
            
            this.currentSection = sectionId;
            this.updateActiveSection(sectionId);
            this.scrollToTop();
            
            // Track navigation
            Analytics.track('navigation', { to: sectionId });
        }
    },
    
    updateActiveSection(sectionId) {
        // Update nav items
        document.querySelectorAll('.nav-item').forEach(item => {
            item.classList.toggle('active', item.dataset.section === sectionId);
        });
        
        // Update sections
        document.querySelectorAll('.section').forEach(section => {
            const isActive = section.id === sectionId;
            section.classList.toggle('active', isActive);
            
            if (isActive) {
                section.style.animation = 'none';
                setTimeout(() => {
                    section.style.animation = 'fadeInUp 0.5s ease forwards';
                }, 10);
            }
        });
    },
    
    scrollToTop() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    },
    
    setupScrollBehavior() {
        let lastScroll = 0;
        
        window.addEventListener('scroll', Utils.debounce(() => {
            const currentScroll = window.pageYOffset;
            
            // Add scrolled class to body for logo animation
            if (currentScroll > 50) {
                document.body.classList.add('scrolled');
            } else {
                document.body.classList.remove('scrolled');
            }
            
            lastScroll = currentScroll;
        }, 100));
    }
};

// ================================
// 3D Books Functionality - 18 PAGES
// ================================
const Books3D = {
    init() {
        this.setupBooks();
    },
    
    setupBooks() {
        const bookContainers = document.querySelectorAll('.book-container');
        
        bookContainers.forEach(container => {
            const book = container.querySelector('.book');
            
            // Click handler
            book.addEventListener('click', (e) => {
                e.preventDefault();
                this.flipBook(container);
                TelegramApp.hapticFeedback('medium');
            });
            
            // Touch handler
            let touchStartTime = 0;
            
            book.addEventListener('touchstart', (e) => {
                touchStartTime = Date.now();
            });
            
            book.addEventListener('touchend', (e) => {
                const touchDuration = Date.now() - touchStartTime;
                if (touchDuration < 500) {
                    e.preventDefault();
                    this.flipBook(container);
                    TelegramApp.hapticFeedback('medium');
                }
            });
            
            // Keyboard handler
            book.setAttribute('tabindex', '0');
            book.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    this.flipBook(container);
                    TelegramApp.hapticFeedback('medium');
                }
            });
            
            // Initialize state
            container.dataset.state = '0';
        });
    },
    
    flipBook(container) {
        const currentState = parseInt(container.dataset.state || '0');
        let nextState;
        let actionName;
        
        // State cycle: 0 -> 1 -> 2 -> ... -> 9 -> 0
        if (currentState === 0) {
            nextState = 1;
            actionName = 'open_page_1-2';
        } else if (currentState >= 1 && currentState < 9) {
            nextState = currentState + 1;
            actionName = `open_page_${(currentState * 2) + 1}-${(currentState * 2) + 2}`;
        } else if (currentState === 9) {
            nextState = 0;
            actionName = 'close';
        } else {
            nextState = 0;
            actionName = 'reset';
        }
        
        this.updateBookState(container, nextState);
        
        // Track analytics
        Analytics.track('book_flip', {
            book: container.dataset.book,
            action: actionName,
            state: nextState
        });
        
        // Send to Telegram on first open
        if (nextState === 1) {
            TelegramApp.sendData({
                action: 'book_flip',
                data: {
                    book: container.dataset.book,
                    action: 'open'
                }
            });
        }
    },
    
    updateBookState(container, state) {
        // Remove all state classes
        for (let i = 0; i <= 9; i++) {
            container.classList.remove(`state-${i}`);
        }
        
        // Hide all spreads
        const spreads = container.querySelectorAll('.book-spread');
        spreads.forEach(spread => {
            spread.classList.remove('active');
            spread.style.opacity = '0';
            spread.style.pointerEvents = 'none';
            spread.style.visibility = 'hidden';
        });
        
        // Apply new state
        setTimeout(() => {
            container.classList.add(`state-${state}`);
            container.dataset.state = state.toString();
            
            // Show active spread
            if (state >= 1 && state <= 9) {
                const spread = container.querySelector(`.book-spread-${state}`);
                if (spread) {
                    spread.classList.add('active');
                    spread.style.opacity = '1';
                    spread.style.pointerEvents = 'all';
                    spread.style.visibility = 'visible';
                }
            }
        }, 50);
        
        // Bounce animation
        const book = container.querySelector('.book');
        const originalTransform = book.style.transform;
        book.style.transform = (originalTransform || '') + ' scale(0.95)';
        setTimeout(() => {
            book.style.transform = originalTransform || '';
        }, 150);
    },
    
    closeAllBooks() {
        const bookContainers = document.querySelectorAll('.book-container');
        bookContainers.forEach(container => {
            for (let i = 1; i <= 9; i++) {
                container.classList.remove(`state-${i}`);
            }
            container.classList.add('state-0');
            container.dataset.state = '0';
            
            const spreads = container.querySelectorAll('.book-spread');
            spreads.forEach(spread => {
                spread.classList.remove('active');
                spread.style.opacity = '0';
                spread.style.pointerEvents = 'none';
                spread.style.visibility = 'hidden';
            });
        });
    }
};

// ================================
// Shop Functionality - FIXED MESSAGES
// ================================
const Shop = {
    init() {
        this.setupOrderButtons();
    },
    
    setupOrderButtons() {
        const orderButtons = document.querySelectorAll('.order-btn');
        
        orderButtons.forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                const card = btn.closest('.service-card');
                const productType = card.dataset.product;
                this.handleOrder(productType, card);
                TelegramApp.hapticFeedback('success');
            });
        });
    },
    
    handleOrder(productType, card) {
        const title = card.querySelector('.card-title')?.textContent.trim() || '';
        const price = card.querySelector('.card-price')?.textContent.trim() || '';
        
        // Generate personalized message based on product type
        const messages = {
            'size-s': `Здравствуйте! Хочу заказать журнал размера S за ${price}. Расскажите, пожалуйста, подробнее о процессе.`,
            'size-m': `Здравствуйте! Интересует журнал размера M за ${price}. Как оформить заказ?`,
            'size-l': `Привет! Хотел бы заказать журнал размера L за ${price}. Что нужно для начала?`,
            'size-xl': `Добрый день! Интересует журнал размера XL за ${price}. Можете рассказать подробнее?`,
            'travel-book': `Здравствуйте! Хочу заказать Travel Book за ${price}. Какие материалы нужны?`,
            'poster': `Здравствуйте! Интересует постер за ${price}. Рамка входит в стоимость?`,
            'express': `Добрый день! Нужен срочный заказ EXPRESS за ${price}. Какие сроки?`,
            'template': `Привет! Интересует готовый шаблон за ${price}. Можно посмотреть варианты?`
        };
        
        const managerMessage = messages[productType] || `Здравствуйте! Хочу заказать ${title} за ${price}.`;
        const managerUrl = `https://t.me/aadesignmagg?text=${encodeURIComponent(managerMessage)}`;
        
        // Send data to Telegram Bot
        const orderData = {
            action: 'order',
            service: title,
            price: price,
            product: productType,
            timestamp: new Date().toISOString()
        };
        
        TelegramApp.sendData(orderData);
        
        // Open manager chat
        TelegramApp.openLink(managerUrl);
        
        // Track analytics
        Analytics.track('order', { product: productType, price: price });
    }
};

// ================================
// Yandex Maps Integration - ТОЛЬКО МОСКВА И ОБНИНСК
// ================================
const TypographyMap = {
    map: null,
    currentCity: null,
    
    // Typography locations - ТОЛЬКО 2 ГОРОДА
    typographies: {
        'moscow': {
            name: 'Москва',
            coords: [55.751244, 37.618423],
            address: 'ул. Тверская, д. 12, стр. 1, Москва, 125009',
            zoom: 12
        },
        'obninsk': {
            name: 'Обнинск',
            coords: [55.095833, 36.606944],
            address: 'пр. Ленина, д. 103, Обнинск, Калужская обл., 249034',
            zoom: 13
        }
    },
    
    init() {
        // Check if we're on FAQ section and Yandex Maps API is loaded
        if (typeof ymaps !== 'undefined') {
            ymaps.ready(() => {
                this.initMap();
                this.setupInfoCard();
            });
        } else {
            console.warn('Yandex Maps API not loaded');
        }
    },
    
    initMap() {
        const mapContainer = document.getElementById('map');
        if (!mapContainer) return;
        
        // Create map centered between Moscow and Obninsk
        this.map = new ymaps.Map('map', {
            center: [55.4, 37.1], // Between Moscow and Obninsk
            zoom: 8,
            controls: ['zoomControl', 'geolocationControl']
        });
        
        // Add placemarks for typographies
        Object.entries(this.typographies).forEach(([key, typography]) => {
            const placemark = new ymaps.Placemark(
                typography.coords,
                {
                    balloonContentHeader: typography.name,
                    balloonContentBody: typography.address,
                    hintContent: typography.name
                },
                {
                    preset: 'islands#redDotIcon',
                    iconColor: '#F01030'
                }
            );
            
            // Click handler for placemark
            placemark.events.add('click', () => {
                this.showTypographyInfo(key);
                TelegramApp.hapticFeedback('light');
            });
            
            this.map.geoObjects.add(placemark);
        });
    },
    
    showTypographyInfo(cityKey) {
        const typography = this.typographies[cityKey];
        if (!typography) return;
        
        this.currentCity = cityKey;
        
        const infoCard = document.getElementById('typography-info');
        const cityElement = document.getElementById('typography-city');
        const addressElement = document.getElementById('typography-address');
        
        if (infoCard && cityElement && addressElement) {
            cityElement.textContent = typography.name;
            addressElement.textContent = typography.address;
            infoCard.style.display = 'block';
            
            // Smooth show animation
            setTimeout(() => {
                infoCard.style.animation = 'fadeInUp 0.4s ease forwards';
            }, 10);
        }
        
        // Zoom to selected city
        if (this.map) {
            this.map.setCenter(typography.coords, typography.zoom, {
                duration: 500
            });
        }
        
        // Track analytics
        Analytics.track('map_city_select', { city: typography.name });
    },
    
    setupInfoCard() {
        // Close button
        const closeBtn = document.getElementById('close-info-btn');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => {
                const infoCard = document.getElementById('typography-info');
                if (infoCard) {
                    infoCard.style.display = 'none';
                }
                TelegramApp.hapticFeedback('light');
            });
        }
        
        // Copy address button
        const copyBtn = document.getElementById('copy-address-btn');
        if (copyBtn) {
            copyBtn.addEventListener('click', () => {
                this.copyAddress();
            });
        }
        
        // Show route button
        const routeBtn = document.getElementById('show-route-btn');
        if (routeBtn) {
            routeBtn.addEventListener('click', () => {
                this.showRoute();
            });
        }
    },
    
    copyAddress() {
        if (!this.currentCity) return;
        
        const typography = this.typographies[this.currentCity];
        const address = typography.address;
        
        // Try to copy to clipboard
        if (navigator.clipboard && navigator.clipboard.writeText) {
            navigator.clipboard.writeText(address).then(() => {
                TelegramApp.showAlert('Адрес скопирован в буфер обмена');
                TelegramApp.hapticFeedback('success');
                Analytics.track('address_copied', { city: typography.name });
            }).catch(err => {
                console.error('Failed to copy:', err);
                this.fallbackCopy(address);
            });
        } else {
            this.fallbackCopy(address);
        }
    },
    
    fallbackCopy(text) {
        // Fallback for older browsers
        const textArea = document.createElement('textarea');
        textArea.value = text;
        textArea.style.position = 'fixed';
        textArea.style.left = '-999999px';
        document.body.appendChild(textArea);
        textArea.select();
        
        try {
            document.execCommand('copy');
            TelegramApp.showAlert('Адрес скопирован');
            TelegramApp.hapticFeedback('success');
        } catch (err) {
            TelegramApp.showAlert('Не удалось скопировать адрес');
        }
        
        document.body.removeChild(textArea);
    },
    
    showRoute() {
        if (!this.currentCity) return;
        
        const typography = this.typographies[this.currentCity];
        
        // Open Yandex Maps with route
        const coords = typography.coords.join(',');
        const mapsUrl = `https://yandex.ru/maps/?rtext=~${coords}&rtt=auto`;
        
        window.open(mapsUrl, '_blank');
        
        TelegramApp.hapticFeedback('light');
        Analytics.track('route_requested', { city: typography.name });
    }
};

// ================================
// FAQ Accordion
// ================================
const FAQ = {
    init() {
        this.setupAccordion();
    },
    
    setupAccordion() {
        const faqItems = document.querySelectorAll('.faq-item');
        
        faqItems.forEach(item => {
            const question = item.querySelector('.faq-question');
            
            question.addEventListener('click', () => {
                const isActive = item.classList.contains('active');
                
                // Close all other items
                faqItems.forEach(otherItem => {
                    if (otherItem !== item) {
                        otherItem.classList.remove('active');
                    }
                });
                
                // Toggle current item
                if (!isActive) {
                    item.classList.add('active');
                    TelegramApp.hapticFeedback('light');
                    Analytics.track('faq_open', { 
                        question: question.textContent.trim() 
                    });
                } else {
                    item.classList.remove('active');
                }
            });
        });
    }
};

// ================================
// Contact Links
// ================================
const Contacts = {
    init() {
        this.setupLinks();
    },
    
    setupLinks() {
        const contactCards = document.querySelectorAll('.contact-card');
        
        contactCards.forEach(card => {
            card.addEventListener('click', (e) => {
                const href = card.getAttribute('href');
                if (href) {
                    TelegramApp.hapticFeedback('light');
                    
                    const platform = href.includes('aadesignmagg') ? 'manager' : 'channel';
                    
                    Analytics.track('contact_click', {
                        platform: platform,
                        url: href
                    });
                    
                    TelegramApp.sendData({
                        action: 'contact_click',
                        platform: platform,
                        url: href,
                        timestamp: new Date().toISOString()
                    });
                }
            });
        });
    }
};

// ================================
// Animations & Effects
// ================================
const Animations = {
    init() {
        this.setupScrollAnimations();
        this.setupLazyLoading();
    },
    
    setupScrollAnimations() {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                }
            });
        }, observerOptions);
        
        // Observe elements
        document.querySelectorAll('.service-card, .book-container, .faq-item, .contact-card').forEach(el => {
            el.classList.add('fade-in');
            observer.observe(el);
        });
    },
    
    setupLazyLoading() {
        if ('loading' in HTMLImageElement.prototype) {
            // Browser supports native lazy loading
            const images = document.querySelectorAll('img[loading="lazy"]');
            images.forEach(img => {
                if (img.dataset.src) {
                    img.src = img.dataset.src;
                }
            });
        } else {
            // Fallback for browsers that don't support lazy loading
            const imageObserver = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        if (img.dataset.src) {
                            img.src = img.dataset.src;
                            img.removeAttribute('data-src');
                            imageObserver.unobserve(img);
                        }
                    }
                });
            });
            
            document.querySelectorAll('img[data-src]').forEach(img => {
                imageObserver.observe(img);
            });
        }
    }
};

// ================================
// Utilities
// ================================
const Utils = {
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },
    
    throttle(func, limit) {
        let inThrottle;
        return function(...args) {
            if (!inThrottle) {
                func.apply(this, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    },
    
    formatPrice(price) {
        return price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ' ');
    },
    
    getDeviceType() {
        const ua = navigator.userAgent;
        if (/(tablet|ipad|playbook|silk)|(android(?!.*mobi))/i.test(ua)) {
            return 'tablet';
        }
        if (/Mobile|iP(hone|od)|Android|BlackBerry|IEMobile|Kindle|Silk-Accelerated|(hpw|web)OS|Opera M(obi|ini)/.test(ua)) {
            return 'mobile';
        }
        return 'desktop';
    },
    
    isInViewport(element) {
        const rect = element.getBoundingClientRect();
        return (
            rect.top >= 0 &&
            rect.left >= 0 &&
            rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
            rect.right <= (window.innerWidth || document.documentElement.clientWidth)
        );
    }
};

// ================================
// Analytics
// ================================
const Analytics = {
    events: [],
    sessionStart: Date.now(),
    
    track(eventName, eventData = {}) {
        const event = {
            name: eventName,
            data: eventData,
            timestamp: new Date().toISOString(),
            device: Utils.getDeviceType(),
            url: window.location.href,
            sessionDuration: Math.floor((Date.now() - this.sessionStart) / 1000)
        };
        
        this.events.push(event);
        
        // Send important events to Telegram
        const importantEvents = ['page_view', 'order', 'contact_click', 'map_city_select', 'route_requested'];
        if (importantEvents.includes(eventName)) {
            TelegramApp.sendData({
                action: 'analytics',
                event: event
            });
        }
        
        console.log('📊 Analytics:', event);
    },
    
    trackPageView(page) {
        this.track('page_view', { page });
    },
    
    trackClick(element, label) {
        this.track('click', { element, label });
    },
    
    getSessionDuration() {
        return Math.floor((Date.now() - this.sessionStart) / 1000);
    },
    
    getSessionSummary() {
        return {
            duration: this.getSessionDuration(),
            events: this.events.length,
            device: Utils.getDeviceType(),
            topEvents: this.getTopEvents()
        };
    },
    
    getTopEvents() {
        const eventCounts = {};
        this.events.forEach(event => {
            eventCounts[event.name] = (eventCounts[event.name] || 0) + 1;
        });
        return Object.entries(eventCounts)
            .sort((a, b) => b[1] - a[1])
            .slice(0, 5);
    }
};

// ================================
// App Initialization
// ================================
const App = {
    init() {
        console.log('🎨 A&A Design Web App v3.1 - UPDATED');
        console.log('🚀 Initializing...');
        
        // Initialize core modules
        TelegramApp.init();
        Navigation.init();
        Shop.init();
        Books3D.init();
        FAQ.init();
        Contacts.init();
        Animations.init();
        
        // Initialize map (will check if on correct section)
        setTimeout(() => {
            TypographyMap.init();
        }, 500);
        
        // Track initial page view
        Analytics.trackPageView('shop');
        
        // Setup error handlers
        this.setupErrorHandler();
        this.monitorPerformance();
        this.checkConnection();
        
        // Setup beforeunload
        this.setupBeforeUnload();
        
        console.log('✅ App Ready!');
        console.log('📱 Device:', Utils.getDeviceType());
        console.log('📖 Features: Bottom Nav, 3D Books (18 pages), Yandex Maps (2 cities), Glass UI');
    },
    
    setupErrorHandler() {
        window.addEventListener('error', (e) => {
            console.error('❌ App Error:', e.message);
            Analytics.track('error', {
                message: e.message,
                source: e.filename,
                line: e.lineno,
                column: e.colno
            });
        });
        
        window.addEventListener('unhandledrejection', (e) => {
            console.error('❌ Unhandled Promise Rejection:', e.reason);
            Analytics.track('promise_rejection', {
                reason: String(e.reason)
            });
        });
    },
    
    monitorPerformance() {
        if ('performance' in window) {
            window.addEventListener('load', () => {
                setTimeout(() => {
                    const perfData = performance.getEntriesByType('navigation')[0];
                    if (perfData) {
                        Analytics.track('performance', {
                            loadTime: Math.round(perfData.loadEventEnd - perfData.fetchStart),
                            domReady: Math.round(perfData.domContentLoadedEventEnd - perfData.fetchStart),
                            resources: performance.getEntriesByType('resource').length
                        });
                    }
                }, 0);
            });
        }
    },
    
    checkConnection() {
        if (!navigator.onLine) {
            TelegramApp.showAlert('Нет подключения к интернету. Некоторые функции могут быть недоступны.');
        }
        
        window.addEventListener('online', () => {
            console.log('🌐 Connection restored');
            Analytics.track('connection_restored');
        });
        
        window.addEventListener('offline', () => {
            TelegramApp.showAlert('Подключение к интернету потеряно');
            Analytics.track('connection_lost');
        });
    },
    
    setupBeforeUnload() {
        window.addEventListener('beforeunload', () => {
            // Send session summary
            const summary = Analytics.getSessionSummary();
            Analytics.track('session_end', summary);
            
            console.log('📊 Session Summary:', summary);
        });
    }
};

// ================================
// Start App when DOM is ready
// ================================
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => App.init());
} else {
    App.init();
}

// ================================
// Export for debugging (development only)
// ================================
if (typeof window !== 'undefined') {
    window.AADesignApp = {
        App,
        TelegramApp,
        Navigation,
        Shop,
        Books3D,
        TypographyMap,
        FAQ,
        Contacts,
        Analytics,
        Animations,
        Utils
    };
}