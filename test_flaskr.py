import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie
from auth_details import executive, direct, assist
# from auth.auth import AuthError, requires_auth


class FilmTestCase(unittest.TestCase):
    """This class represents the film test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = "sqlite:///film_test.db"
        setup_db(self.app, self.database_path)

        self.new_actor = {
            "name": "Ellen Page",
            "age" : 25,
            "gender": "female"
        }

        self.modified_actor = {
            'name': "Elliot Page",
            "age": 25,
            "gender": "male"
        }

        self.new_movie = {
            "title": "Star Wars",
            "release_date": 1977,
        }

        self.modified_movie = {
            'title': "Star Wars: Episode IV: A New Hope",
            "release_date": 1977,
        }

        # Users

        self.casting_assistant = assist
        self.casting_director = direct
        self.executive_producer = executive

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    # GET 
    ## ACTORS

    ### SUCCESS
    def test_get_actors(self):
        res = self.client().get('/actors', headers={"Authorization": "Bearer {}".format(self.casting_assistant)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    ### FAILURE

    def test_actors_wrong_endpoint(self):
        res = self.client().get('/actresses/', headers={"Authorization": "Bearer {}".format(self.casting_assistant)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
 
    ## MOVIES
    ### SUCCESS
    def test_get_movies(self):
        res = self.client().get('/movies', headers={"Authorization": "Bearer {}".format(self.casting_assistant)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']))
    ### FAILURE
    def test_unauthorised_get_movies(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)


    # CREATE
    ## ACTOR
    ### SUCCESS
    def test_create_new_actor(self):
        res = self.client().post('/actors', headers={"Authorization": "Bearer {}".format(self.casting_director)}, json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

    ### FAILURE
    def test_method_not_allowed_create_new_actor(self):
        res = self.client().post('/actors/5', headers={"Authorization": "Bearer {}".format(self.casting_director)}, json=self.new_actor)

        self.assertEqual(res.status_code, 405)


    ### RBAC (Casting Assistant) should fail
    def test_user_not_allowed_create_new_actor(self):
        res = self.client().post('/actors', headers={"Authorization": "Bearer {}".format(self.casting_assistant)}, json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    ## MOVIE
    ### SUCCESS
    def test_create_new_movie(self):
        res = self.client().post('/movies', headers={"Authorization": "Bearer {}".format(self.casting_director)}, json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

    ### FAILURE
    def test_method_not_allowed_create_new_movie(self):
        res = self.client().post('/movies/5', headers={"Authorization": "Bearer {}".format(self.casting_director)}, json=self.new_movie)

        self.assertEqual(res.status_code, 405)


    ### RBAC (Casting assistant) should fail
    def test_user_not_allowed_create_new_movie(self):
        res = self.client().post('/movies', headers={"Authorization": "Bearer {}".format(self.casting_assistant)}, json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)


    # DELETE
    ## ACTOR
    ### SUCCESS
    def test_delete_actor(self):
        # create a new actor to delete
        a = Actor(name=self.new_actor['name'], age=self.new_actor['age'],
                     gender=self.new_actor['gender'])
        a.insert()

        res = self.client().delete('/actors/{}'.format(a.id), headers={"Authorization": "Bearer {}".format(self.casting_director)})
        data = json.loads(res.data)

        actor = Actor.query.filter(Actor.id == a.id).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], a.id)

    ### FAILURE
    def test_422_if_actor_does_not_exist(self):
        res = self.client().delete('/actors/1000', headers={"Authorization": "Bearer {}".format(self.casting_director)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    ### RBAC (Casting Assistant) should fail

    # create a new actor to delete
    def test_not_allowed_to_delete_actor(self):
        a = Actor(name=self.new_actor['name'], age=self.new_actor['age'],
                     gender=self.new_actor['gender'])
        a.insert()

        res = self.client().delete('/actors/{}'.format(a.id), headers={"Authorization": "Bearer {}".format(self.casting_assistant)})
        data = json.loads(res.data)

        actor = Actor.query.filter(Actor.id == a.id).one_or_none()

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)


    ##MOVIE
    ### SUCCESS
    def test_delete_movie(self):
        # create a new movie to delete
        m = Movie(title=self.new_movie['title'], release_date=self.new_movie['release_date'])
        m.insert()

        res = self.client().delete('/movies/{}'.format(m.id), headers={"Authorization": "Bearer {}".format(self.executive_producer)})
        data = json.loads(res.data)

        movie = Movie.query.filter(Movie.id == m.id).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], m.id)

    ### FAILURE
    def test_422_if_movie_does_not_exist(self):
        res = self.client().delete('/movies/1000', headers={"Authorization": "Bearer {}".format(self.executive_producer)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    ### RBAC (Casting Director) should fail

    # create a new movie to delete
    def test_not_allowed_to_delete_movie(self):
        m = Movie(title=self.new_movie['title'], release_date=self.new_movie['release_date'])
        m.insert()

        res = self.client().delete('/movies/{}'.format(m.id), headers={"Authorization": "Bearer {}".format(self.casting_director)})
        data = json.loads(res.data)

        movie = Movie.query.filter(Movie.id == m.id).one_or_none()

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    # MODIFY
    ##ACTOR
    ### SUCCESS
    def test_modify_actor(self):
        res = self.client().patch('/actors/4', headers={"Authorization": "Bearer {}".format(self.executive_producer)}, json=self.modified_actor)
        data = json.loads(res.data)

        actor = Actor.query.filter(Actor.id == 4).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(actor.name, 'Elliot Page')
    
    ### FAILRE
    def test_failed_to_modify_actor(self):
        res = self.client().patch('/actors/4', headers={"Authorization": "Bearer {}".format(self.casting_director)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['message'], "bad request")

    ### RBAC (Casting assistant) should fail
    def test_not_allowed_to_modify_actor(self):
        res = self.client().patch('/actors/4', headers={"Authorization": "Bearer {}".format(self.casting_assistant)}, json=self.modified_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['message'], "You don't have the permission to access the requested resource.")

    ##MOVIE
    ### SUCCESS
    def test_modify_movie(self):
        res = self.client().patch('/movies/5', headers={"Authorization": "Bearer {}".format(self.casting_director)}, json=self.modified_movie)
        data = json.loads(res.data)

        movie = Movie.query.filter(Movie.id == 5).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(movie.title, 'Star Wars: Episode IV: A New Hope')
    
    ### FAILRE
    def test_failed_to_modify_movie(self):
        res = self.client().patch('/movies/4', headers={"Authorization": "Bearer {}".format(self.casting_director)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['message'], "bad request")

    ### RBAC (Casting assistant) should fail
    def test_not_allowed_to_modify_movie(self):
        res = self.client().patch('/movies/4', headers={"Authorization": "Bearer {}".format(self.casting_assistant)}, json=self.modified_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['message'], "You don't have the permission to access the requested resource.")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()