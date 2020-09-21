import datetime
from functools import wraps
import json
from flask import Flask, request, make_response, jsonify
from flask_restx import Resource, Api, reqparse, abort, fields
from flask_cors import CORS
from book_rental_manager.logger import get_logger
from book_rental_manager.models import Customer, Book, Rental
from mongoengine import connect, disconnect

app = Flask(__name__)
api = Api(app)
DATABASE_HOST = 'mongodb'

DATABASE_NAME = 'BookRentalManager'
app.config['MONGO_DBNAME'] = DATABASE_NAME
app.config['MONGO_URI'] = f'mongodb://{DATABASE_HOST}:27017/{DATABASE_NAME}'
URL = f'mongodb://{DATABASE_HOST}:27017/{DATABASE_NAME}'
connect(DATABASE_NAME, host=f'{DATABASE_HOST}:27017')

CORS(app, resources={r'/*': {'origins': '*'}})

logger = get_logger('API')

customers_parser = reqparse.RequestParser()
customers_parser.add_argument(
    'name', type=str, help="Cutomer's name", store_missing=False)
customers_parser.add_argument(
    'phone', type=str, help="Customer's phone number", store_missing=False)


def result(f):
    @wraps(f)
    def func(*args, **kwargs):
        try:
            connect(DATABASE_NAME, host=f'{DATABASE_HOST}:27017')
            r = f(*args, **kwargs)
            return r
            # return make_response(jsonify(result), 200)
        except ValueError as e:
            logger.exception(msg=str(e), exc_info=e)
            api.abort(404, 'There is not the index')
        except Exception as e:
            logger.exception(msg=str(e), exc_info=e)
            disconnect()
            raise
        finally:
            disconnect()
    return func


@api.route('/customers')
class Customers(Resource):
    @result
    def get(self):
        args = customers_parser.parse_args()
        queries = dict()
        for arg in args:
            queries[f'{arg}__icontains'] = args[arg]
        values = Customer.objects(**queries).to_json()
        return json.loads(values)

    @result
    def post(self):
        request.get_json(force=True)
        args = customers_parser.parse_args()
        logger.debug(args)
        customer = Customer(**args)
        customer.save()
        return None


@api.route('/customers/<int:customer_id>')
class Customers(Resource):
    def get_customer(self, customer_id):
        customer = Customer.objects(customer_id=customer_id).fields(id=0).first()
        if not customer:
            raise ValueError('The index of the item is not existed.')
        return customer

    @result
    def get(self, customer_id):
        customer = self.get_customer(customer_id)
        return customer.to_mongo().to_dict()

    @result
    def patch(self, customer_id):
        args = customers_parser.parse_args()
        Customer.objects(customer_id=customer_id).update(**args)
        return None

    @result
    def delete(self, customer_id):
        Customer.objects(customer_id=customer_id).delete()
        return None

book_parser = reqparse.RequestParser()
book_parser.add_argument(
    'title', type=str, help="The title of the book", store_missing=False)
book_parser.add_argument(
    'author', type=str, help="The author of the book", store_missing=False)
book_parser.add_argument('publisher', type=str,
                         help="Publisher's name", store_missing=False)


@api.route('/books')
class Books(Resource):
    @result
    def get(self):
        args = book_parser.parse_args()
        queries = dict()
        for arg in args:
            queries[f'{arg}__icontains'] = args[arg]
        values = Book.objects(**queries).to_json()
        return json.loads(values)

    @result
    def post(self):
        request.get_json(force=True)
        args = book_parser.parse_args()
        customer = Book(**args)
        customer.save()
        return None


@api.route('/books/<int:book_id>')
class Books(Resource):
    @result
    def get(self, book_id):
        book = Book.objects(book_id=book_id).first()
        return book.to_mongo().to_dict()

    @result
    def patch(self, book_id):
        args = customers_parser.parse_args()
        Book.objects(book_id=book_id).update(**args)
        return None

    @result
    def delete(self, book_id):
        Book.objects(book_id=book_id).delete()
        return None


