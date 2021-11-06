import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Actor, Movie, db, add_actor_data, add_movie_data
from auth.auth import AuthError, requires_auth


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    @app.route('/')
    def index():
        return 'Should probably have something here'

    # Actors

    @app.route('/actors')
    @requires_auth('get:actors')
    def get_actors(payload):

        actors = Actor.query.all()
        data = []
        for actor in actors:
            actor_data = {'id': actor.id, 'name': actor.name, 'age': actor.age, 'gender': actor.gender}
            data.append(actor_data)

        return jsonify({
          "success": True,
          "actors": data
        })

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def create_actor(payload):
        body = request.get_json()
        try:
            actor = Actor(
              name=body.get('name'),
              age=body.get('age'),
              gender=body.get('gender'),
            )
            actor.insert()

            return jsonify({
              "success": True,
              "created": actor.id
            })

        except Exception as e:
            print(e)
            abort(422)

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(payload, actor_id):
        try:
            actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

            if actor is None:
                abort(404)          

            actor.delete()

            return jsonify({
              'success': True,
              "deleted": actor.id,
              'total_actors': len(Actor.query.all())
            })

        except Exception as e:
            print(e)
            abort(422)

    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def modify_actor(payload, actor_id):

        body = request.get_json()

        try:
            actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
            if actor is None:
                abort(404)

            if 'name' in body:
                actor.name = body.get('name')
            if 'gender' in body:
                actor.gender = body.get('gender')

            actor.update()

            return jsonify({
              "success": True,
              "actor": {
                "name": actor.name,
                "age": actor.age,
                "gender": actor.gender
              }
            })

        except Exception as e:    
            print(e)
            abort(400)

    # Movies

    @app.route('/movies')
    @requires_auth('get:movies')
    def get_movies(payload):
        movies = Movie.query.all()
        data = []
        for movie in movies:
            movie_data = {'id': movie.id, 'title': movie.title, 'release_date': movie.release_date}
            data.append(movie_data)

        return jsonify({
            "success": True,
            "movies": data
        })

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def create_movie(payload):
        body = request.get_json()
        try:
            movie = Movie(
              title=body.get('title'),
              release_date=body.get('release_date'),
            )
            movie.insert()

            return jsonify({
              "success": True,
              "created": movie.id
            })

        except Exception as e:
            print(e)        
            abort(422)

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(payload, movie_id):
        try:
            movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

            if movie is None:
                abort(404)
            
            movie.delete()

            return jsonify({
              'success': True,
              "deleted": movie.id,
              'total_movies': len(Movie.query.all())
            })

        except Exception as e:    
            print(e)
            abort(422)

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def modify_movie(payload, movie_id):

        body = request.get_json()

        try:
            movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
            if movie is None:
                abort(404)

            if 'title' in body:
                movie.title = body.get('title')
            if 'release_date' in body:
                movie.release_date = body.get('release_date')

            movie.update()

            return jsonify({
              "success": True,
              "movie": {
                "title": movie.title,
                "release_date": movie.release_date,
              }

            })

        except Exception as e:
            print(e)
            abort(400)

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not found"
        }), 404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False, 
            "error": 400,
            "message": "bad request"
            }), 400

    @app.errorhandler(403)
    def access_denied(error):
        return jsonify({
            "success": False, 
            "error": 403,
            "message": "You don't have the permission to access the requested resource."
            }), 403

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
          "success": False, 
          "error": 422,
          "message": "unprocessable"
          }), 422

    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
          "success": False, 
          "error": 405,
          "message": "method not allowed"
          }), 405

    @app.errorhandler(AuthError)
    def auth_error(ex):
        response = jsonify(ex.error)
        response.status_code = ex.status_code
        return response

    return app


APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)