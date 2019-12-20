from flask import Flask




def create_app():
    app = Flask(__name__)
    register_blueprint(app)
    return app



def register_blueprint(app):
    from restfulAPI.web import web
    app.register_blueprint(web)