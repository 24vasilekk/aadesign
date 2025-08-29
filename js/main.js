/**
 * A&A Design - Custom Journals
 * Main JavaScript File
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
            this.setupBackButton();
            this.setThemeColors();
        }
    },
    
    setupMainButton() {
        if (this.tg) {
            this.tg.MainButton.text = "Оформить заказ";
            this.tg.MainButton.color = "#F00B0D";
            this.tg.MainButton.textColor = "#ffffff";
        }
    },
    
    setupBackButton() {
        if (this.tg && this.tg.BackButton) {
            this.tg.BackButton.onClick(() => {
                Navigation.goBack();
            });
        }
    },
    
    setThemeColors() {
        if (this.tg) {
            this.tg.setHeaderColor('#F00B0D');
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
    }
};

// ================================
// Navigation System
// ================================
const Navigation = {
    currentSection: 'shop',
    history: ['shop'],
    
    init() {
        this.setupTabs();
        this.setupSwipeNavigation();
        this.updateActiveSection('shop');
    },
    
    setupTabs() {
        const tabs = document.querySelectorAll('.nav-tab');
        tabs.forEach(tab => {
            tab.addEventListener('click', (e) => {
                e.preventDefault();
                const targetSection = tab.dataset.section;
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
            
            this.history.push(sectionId);
            this.updateActiveSection(sectionId);
            this.currentSection = sectionId;
            this.scrollToTop();
            this.updateBackButton();
        }
    },
    
    goBack() {
        if (this.history.length > 1) {
            this.history.pop();
            const previousSection = this.history[this.history.length - 1];
            this.updateActiveSection(previousSection);
            this.currentSection = previousSection;
            this.updateBackButton();
        }
    },
    
    updateActiveSection(sectionId) {
        // Update tabs
        document.querySelectorAll('.nav-tab').forEach(tab => {
            tab.classList.toggle('active', tab.dataset.section === sectionId);
        });
        
        // Update sections
        document.querySelectorAll('.section').forEach(section => {
            section.classList.toggle('active', section.id === sectionId);
        });
        
        // Animate section entrance
        const activeSection = document.getElementById(sectionId);
        if (activeSection) {
            activeSection.style.animation = 'none';
            setTimeout(() => {
                activeSection.style.animation = 'fadeInUp 0.5s ease forwards';
            }, 10);
        }
    },
    
    updateBackButton() {
        if (TelegramApp.tg && TelegramApp.tg.BackButton) {
            if (this.history.length > 1) {
                TelegramApp.tg.BackButton.show();
            } else {
                TelegramApp.tg.BackButton.hide();
            }
        }
    },
    
    scrollToTop() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    },
    
    setupSwipeNavigation() {
        let touchStartX = 0;
        let touchEndX = 0;
        let touchStartY = 0;
        let touchEndY = 0;
        
        document.addEventListener('touchstart', (e) => {
            touchStartX = e.changedTouches[0].screenX;
            touchStartY = e.changedTouches[0].screenY;
        });
        
        document.addEventListener('touchend', (e) => {
            touchEndX = e.changedTouches[0].screenX;
            touchEndY = e.changedTouches[0].screenY;
            this.handleSwipe();
        });
        
        this.handleSwipe = () => {
            const swipeThreshold = 80;
            const verticalThreshold = 60;
            
            const horizontalDistance = Math.abs(touchEndX - touchStartX);
            const verticalDistance = Math.abs(touchEndY - touchStartY);
            
            // Только если горизонтальный свайп больше вертикального
            if (horizontalDistance > verticalDistance && horizontalDistance > swipeThreshold) {
                const tabs = ['shop', 'cases', 'reviews', 'faq'];
                const currentIndex = tabs.indexOf(this.currentSection);
                
                if (touchStartX - touchEndX > swipeThreshold) {
                    // Swipe left - next tab
                    if (currentIndex < tabs.length - 1) {
                        this.navigateTo(tabs[currentIndex + 1]);
                    }
                } else if (touchEndX - touchStartX > swipeThreshold) {
                    // Swipe right - previous tab
                    if (currentIndex > 0) {
                        this.navigateTo(tabs[currentIndex - 1]);
                    }
                }
            }
        };
    }
};

// ================================
// 3D Books Functionality
// ================================
const Books3D = {
    init() {
        this.setupBooks();
    },
    
    setupBooks() {
        const bookContainers = document.querySelectorAll('.book-container');
        
        bookContainers.forEach(container => {
            const book = container.querySelector('.book');
            let isFlipped = false;
            
            book.addEventListener('click', (e) => {
                e.preventDefault();
                this.flipBook(container);
                TelegramApp.hapticFeedback('medium');
            });
            
            // Touch events for better mobile interaction
            let touchStartTime = 0;
            
            book.addEventListener('touchstart', (e) => {
                touchStartTime = Date.now();
            });
            
            book.addEventListener('touchend', (e) => {
                const touchDuration = Date.now() - touchStartTime;
                if (touchDuration < 500) { // Quick tap
                    e.preventDefault();
                    this.flipBook(container);
                    TelegramApp.hapticFeedback('medium');
                }
            });
            
            // Keyboard navigation
            book.setAttribute('tabindex', '0');
            book.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    this.flipBook(container);
                    TelegramApp.hapticFeedback('medium');
                }
            });
            
            // Store initial state
            container.dataset.flipped = 'false';
        });
    },
    
    flipBook(container) {
        const isCurrentlyFlipped = container.dataset.flipped === 'true';
        
        if (isCurrentlyFlipped) {
            // Flip back to cover
            container.classList.remove('flipped');
            container.dataset.flipped = 'false';
            
            // Track analytics
            Analytics.track('book_flip', {
                book: container.dataset.book,
                action: 'close'
            });
        } else {
            // Flip to description pages
            container.classList.add('flipped');
            container.dataset.flipped = 'true';
            
            // Track analytics
            Analytics.track('book_flip', {
                book: container.dataset.book,
                action: 'open'
            });
        }
    },
    
    // Auto-close books when switching sections
    closeAllBooks() {
        const bookContainers = document.querySelectorAll('.book-container');
        bookContainers.forEach(container => {
            container.classList.remove('flipped');
            container.dataset.flipped = 'false';
        });
    },
    
    // Demo mode - automatically flip through books
    startDemo() {
        const bookContainers = document.querySelectorAll('.book-container');
        let currentIndex = 0;
        
        const flipNext = () => {
            // Close all books first
            this.closeAllBooks();
            
            // Flip current book
            setTimeout(() => {
                if (bookContainers[currentIndex]) {
                    this.flipBook(bookContainers[currentIndex]);
                }
                
                currentIndex = (currentIndex + 1) % bookContainers.length;
                
                // Schedule next flip
                setTimeout(flipNext, 3000);
            }, 500);
        };
        
        // Start demo after a delay
        setTimeout(flipNext, 2000);
    }
};

// ================================
// Shop Functionality
// ================================
const Shop = {
    cart: [],
    
    init() {
        this.setupOrderButtons();
        this.loadCart();
    },
    
    setupOrderButtons() {
        const orderButtons = document.querySelectorAll('.order-btn');
        orderButtons.forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                const card = btn.closest('.service-card');
                const service = this.extractServiceData(card);
                this.handleOrder(service);
                TelegramApp.hapticFeedback('success');
            });
        });
    },
    
    extractServiceData(card) {
        return {
            title: card.querySelector('.service-title').textContent.trim(),
            price: card.querySelector('.service-price').textContent.trim(),
            details: card.querySelector('.service-details').textContent.trim(),
            time: card.querySelector('.service-time').textContent.trim()
        };
    },
    
    handleOrder(service) {
        // Создаем сообщение для менеджера в зависимости от услуги
        let managerMessage = '';
        const serviceTitle = service.title.toLowerCase();
        
        if (serviceTitle.includes('размер s')) {
            managerMessage = 'Здравствуйте! Хочу заказать журнал размера S (до 12 страниц) за 3799₽. Расскажите, пожалуйста, подробнее о процессе заказа.';
        } else if (serviceTitle.includes('размер m')) {
            managerMessage = 'Здравствуйте! Меня интересует журнал размера M (до 16 страниц) за 4799₽. Как можно оформить заказ?';
        } else if (serviceTitle.includes('размер l')) {
            managerMessage = 'Привет! Хотел бы заказать журнал размера L (до 20 страниц) за 5799₽. Что нужно для начала работы?';
        } else if (serviceTitle.includes('размер xl')) {
            managerMessage = 'Добрый день! Интересует журнал размера XL (до 30 страниц) за 7799₽. Можете рассказать о возможностях?';
        } else if (serviceTitle.includes('travel book')) {
            managerMessage = 'Здравствуйте! Хочу заказать Travel Book на 20 страниц за 3799₽. Какие материалы нужно подготовить?';
        } else if (serviceTitle.includes('express')) {
            managerMessage = 'Добрый день! Мне нужен срочный заказ EXPRESS за 9799₽. Какие сроки и условия?';
        } else if (serviceTitle.includes('готовый вариант')) {
            managerMessage = 'Привет! Интересует готовый вариант журнала за 2799₽. Можно посмотреть доступные шаблоны?';
        } else {
            managerMessage = `Здравствуйте! Хочу заказать ${service.title} за ${service.price}. Расскажите подробнее об услуге.`;
        }
        
        // Открываем диалог с менеджером
        const managerUrl = `https://t.me/cosmeticsourc?text=${encodeURIComponent(managerMessage)}`;
        
        // Отправляем данные в Telegram
        const orderData = {
            action: 'order',
            service: service.title,
            price: service.price,
            details: service.details,
            time: service.time,
            timestamp: new Date().toISOString()
        };
        
        TelegramApp.sendData(orderData);
        
        // Открываем ссылку на менеджера
        if (TelegramApp.tg) {
            TelegramApp.tg.openTelegramLink(managerUrl);
        } else {
            window.open(managerUrl, '_blank');
        }
        
        TelegramApp.hapticFeedback('success');
    },
    
    addToCart(item) {
        this.cart.push(item);
        this.saveCart();
        this.updateCartUI();
    },
    
    removeFromCart(index) {
        this.cart.splice(index, 1);
        this.saveCart();
        this.updateCartUI();
    },
    
    clearCart() {
        this.cart = [];
        this.saveCart();
        this.updateCartUI();
    },
    
    saveCart() {
        try {
            sessionStorage.setItem('aa_design_cart', JSON.stringify(this.cart));
        } catch (e) {
            console.log('Could not save cart');
        }
    },
    
    loadCart() {
        try {
            const saved = sessionStorage.getItem('aa_design_cart');
            if (saved) {
                this.cart = JSON.parse(saved);
                this.updateCartUI();
            }
        } catch (e) {
            console.log('Could not load cart');
        }
    },
    
    updateCartUI() {
        // Update cart counter if you add one to the UI
        const cartCount = this.cart.length;
        if (cartCount > 0 && TelegramApp.tg) {
            TelegramApp.tg.MainButton.text = `Оформить заказ (${cartCount})`;
        }
    },
    
    checkout() {
        if (this.cart.length === 0) {
            TelegramApp.showAlert('Корзина пуста');
            return;
        }
        
        const total = this.calculateTotal();
        const message = `Ваш заказ:\n\n${this.getCartSummary()}\n\nИтого: ${total}₽\n\nОформить заказ?`;
        
        TelegramApp.showConfirm(message, (confirmed) => {
            if (confirmed) {
                this.processCheckout();
            }
        });
    },
    
    calculateTotal() {
        return this.cart.reduce((sum, item) => {
            const price = parseInt(item.price.replace(/[^\d]/g, ''));
            return sum + price;
        }, 0);
    },
    
    getCartSummary() {
        return this.cart.map(item => `• ${item.service} - ${item.price}`).join('\n');
    },
    
    processCheckout() {
        const checkoutData = {
            action: 'checkout',
            cart: this.cart,
            total: this.calculateTotal(),
            timestamp: new Date().toISOString()
        };
        
        TelegramApp.sendData(checkoutData);
        TelegramApp.showAlert('Заказ отправлен! Мы свяжемся с вами в ближайшее время.');
        this.clearCart();
        
        if (TelegramApp.tg) {
            TelegramApp.tg.close();
        }
    }
};

// ================================
// Reviews Slider
// ================================
const ReviewsSlider = {
    currentSlide: 0,
    totalSlides: 3,
    autoPlayInterval: null,
    touchStartX: 0,
    touchEndX: 0,
    
    init() {
        this.setupDots();
        this.setupTouch();
        this.startAutoPlay();
    },
    
    setupDots() {
        const dots = document.querySelectorAll('.dot');
        dots.forEach((dot, index) => {
            dot.addEventListener('click', () => {
                this.goToSlide(index);
                this.stopAutoPlay();
                this.startAutoPlay();
                TelegramApp.hapticFeedback('light');
            });
        });
    },
    
    setupTouch() {
        const slider = document.querySelector('.reviews-slider');
        if (!slider) return;
        
        slider.addEventListener('touchstart', (e) => {
            this.touchStartX = e.changedTouches[0].screenX;
            this.stopAutoPlay();
        });
        
        slider.addEventListener('touchend', (e) => {
            this.touchEndX = e.changedTouches[0].screenX;
            this.handleSwipe();
            this.startAutoPlay();
        });
    },
    
    handleSwipe() {
        const swipeThreshold = 50;
        
        if (this.touchStartX - this.touchEndX > swipeThreshold) {
            this.nextSlide();
        } else if (this.touchEndX - this.touchStartX > swipeThreshold) {
            this.prevSlide();
        }
    },
    
    goToSlide(index) {
        this.currentSlide = index;
        this.updateSlider();
    },
    
    nextSlide() {
        this.currentSlide = (this.currentSlide + 1) % this.totalSlides;
        this.updateSlider();
    },
    
    prevSlide() {
        this.currentSlide = (this.currentSlide - 1 + this.totalSlides) % this.totalSlides;
        this.updateSlider();
    },
    
    updateSlider() {
        const slider = document.getElementById('reviewsSlider');
        const dots = document.querySelectorAll('.dot');
        
        if (slider) {
            slider.style.transform = `translateX(-${this.currentSlide * 100}%)`;
        }
        
        dots.forEach((dot, index) => {
            dot.classList.toggle('active', index === this.currentSlide);
        });
    },
    
    startAutoPlay() {
        this.autoPlayInterval = setInterval(() => {
            this.nextSlide();
        }, 5000);
    },
    
    stopAutoPlay() {
        if (this.autoPlayInterval) {
            clearInterval(this.autoPlayInterval);
        }
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
                
                // Close all items
                faqItems.forEach(otherItem => {
                    otherItem.classList.remove('active');
                });
                
                // Toggle current item
                if (!isActive) {
                    item.classList.add('active');
                    TelegramApp.hapticFeedback('light');
                }
            });
        });
    }
};

// ================================
// Contact Links
// ================================
const Contacts = {
    links: [
        'https://t.me/cosmeticsourc',
        'https://instagram.com/aadesingmag',
        'https://t.me/aadesingmag'
    ],
    
    init() {
        this.setupLinks();
    },
    
    setupLinks() {
        const contactLinks = document.querySelectorAll('.contact-link');
        
        contactLinks.forEach((link, index) => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                
                if (this.links[index]) {
                    TelegramApp.hapticFeedback('light');
                    
                    // Track contact click
                    const contactData = {
                        action: 'contact_click',
                        platform: ['telegram', 'instagram', 'channel'][index],
                        url: this.links[index],
                        timestamp: new Date().toISOString()
                    };
                    
                    TelegramApp.sendData(contactData);
                    
                    // Open link
                    window.open(this.links[index], '_blank');
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
        
        // Add fade-in class to elements
        document.querySelectorAll('.service-card, .case-card').forEach(el => {
            el.classList.add('fade-in');
            observer.observe(el);
        });
    },
    
    setupLazyLoading() {
        const images = document.querySelectorAll('img[data-src]');
        
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.removeAttribute('data-src');
                    observer.unobserve(img);
                }
            });
        });
        
        images.forEach(img => imageObserver.observe(img));
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
    
    track(eventName, eventData = {}) {
        const event = {
            name: eventName,
            data: eventData,
            timestamp: new Date().toISOString(),
            device: Utils.getDeviceType(),
            url: window.location.href
        };
        
        this.events.push(event);
        
        // Send to Telegram if needed
        if (eventName === 'page_view' || eventName === 'order' || eventName === 'contact_click') {
            TelegramApp.sendData({
                action: 'analytics',
                event: event
            });
        }
        
        console.log('Analytics:', event);
    },
    
    trackPageView(page) {
        this.track('page_view', { page });
    },
    
    trackClick(element, label) {
        this.track('click', { element, label });
    },
    
    trackScroll(percentage) {
        this.track('scroll', { percentage });
    },
    
    getSessionDuration() {
        const start = this.events[0]?.timestamp;
        if (start) {
            const duration = Date.now() - new Date(start).getTime();
            return Math.floor(duration / 1000); // in seconds
        }
        return 0;
    }
};

// ================================
// App Initialization
// ================================
const App = {
    init() {
        console.log('🎀 A&A Design Web App Initializing...');
        
        // Initialize modules
        TelegramApp.init();
        Navigation.init();
        Shop.init();
        Books3D.init();
        ReviewsSlider.init();
        FAQ.init();
        Contacts.init();
        Animations.init();
        
        // Track initial page view
        Analytics.trackPageView('shop');
        
        // Setup global error handler
        this.setupErrorHandler();
        
        // Setup performance monitoring
        this.monitorPerformance();
        
        // Check connection
        this.checkConnection();
        
        console.log('✅ A&A Design Web App Ready!');
    },
    
    setupErrorHandler() {
        window.addEventListener('error', (e) => {
            console.error('App Error:', e.message);
            Analytics.track('error', {
                message: e.message,
                source: e.filename,
                line: e.lineno,
                column: e.colno
            });
        });
        
        window.addEventListener('unhandledrejection', (e) => {
            console.error('Unhandled Promise Rejection:', e.reason);
            Analytics.track('promise_rejection', {
                reason: e.reason
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
                            loadTime: perfData.loadEventEnd - perfData.fetchStart,
                            domReady: perfData.domContentLoadedEventEnd - perfData.fetchStart,
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
            console.log('Connection restored');
        });
        
        window.addEventListener('offline', () => {
            TelegramApp.showAlert('Подключение к интернету потеряно');
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
// Export for debugging
// ================================
window.AADesignApp = {
    App,
    TelegramApp,
    Navigation,
    Shop,
    Books3D,
    ReviewsSlider,
    FAQ,
    Contacts,
    Analytics,
    Utils
};