import time
import factory
import datetime
import mongoengine
import mongoengine_goodjson as gj


class Customer(gj.Document):
    customer_id = mongoengine.SequenceField(collection_name='Customer', unique=True)
    name = mongoengine.StringField()
    phone = mongoengine.StringField()


class CustomerFactory(factory.mongoengine.MongoEngineFactory):
    class Meta:
        model = Customer
    name = factory.Faker('name', locale='ko_KR')
    phone = factory.Faker('phone_number', locale='ko_KR')


class Book(gj.Document):
    book_id = mongoengine.SequenceField(collection_name='Book', unique=True)
    title = mongoengine.StringField()
    author = mongoengine.StringField()
    publisher = mongoengine.StringField()


class BookFactory(factory.mongoengine.MongoEngineFactory):
    class Meta:
        model = Book
    title = factory.Faker('catch_phrase', locale='ko_KR')
    author = factory.Faker('name', locale='ko_KR')
    publisher = factory.Faker('company', locale='ko_KR')


class Rental(gj.Document):
    rental_id = mongoengine.SequenceField(collection_name='Rental', unique=True)
    book = gj.FollowReferenceField(Book)
    customer = gj.FollowReferenceField(Customer)
    rental_start = mongoengine.DateTimeField()
    rental_end = mongoengine.DateTimeField()


class RentalFactory(factory.mongoengine.MongoEngineFactory):
    class Meta:
        model = Rental

    rental_start = factory.Faker('date_time_between', locale='ko_KR', start_date='-3d', end_date='now')

