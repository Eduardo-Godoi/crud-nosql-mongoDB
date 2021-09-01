from flask import Flask


def create_app():
    app = Flask(__name__)

    from .views import blog_view
    blog_view.init_app(app)

    return app
