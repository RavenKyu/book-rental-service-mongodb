import os
import time
import random
import datetime
# from book_rental_manager.app import mongo

def init_db():
    pass
    # mongo.drop_database()

def dummy_members():
    from book_rental_manager.models import CustomerFactory
    [CustomerFactory() for _ in range(30)]

def dummy_books():
    from book_rental_manager.models import BookFactory
    [BookFactory() for _ in range(100)]
