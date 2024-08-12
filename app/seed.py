#!/usr/bin/env python3

# Standard library imports
from random import randint, choice as rc

# Local imports
from app import app, bcrypt
from app.models import db, Movie, User, Review, CartItem

if __name__ == "__main__":

    with app.app_context():

        # Clear existing data
        Movie.query.delete()
        User.query.delete()
        Review.query.delete()
        CartItem.query.delete()

        print("Starting seed...")

        # Insert movies first
        movie1 = Movie(
            name="The Cabin in the Woods",
            image="https://m.media-amazon.com/images/I/81+TuC6oQ8L._AC_UF350,350_QL50_.jpg",
            year=2011,
            director="Drew Goddard",
            description="Five teenagers head off for a weekend at a secluded cabin in the woods. They arrive to find they are quite isolated with no means of communicating with the outside world. When the cellar door flings itself open, they of course go down to investigate. They find an odd assortment of relics and curios, but when one of the women, Dana, reads from a book, she awakens a family of deadly zombie killers. However, there's far more going on than meets the eye.",
            price=16.99,
        )

        movie2 = Movie(
            name="Fear and Loathing in Las Vegas",
            image="https://m.media-amazon.com/images/I/71bzrdGNELL._AC_UF894,1000_QL80_.jpg",
            year=1998,
            director="Terry Gilliam",
            description='The big-screen version of Hunter S. Thompson\'s seminal psychedelic classic about his road trip across Western America as he and his large Samoan lawyer searched desperately for the "American dream"... they were helped in large part by the huge amount of drugs and alcohol kept in their convertible, The Red Shark.',
            price=10.99,
        )

        movie3 = Movie(
            name="Dune",
            image="https://m.media-amazon.com/images/I/61QbqeCVm0L.jpg",
            year=2021,
            director="Denis Villeneuve",
            description="A mythic and emotionally charged hero's journey, \"Dune\" tells the story of Paul Atreides, a brilliant and gifted young man born into a great destiny beyond his understanding, who must travel to the most dangerous planet in the universe to ensure the future of his family and his people. As malevolent forces explode into conflict over the planet's exclusive supply of the most precious resource in existence-a commodity capable of unlocking humanity's greatest potential-only those who can conquer their fear will survive",
            price=21.95,
        )

        db.session.add_all([movie1, movie2, movie3])
        db.session.commit()  # Commit after adding movies

        # Insert users
        password_1 = "abc123"
        password_2 = "clay123"
        password_3 = "ana123"

        pw_hash_1 = bcrypt.generate_password_hash(password_1).decode("utf-8")
        pw_hash_2 = bcrypt.generate_password_hash(password_2).decode("utf-8")
        pw_hash_3 = bcrypt.generate_password_hash(password_3).decode("utf-8")

        user1 = User(username="dkerr123", password_hash=pw_hash_1, type="admin")
        user2 = User(username="clay456", password_hash=pw_hash_2, type="customer")
        user3 = User(username="ana789", password_hash=pw_hash_3, type="customer")

        db.session.add_all([user1, user2, user3])
        db.session.commit()  # Commit after adding users

        # Insert cart items
        cart_item1 = CartItem(movie_id=1, user_id=2)
        cart_item2 = CartItem(movie_id=2, user_id=2)
        cart_item3 = CartItem(movie_id=1, user_id=1)

        db.session.add_all([cart_item1, cart_item2, cart_item3])

        # Insert reviews
        review1 = Review(rating=6, text="Good but not great.", movie_id=1, user_id=2)
        review2 = Review(rating=10, text="Great movie!", movie_id=2, user_id=2)
        review3 = Review(rating=8, text="Better than expected.", movie_id=1, user_id=1)

        db.session.add_all([review1, review2, review3])
        db.session.commit()

        print("🌱 Database successfully seeded! 🌱")
