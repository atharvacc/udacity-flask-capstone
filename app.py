import os
from flask import Flask, jsonify, abort, request
from models import setup_db
from flask_cors import CORS
from models import Actors, Movies
from auth import requires_auth


RESULTS_PER_PAGE = 10


def paginate_results(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * RESULTS_PER_PAGE
    end = start + RESULTS_PER_PAGE

    result = [x.format() for x in selection]
    current_questions = result[start:end]
    return current_questions


def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors(jwt):
        all_actors = Actors.query.order_by(Actors.id).all()
        return jsonify({
        'success': True,
        'actors': [ (actor.id, actor.name)  for actor in all_actors]
    })

    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies(jwt):
        all_movies = Movies.query.order_by(Movies.id).all()
        return jsonify({
        'success': True,
        'movies': [(movie.id, movie.title) for movie in all_movies]
    })

    @app.route('/actors/<int:id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actors( jwt, id):
        actor = Actors.query.get(id)
        if actor is None:
            abort(404)

        actor.delete()

        return jsonify({
            'success': True,
            'delete': actor.id
        })

    @app.route('/movies/<int:id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movies(jwt, id):
        movie = Movies.query.get(id)
        if movie is None:
            abort(404)

        movie.delete()

        return jsonify({
            'success': True,
            'delete': movie.id
        })

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def post_movies(jwt):
        data = request.get_json()
        if 'title' and 'release_date' not in data:
            abort(422)

        title = data['title']
        release_date = data['release_date']
        movie = Movies(title=title, release_date=release_date)
        movie.insert()

        return jsonify({
            'success': True,
            'movie': [movie.title, movie.release_date, movie.id]
        })

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def post_actors(jwt):
        data = request.get_json()
        if 'name' and 'age' and 'gender' not in data:
            abort(422)

        name = data['name']
        age = data['age']
        gender = data['gender']
        actor = Actors(name=name, age=age, gender=gender)
        actor.insert()

        return jsonify({
            'success': True,
            'actor': [actor.name, actor.age, actor.gender, actor.id]
        })

    @app.route('/actors/<int:id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actors(jwt, id):
        actor = Actors.query.get(id)
        if actor is None:
            abort(404)

        data = request.get_json()
        if 'name' in data:
            actor.name = data['name']
        if 'age' in data:
            actor.age = data['age']
        if 'gender' in data:
            actor.gender = data['gender']
        actor.update()
        return jsonify({
            'success': True,
            'actor': [actor.name, actor.age, actor.gender, actor.id]
        })

    @app.route('/movies/<int:id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movies(jwt, id):
        movie = Movies.query.get(id)
        if movie is None:
            abort(404)

        data = request.get_json()
        if 'title' in data:
            movie.title = data['title']
        if 'release_date' in data:
            movie.release_date = data['release_date']
        movie.update()
        return jsonify({
            'success': True,
            'movie': [movie.title, movie.release_date, movie.id]
        })

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400


    @app.errorhandler(AuthError)
    def auth_error(auth_error):
        return jsonify({
        "success": False,
        "error": auth_error.status_code,
        "message": auth_error.error['description']
        }), auth_error.status_code
    return app


app = create_app()

if __name__ == '__main__':
    
    app.run()