from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/keys/<id>', methods=['GET'])
def get(id):
    print 'get %s' % id
    return id


@app.route('/keys', methods=['GET'])
def get_all():
    filter = request.args.get('filter')
    print 'filter : %s' % filter
    print 'get all'
    return 'all'


@app.route('/keys', methods=['PUT'])
def put():
    expire_in = request.args.get('expire_in')
    json_payload = request.json
    print 'put %s' % json_payload
    print 'expire args %s' % expire_in
    return jsonify(json_payload)


@app.route('/keys/<id>', methods=['DELETE'])
def delete(id):
    print 'delete %s' % id
    return id


@app.route('/keys', methods=['DELETE'])
def delete_all():
    print 'delete all'
    return 'delete all'


if __name__ == '__main__':
    app.run()
