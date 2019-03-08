from flask import Flask
import os
import pickledb
from metrics.metrics_handler import setup_metrics

app = Flask(__name__)
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'key_value_store.db')
))
setup_metrics(app)

db = pickledb.load(app.config['DATABASE'], True)

from appplication.routes import keys_route

app.register_blueprint(keys_route.views)
