import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

if os.path.exists("env.py"):
    import env

app = Flask(__name__)

app.config["MONGO_DBNAME"] = "spooky_spool"
app.config["MONGO_URI"] = os.getenv("MONGODB_URI")

mongo = PyMongo(app)


@app.route("/")
def index():
    all_movies = mongo.db.movies

    movies = all_movies.find()

    horror_movies = all_movies.find({"genre": {"$elemMatch": {"$eq": ObjectId("5f806ebc0727bbf597c35ba4")}}})

    thriller_movies = all_movies.find({"genre": {"$elemMatch": {"$eq": ObjectId("5f806ebc0727bbf597c35ba5")}}})

    return "Normal movies: " + str(movies.count()) + " Horror Movies: " + str(horror_movies.count()) + " Thriller Movies: " + str(thriller_movies.count())

@app.route("/browse")
def browse_movies():

    movie_list = mongo.db.movies

    movies = movie_list.find().sort("year", -1).limit(60)

    return render_template("browse.html", movies=movies)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
