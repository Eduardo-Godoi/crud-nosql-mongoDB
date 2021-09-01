from flask import request, jsonify
from app.model.post_model import Post
from .except_main import KeySentError, ValueSentError, ReceivedIdError


def check_data(request_data: dict):
    key_accept = ['title', 'author', 'tags', 'content']

    for key in request_data.keys():
        if key not in key_accept:
            raise KeySentError

    if len(request_data) == 4:
        title, author, tags, content = request_data.values()
        if type(title) != str or type(author) != str or type(tags) != str or type(content) != str:
            raise ValueSentError


def create_a_new_post() -> dict:
    try:
        data = request.get_json()
        title, author, tags, content = data.values()

        check_data(data)

        new_post = Post(title, author, tags, content)
        post = new_post.save()

        return post, 201

    except ValueError:
        return {'msg': 'Verifique os Dados enviados'}, 400

    except KeySentError:
        return {'msg': f'Verifique as chaves enviadas chaves aceitas title, author, tags, content'}, 400

    except ValueSentError:
        return {'msg': 'Verifique os tipos dos valores enviados, Valor aceito: String'}, 400


def show_posts(id=None) -> dict:
    try:
        if id:
            if id > Post.length_collection:
                raise ReceivedIdError
            post = jsonify(Post.get_post_by_id(id))
            return post, 200

        all_posts = Post.show_all_posts()

        return jsonify(all_posts), 200

    except ReceivedIdError:
        return {'msg': f'O id recebido é maior que {Post.length_collection}'}, 404


def update(id: int) -> dict:
    try:

        new_data = request.get_json()

        check_data(new_data)

        if id > Post.length_collection:
            raise ReceivedIdError

        updated_publication = Post.update_post(id, new_data)

        return jsonify(updated_publication), 200

    except ReceivedIdError:
        number = Post.length_collection
        return {'msg': f'O id recebido é maior que {number}, envie um id menor'}, 404

    except KeySentError:
        return {'msg': f'Verifique as chaves enviadas chaves aceitas title, author, tags, content'}, 400

def delete(id: int) -> dict:
    try:
        if id not in Post.list_id:
            raise ReceivedIdError

        post = Post.delete_post(id)
        return post, 200

    except ReceivedIdError:
        return {'msg': 'O id recebido não foi encontrado'}, 404
