from flask import Flask
from app.services.main import create_a_new_post, show_posts, update, delete


def init_app(app: Flask):

    @app.post('/posts')
    def creat_post():
        return create_a_new_post()

    @app.get('/posts/<int:id>')
    @app.get('/posts')
    def read_posts(id=None):
        return show_posts(id)

    @app.patch('/posts/<int:id>')
    def update_post(id):
        return update(id)

    @app.delete('/posts/<int:id>')
    def delete_post(id: int):
        return delete(id)
