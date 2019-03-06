from flask import Flask, jsonify, request, abort, make_response
from prometheus_client import make_wsgi_app, Counter
from werkzeug.wsgi import DispatcherMiddleware
from service.database_service import DatabaseService
from dateutil import parser
from datetime import datetime

app = Flask(__name__)

database_service = DatabaseService()

error_counter = Counter('my_requests_total', 'HTTP Failures', ['error_code', 'description'])


@app.route('/keys/<id>', methods=['GET'])
def get(id):
    if not database_service.exists(id):
        abort(404)
    value = database_service.get(id)
    if is_value_expired(value):
        abort(410)
    return jsonify({'response': value})


@app.route('/keys', methods=['GET'])
def get_all():
    filter = request.args.get('filter')
    print 'filter : %s' % filter
    values = database_service.get_all_values(filter)
    return jsonify({'response': values})


@app.route('/keys', methods=['PUT'])
def put():
    expire_in = request.args.get('expire_in')
    json_payload = request.json
    print 'expire args %s' % expire_in
    res = database_service.put(json_payload, expire_in)
    return jsonify({'response': res})


@app.route('/keys/<id>', methods=['DELETE'])
def delete(id):
    if not database_service.exists(id):
        abort(404)
    res = database_service.delete(id)
    return jsonify({'response': res})


@app.route('/keys', methods=['DELETE'])
def delete_all():
    res = database_service.delete_all()
    return jsonify({'response': res})


@app.errorhandler(404)
def not_found(error):
    error_counter.labels(error_code='404', description='Entity not found').inc()
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(410)
def expired(error):
    error_counter.labels(error_code='410', description='Entity expired').inc()
    return make_response(jsonify({'error': 'Expired'}), 410)


@app.errorhandler(500)
def server_error(error):
    error_counter.labels(error_code='500', description='Internal error').inc()
    return make_response(jsonify({'error': 'Internal error :('}), 500)


def is_value_expired(value):
    if not value.get('date_expiration'):
        return False
    date_expiration = parser.parse(value.get('date_expiration'))
    print date_expiration
    print datetime.now()
    return date_expiration < datetime.now()


# run : uwsgi --http 127.0.0.1:8000 --wsgi-file app.py --callable app_dispatch
app_dispatch = DispatcherMiddleware(app, {
    '/metrics': make_wsgi_app()
})
