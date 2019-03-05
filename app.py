from flask import Flask, jsonify, request, abort, make_response
import pickledb

app = Flask(__name__)
db = pickledb.load('key_value_store.db', True)


@app.route('/keys/<id>', methods=['GET'])
def get(id):
    if not db.exists(id):
        abort(404)
    value = db.get(id)
    return jsonify({'response': value})


@app.route('/keys', methods=['GET'])
def get_all():
    values = []

    filter = request.args.get('filter')
    print 'filter : %s' % filter

    all_keys = db.getall()

    for key in all_keys:
        values.append(db.get(key))
    return jsonify({'response': values})


@app.route('/keys', methods=['PUT'])
def put():
    expire_in = request.args.get('expire_in')
    json_payload = request.json

    for key, value in json_payload.iteritems():
        db.set(str(key), value)

    print 'expire args %s' % expire_in
    return jsonify({'response': json_payload})


@app.route('/keys/<id>', methods=['DELETE'])
def delete(id):
    db.drem(id)
    return jsonify({'response': id})


@app.route('/keys', methods=['DELETE'])
def delete_all():
    db.deldb()
    return jsonify({'response': 'delete all'})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run()
