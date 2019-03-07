from werkzeug.wsgi import DispatcherMiddleware
from appplication import app
from prometheus_client import make_wsgi_app

# if __name__ == '__main__':
#     app.run()

# run : uwsgi --http 127.0.0.1:8000 --wsgi-file app.py --callable app_dispatch

app_dispatch = DispatcherMiddleware(app, {
    '/metrics': make_wsgi_app()
})
