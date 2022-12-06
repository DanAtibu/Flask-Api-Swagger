from flask import Flask, request, send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint
from utils import UserTable, NotFoundResponse
from json import loads


app = Flask(__name__)


# SWAGGER REGISTER
app.register_blueprint(get_swaggerui_blueprint(
    # SWAGGER URL
    '/docs',
    # API URL
    '/static/swagger/swagger.json',
    # CONFIG
    config={
        'app_name': "Simple Flask App With Swagger"
    }
), url_prefix='/docs')


app.route('/', methods=["GET"])(lambda: UserTable.get_all())


@app.route('/', methods=["POST"])
def post():
    return UserTable.insert(loads(request.data))


@app.route('/<int:id>', methods=["GET"])
@NotFoundResponse
def get_one_user(id):
    return UserTable.get_one(id)


@app.route('/<int:id>', methods=["PATCH"])
@NotFoundResponse
def patch(id):
    return UserTable.update(id, loads(request.data))


@app.route('/<int:id>', methods=["DELETE"])
@NotFoundResponse
def delete(id):
    return UserTable.delete(id)


# SWAGGER CONFIG
@app.route('/static/swagger/<path:path>', methods=["GET"])
def serve_static_file(path):
    return send_from_directory('static/swagger', path)


if __name__ == '__main__':
    app.run(debug=True)
