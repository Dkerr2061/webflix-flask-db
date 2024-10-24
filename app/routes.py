#!/usr/bin/env python3

# Standard library imports

# Remote library imports
from email.mime import image
from flask import request, make_response, session
from flask_restful import Resource

# Local imports
from app import app, db, api, bcrypt
from flask import render_template

# Add your model imports
from app.models import User, Movie, CartItem, Review, Artists, Albums, AlbumReviews


# Views go here!
# ===================================================================================
@app.route("/")
@app.route("/<int:id>")
def index(id=0):
    return render_template("index.html")


class AllMovies(Resource):

    def get(self):
        movies = Movie.query.all()
        body = [
            movie.to_dict(
                rules=(
                    "-reviews.movie",
                    "-reviews.user",
                    "-cart_items.movie_cart",
                    "-cart_items.user_cart",
                )
            )
            for movie in movies
        ]
        return make_response(body, 200)

    def post(self):
        try:
            new_movie = Movie(
                name=request.json.get("name"),
                image=request.json.get("image"),
                year=request.json.get("year"),
                director=request.json.get("director"),
                description=request.json.get("description"),
                price=request.json.get("price"),
            )
            db.session.add(new_movie)
            db.session.commit()
            body = new_movie.to_dict(
                rules=(
                    "-reviews.movie",
                    "-reviews.user",
                    "-cart_items.movie_cart",
                    "-cart_items.user_cart",
                )
            )
            return make_response(body, 201)
        except:
            body = {"error": "New movie could not be created."}
            return make_response(body, 400)


api.add_resource(AllMovies, "/movies")


class MovieByID(Resource):

    def get(self, id):
        movie = db.session.get(Movie, id)
        if movie:
            body = movie.to_dict(
                rules=(
                    "-reviews.movie",
                    "-reviews.user",
                    "-cart_items.movie_cart",
                    "-cart_items.user_cart",
                )
            )

            body["users"] = [
                user.to_dict(only=("id", "username")) for user in movie.users
            ]

            return make_response(body, 200)
        else:
            body = {"error": f"Movie {id} not found."}
            return make_response(body, 404)

    def patch(self, id):
        movie = db.session.get(Movie, id)
        if movie:
            try:
                for attr in request.json:
                    setattr(movie, attr, request.json[attr])
                db.session.commit()
                body = movie.to_dict(
                    rules=(
                        "-reviews.movie",
                        "-reviews.user",
                        "-cart_items.movie_cart",
                        "-cart_items.user_cart",
                    )
                )
                return make_response(body, 200)
            except:
                body = {"error": "Movie could not be updated."}
                return make_response(body, 400)
        else:
            body = {"error": f"Movie {id} could not be found."}
            return make_response(body, 404)

    def delete(self, id):
        movie = db.session.get(Movie, id)
        if movie:
            db.session.delete(movie)
            db.session.commit()
            body = {}
            return make_response(body, 204)
        else:
            body = {"error": f"Movie {id} was not found"}
            return make_response(body, 404)


api.add_resource(MovieByID, "/movies/<int:id>")

# =================================================================================


class AllUsers(Resource):

    def get(self):
        users = User.query.all()
        body = [
            user.to_dict(
                rules=(
                    "-reviews.movie",
                    "-reviews.user",
                    "-cart_items.movie_cart",
                    "-cart_items.user_cart",
                    "-password_hash",
                )
            )
            for user in users
        ]
        return make_response(body, 200)

    def post(self):
        try:
            new_user = User(
                username=request.json.get("username"),
                password_hash=request.json.get("password_hash"),
                type=request.json.get("type"),
            )
            db.session.add(new_user)
            db.session.commit()
            body = new_user.to_dict(
                rules=(
                    "-reviews.movie",
                    "-reviews.user",
                    "-cart_items.movie_cart",
                    "-cart_items.user_cart",
                    "-password_hash",
                )
            )
            return make_response(body, 201)
        except:
            body = {"error": "Could not create new user."}
            return make_response(body, 400)


api.add_resource(AllUsers, "/users")


class UserByID(Resource):

    def get(self, id):
        user = db.session.get(User, id)
        if user:
            try:
                body = user.to_dict(
                    rules=(
                        "-reviews.movie",
                        "-reviews.user",
                        "-cart_items.movie_cart",
                        "-cart_items.user_cart",
                        "-password_hash",
                    )
                )

                body["movies"] = [
                    movie.to_dict(
                        rules=(
                            "-reviews.movie",
                            "-reviews.user",
                            "-cart_items.movie_cart",
                            "-cart_items.user_cart",
                            "-password_hash",
                        )
                    )
                    for movie in user.movies
                ]

                return make_response(body, 200)
            except:
                body = {"error": "User not found"}
                return make_response(body, 404)
        else:
            body = {"error": f"User {id} was not found."}
            return make_response(body, 404)

    def delete(self, id):
        user = db.session.get(User, id)
        if user:
            try:
                db.session.delete(user)
                db.session.commit()
                body = {}
                return make_response(body, 204)
            except:
                body = {"error": f"User {id} could not be deleted"}
                return make_response(body, 400)
        else:
            body = {"error": f"User {id} could not be found"}
            return make_response(body, 404)


