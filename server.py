import datetime
from functools import wraps

from flask import request, make_response, jsonify
import jwt

from app import app


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')

        if not token:
            return jsonify({'message': 'Token is required'})

        try:
            jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'message': 'Token is invalid'})

        return f(*args, **kwargs)

    return decorated


@app.route('/protected')
@token_required
def protected():
    return jsonify({'message': 'This is available only for people with valid token'})


@app.route('/login')
def login():
    auth = request.authorization
    if auth and auth.password == 'password':
        token = jwt.encode(
            {'user': auth.username,
             'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=10)},
            app.config['SECRET_KEY'])
        return jsonify({'token': token.decode('UTF-8')})
    return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})


if __name__ == '__main__':
    app.run(debug=True)
