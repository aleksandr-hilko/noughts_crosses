import os

from flask import Flask, jsonify
from flask_mongoengine import MongoEngine
from flask_jwt_extended import JWTManager


application = Flask(__name__)
application.config["JWT_SECRET_KEY"] = "KeepThisS3cr3tereterterter5yuy67u"

jwt = JWTManager(application)

application.config["SECRET_KEY"] = "KeepThisS3cr3t"

application.config['MONGODB_SETTINGS'] = {
    'db': os.environ['MONGODB_DATABASE'],
    'username': os.environ['MONGODB_USERNAME'],
    'password': os.environ['MONGODB_PASSWORD'],
    'host': os.environ['MONGODB_HOSTNAME'],
    'port': 27017,
}

db = MongoEngine(application)


def register_blueprints(app):
    # Prevents circular imports
    from app.auth.views import auth
    app.register_blueprint(auth)


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
