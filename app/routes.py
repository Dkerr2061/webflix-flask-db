from flask import render_template, request, make_response, session
from flask_restful import Resource

from app import app, db

from app.models import User, Movie, CartItem, Review


@app.route("/")
def index():
    return render_template("index.html")
