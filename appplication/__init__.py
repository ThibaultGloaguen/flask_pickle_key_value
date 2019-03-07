from flask import Flask
import os
import pickledb
from prometheus_client import Counter

app = Flask(__name__)
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'key_value_store.db')
))
db = pickledb.load(app.config['DATABASE'], True)

error_counter = Counter('my_requests_total', 'HTTP Failures', ['error_code', 'description'])

from appplication.routes import keys

app.register_blueprint(keys.views)
