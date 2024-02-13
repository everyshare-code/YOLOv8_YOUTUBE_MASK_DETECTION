# main.py
from app import app
from asgiref.wsgi import WsgiToAsgi
import uvicorn

asgi_app=WsgiToAsgi(app)

if __name__ == "__main__":
    uvicorn.run(asgi_app, host="0.0.0.0", port=5000)