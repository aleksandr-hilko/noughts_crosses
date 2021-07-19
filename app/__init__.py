import os

from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_pymongo import PyMongo


application = Flask(__name__)
application.config["JWT_SECRET_KEY"] = "KeepThisS3cr3tereterterter5yuy67u"

jwt = JWTManager(application)

application.config["SECRET_KEY"] = "KeepThisS3cr3t"
application.config["MONGO_URI"] = f'mongodb://{os.environ["MONGODB_HOSTNAME"]}:27017/{os.environ["MONGODB_DATABASE"]}'

mongodb_client = PyMongo(application)
db = mongodb_client.db


def register_blueprints(app):
    # Prevents circular imports
    from app.auth.views import auth
    from app.game.views import game
    app.register_blueprint(auth)
    app.register_blueprint(game)


register_blueprints(application)


@application.route('/')
def index():
    return jsonify(
        status=True,
        message='Welcome to the Dockerized Flask MongoDB app!'
    )


if __name__ == '__main__':
    ENVIRONMENT_DEBUG = os.environ.get("APP_DEBUG", True)
    ENVIRONMENT_PORT = os.environ.get("APP_PORT", 5000)
    application.run(host='0.0.0.0', port=ENVIRONMENT_PORT, debug=ENVIRONMENT_DEBUG)
