import os
import http.server
import socketserver
from http import HTTPStatus

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Добавляем CORS заголовки для Telegram Web App
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        # Заголовки безопасности
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('X-Frame-Options', 'ALLOWALL')  # Разрешаем iframe для Telegram
        super().end_headers()

    def do_GET(self):
        # Обслуживаем index.html для корневого пути
        if self.path == '/':
            self.path = '/index.html'
        return super().do_GET()

# Получаем порт из переменной окружения
PORT = int(os.environ.get('PORT', 8000))

# Создаем сервер
with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
    print(f"🌐 Server running at http://localhost:{PORT}/")
    print(f"🎀 A&A Design Web App is ready!")
    httpd.serve_forever()