api.add_resource(UserByID, "/users/<int:id>")

# =================================================================================


class AllReviews(Resource):

    def get(self):
        reviews = Review.query.all()
        body = [
            review.to_dict(
                rules=(
                    "-movie.reviews",
                    "-user.reviews",
                    "-user.cart_items",
                    "-movie.cart_items",
                    "-user.password_hash",
                )
            )
            for review in reviews
        ]
        return make_response(body, 200)

    def post(self):
        try:
            new_review = Review(
                rating=request.json.get("rating"),
                text=request.json.get("text"),
                movie_id=request.json.get("movie_id"),
                user_id=request.json.get("user_id"),
            )
            db.session.add(new_review)
            db.session.commit()
            body = new_review.to_dict(
                rules=(
                    "-movie.reviews",
                    "-user.reviews",
                    "-user.cart_items",
                    "-movie.cart_items",
                    "-user.password_hash",
                )
            )
            return make_response(body, 201)
        except:
            body = {"error": "Review could not be created."}
            return make_response(body, 400)


api.add_resource(AllReviews, "/reviews")


class ReviewByID(Resource):

    def get(self, id):
        pass
        review = db.session.get(Review, id)
        if review:
            try:
                body = review.to_dict(
                    rules=(
                        "-movie.reviews",
                        "-user.reviews",
                        "-user.cart_items",
                        "-movie.cart_items",
                        "-user.password_hash",
                    )
                )
                return make_response(body, 200)
            except:
                body = {"error": "Could not fetch review at this moment."}
                return make_response(body, 400)
        else:
            body = {"error": f"Review {id} could not be found."}
            return make_response(body, 404)

    def patch(self, id):
        review = db.session.get(Review, id)
        if review:
            try:
                for attr in request.json:
                    setattr(review, attr, request.json[attr])
                db.session.commit()
                body = review.to_dict(
                    rules=(
                        "-movie.reviews",
                        "-user.reviews",
                        "-user.cart_items",
                        "-movie.cart_items",
                        "-user.password_hash",
                    )
                )
                return make_response(body, 201)
            except:
                body = {"error": "Review could not be updated."}
                return make_response(body, 400)
        else:
            body = {"error": f"Review {id} not found."}
            return make_response(body, 404)

    def delete(self, id):
        review = db.session.get(Review, id)
        if review:
            db.session.delete(review)
            db.session.commit()
            body = {}
            return make_response(body, 204)
        else:
            body = {"error": f"Review {id} not found."}
            return make_response(body, 404)


api.add_resource(ReviewByID, "/reviews/<int:id>")


class AllCartItems(Resource):

    def get(self):
        user = User.query.filter(User.id == session.get("user_id")).first()

        if user and user.type == "admin":
            cart_items = CartItem.query.all()
            body = [
                cart_item.to_dict(
                    rules=(
                        "-movie_cart.cart_items",
                        "-user_cart.cart_items",
                        "-movie_cart.reviews",
                        "-user_cart.reviews",
                        "-user_cart.password_hash",
                    )
                )
                for cart_item in cart_items
            ]
            return make_response(body, 200)
        elif user and user.type == "customer":
            body = [
                cart_item.to_dict(
                    rules=(
                        "-movie_cart.cart_items",
                        "-user_cart.cart_items",
                        "-movie_cart.reviews",
                        "-user_cart.reviews",
                        "-user_cart.password_hash",
                    )
                )
                for cart_item in list(set(user.cart_items))
            ]
            return make_response(body, 200)
        else:
            body = {"error": "Something went wrong..."}
            return make_response(body, 400)

    def post(self):
        try:
            new_cart_item = CartItem(
                movie_id=request.json.get("movie_id"),
                user_id=request.json.get("user_id"),
            )
            db.session.add(new_cart_item)
            db.session.commit()
            body = new_cart_item.to_dict(
                rules=(
                    "-movie_cart.cart_items",
                    "-user_cart.cart_items",
                    "-movie_cart.reviews",
                    "-user_cart.reviews",
                    "-user_cart.password_hash",
                )
            )
            return make_response(body, 201)
        except:
            body = {"error": "Could not add item to cart."}
            return make_response(body, 400)


api.add_resource(AllCartItems, "/cart_items")