rental_parser = reqparse.RequestParser()
rental_parser.add_argument('book_id', type=int, help="The title of the book")
rental_parser.add_argument('customer_id', type=int,
                           help="The author of the book")
rental_parser.add_argument('rental_start', type=str, help="Publisher's name")
rental_parser.add_argument('rental_end', type=str,
                           help="Publisher's name", store_missing=False)
rental_parser.add_argument('limit', type=int)
rental_parser.add_argument('offset', type=int)


# class DateTimeField(fields.Raw):
#     """
#     데이터 직렬화
#     fields.DateTime에서 datetime 객체를 제대로 파싱하지 못하여 null을
#     리턴. 따로 만들어서 사용
#     """
#
#     def format(self, value):
#         return value.isoformat() if isinstance(value, datetime.datetime) else None
#
#
# model_rental = api.model('Rental', {
#     'id': fields.Integer,
#     'book_id': fields.Integer,
#     'customer_id': fields.Integer,
#     'rental_start': DateTimeField(attribute='rental_start'),
#     'rental_end': DateTimeField(attribute='rental_end')
# })
#

@api.route('/rentals')
class Retanls(Resource):
    @result
    def get(self):
        args = rental_parser.parse_args()
        queries = dict()
        logger.debug(args)
        # WHERE

        if args.setdefault('book_id', None):
            book = Book.objects(book_id=args['book_id']).first()
            queries[f'book'] = book

        if args.setdefault('customer_id', None):
            customer = Customer.objects(customer_id=args['customer_id']).first()
            queries[f'customer'] = customer

        # DATE TIME
        if args.setdefault('rental_start', None):
            dt = datetime.datetime.fromisoformat(args['rental_start'])
            queries[f'rental_start__lte'] = dt

        if args.setdefault('rental_end', None):
            if args['rental_end']:
                dt = datetime.datetime.fromisoformat(args['rental_end'])
                queries[f'rental_end__gte'] = dt
            else:
                queries[f'rental_end__gte'] = None

        # OFFSET/LIMIT
        offset = args.setdefault('offset', None)
        limit = args.setdefault('limit', None)
        values = Rental.objects(**queries)[offset:limit].to_json()
        return json.loads(values)

        # # WHERE
        # target = ['customer_id', 'book_id']
        # for t in target:
        #     if args[t] is None:
        #         continue
        #     query = query.filter_by(**{t: args[t]})

        # DATE TIME
        # if args['rental_start']:
        #     dt = datetime.datetime.fromisoformat(args['rental_start'])
        #     query = query.filter(Rental.rental_start >= dt)
        # if hasattr(args, 'rental_end'):
        #     if args['rental_end']:
        #         dt = datetime.datetime.fromisoformat(args['rental_end'])
        #         query = query.filter(Rental.rental_end <= dt)
        #     else:
        #         query = query.filter_by(rental_end=None)
        #
        # # OFFSET/LIMIT
        # if getattr(args, 'limit'):
        #     query = query.limit(args['limit'])
        # if getattr(args, 'offset'):
        #     query = query.offset(args['offset'])
        #
        # data = query.all()
        # return data

    @result
    def post(self):
        request.get_json(force=True)
        logger.debug(request)
        args = rental_parser.parse_args()
        customer = Customer.objects(customer_id=args['customer_id']).first()
        book = Book.objects(book_id=args['book_id']).first()
        rental = Rental(customer=customer, book=book)
        rental.save()
        return None
#
#
# @api.route('/rentals/<int:rental_id>')
# class Rentals(Resource):
#     def get_a_rental(self, rental_id):
#         rental = Rental.query.filter_by(id=rental_id).one()
#         return rental
#
#     @result
#     @api.marshal_with(model_rental)
#     def get(self, rental_id):
#         rental = self.get_a_rental(rental_id)
#         return rental
#
#     @result
#     def patch(self, rental_id):
#         args = rental_parser.parse_args()
#         rental = self.get_a_book(rental_id)
#         rental.query.update(args)
#         db_session.commit()
#         return None
#
#     @result
#     def delete(self, rental_id):
#         rental = self.get_a_book(rental_id)
#         db_session.delete(rental)
#         db_session.commit()
#         return None
