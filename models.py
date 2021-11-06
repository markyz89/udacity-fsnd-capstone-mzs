from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json
import sqlite3 as sql


db = SQLAlchemy()

# database_path = "postgres://{}/{}".format(database_uri, database_name)
database_path = "sqlite:///film.db"


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


class Actor(db.Model):
    __tablename__ = 'actors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String)

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def __repr__(self):
        return f'ID: {self.id}, name: {self.name}, age: {self.age}, gender: {self.gender}'

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
          'id': self.id,
          'name': self.name,
          'age': self.age,
          'gender': self.gender,
        }


class Movie(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    release_date = db.Column(db.Integer)

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def __repr__(self):
        return f'ID: {self.id}, title: {self.title}, release_date: {self.release_date}'

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
          'id': self.id,
          'title': self.title,
          'release_date': self.release_date,
        }


# to create dummy data for Sqlite database via Python interpreter

def add_actor_data(name, age, gender):  
    try:
        # Connecting to database
        con = sql.connect('film.db')
        # Getting cursor
        c = con.cursor() 
        # Adding data
        c.execute("INSERT INTO actors (name, age, gender) VALUES (?,?,?)",(name, age, gender))
        # Applying changes
        con.commit() 
    except Exception as e:  
        print("An error has occured", e)


def add_movie_data(title, release_date):
    try:
        # Connecting to database
        con = sql.connect('film.db')
        # Getting cursor
        c = con.cursor() 
        # Adding data
        c.execute("INSERT INTO movies (title, release_date) VALUES (?,?)", (title, release_date))
        # Applying changes
        con.commit() 
    except Exception as e:
        print("An error has occured", e)