class CartItemsByID(Resource):

    def get(self, id):
        cart_item = db.session.get(CartItem, id)
        if cart_item:
            try:
                body = cart_item.to_dict(
                    rules=(
                        "-movie_cart.cart_items",
                        "-user_cart.cart_items",
                        "-movie_cart.reviews",
                        "-user_cart.reviews",
                        "-user_cart.password_hash",
                    )
                )
                return make_response(body, 200)
            except:
                body = {"error": "Could not process request."}
                return make_response(body, 400)
        else:
            body = {"error": f"Cart item {id} could not be found."}
            return make_response(body, 404)

    def delete(self, id):
        cart_item = db.session.get(CartItem, id)
        if cart_item:
            db.session.delete(cart_item)
            db.session.commit()
            body = {}
            return make_response(body, 204)
        else:
            body = {"error": f"Cart item {id} not found."}


api.add_resource(CartItemsByID, "/cart_items/<int:id>")


class Login(Resource):

    def post(self):
        username = request.json.get("username")
        password = request.json.get("password_hash")
        current_user = User.query.filter(User.username == username).first()

        if current_user and bcrypt.check_password_hash(
            current_user.password_hash, password
        ):
            session["user_id"] = current_user.id
            body = current_user.to_dict(
                rules=(
                    "-reviews.movie",
                    "-reviews.user",
                    "-cart_items.movie_cart",
                    "-cart_items.user_cart",
                    "-password_hash",
                )
            )

            body["movies"] = [
                movie.to_dict(
                    rules=(
                        "-reviews.movie",
                        "-reviews.user",
                        "-cart_items.movie_cart",
                        "-cart_items.user_cart",
                        "-password_hash",
                    )
                )
                for movie in list(set(current_user.movies))
            ]

            return make_response(body, 200)
        else:
            body = {"error": "Invalid Username or Password."}
            return make_response(body, 401)


api.add_resource(Login, "/login")


class CheckSession(Resource):

    def get(self):
        current_user = db.session.get(User, session.get("user_id"))
        if current_user:
            body = current_user.to_dict(
                rules=(
                    "-reviews.movie",
                    "-reviews.user",
                    "-cart_items.movie_cart",
                    "-cart_items.user_cart",
                    "-password_hash",
                )
            )

            body["movies"] = [
                movie.to_dict(
                    rules=(
                        "-reviews.movie",
                        "-reviews.user",
                        "-cart_items.movie_cart",
                        "-cart_items.user_cart",
                        "-password_hash",
                    )
                )
                for movie in list(set(current_user.movies))
            ]

            return make_response(body, 200)
        else:
            body = {"error": "Please LogIn!"}
            return make_response(body, 401)


api.add_resource(CheckSession, "/check_session")


class Logout(Resource):

    def delete(self):
        if session.get("user_id"):
            del session["user_id"]

        body = {}
        return make_response(body, 204)


api.add_resource(Logout, "/logout")


class Signup(Resource):

    def post(self):
        try:
            password = request.json.get("password_hash")
            pw_hash = bcrypt.generate_password_hash(password).decode("utf-8")
            new_user = User(
                username=request.json.get("username"),
                password_hash=pw_hash,
                type="customer",
            )
            db.session.add(new_user)
            db.session.commit()
            session["user_id"] = new_user.id

            body = new_user.to_dict(
                rules=(
                    "-reviews.movie",
                    "-reviews.user",
                    "-cart_items.movie_cart",
                    "-cart_items.user_cart",
                    "-password_hash",
                )
            )

            body["movies"] = [
                movie.to_dict(
                    rules=(
                        "-reviews.movie",
                        "-reviews.user",
                        "-cart_items.movie_cart",
                        "-cart_items.user_cart",
                        "-password_hash",
                    )
                )
                for movie in new_user.movies
            ]

            return make_response(body, 201)
        except:
            body = {"error": "Could not create new user."}
            return make_response(body, 400)


api.add_resource(Signup, "/signup")

# ------------------------------------------------------------------------


class AllArtists(Resource):
    def get(self):
        artists = Artists.query.all()
        body = [artist.to_dict(only=("id", "name", "image")) for artist in artists]
        return make_response(body, 200)

    def post(self):
        try:
            new_artist = Artists(
                name=request.json.get("name"), image=request.json.get("image")
            )
            db.session.add(new_artist)
            db.session.commit()

            body = new_artist.to_dict(only=("id", "name", "image"))
            return make_response(body, 201)
        except:
            body = {
                "error": "Artist's name must be unique and both name and image fields must be completed."
            }
            return make_response(body, 400)


api.add_resource(AllArtists, "/artists")

if __name__ == "__main__":
    app.run(port=8000, debug=True)
