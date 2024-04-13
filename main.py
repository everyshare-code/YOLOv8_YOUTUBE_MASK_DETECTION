from app import app
from asgiref.wsgi import WsgiToAsgi
from uvicorn import run

asgi_app = WsgiToAsgi(app)  # Flask 앱을 ASGI 앱으로 변환
run(asgi_app, host="0.0.0.0", port=5001)