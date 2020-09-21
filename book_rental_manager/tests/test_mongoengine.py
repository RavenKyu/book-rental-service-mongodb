import unittest
import datetime
from mongoengine import connect, disconnect
from book_rental_manager.models import Customer
from book_rental_manager.models import Book
from book_rental_manager.models import Rental


class TestPerson(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        connect('mongoenginetest', host='mongomock://localhost')

    @classmethod
    def tearDownClass(cls):
       disconnect()

    def test0100_check_model_customer(self):
        customer = Customer(name='Raven', phone='010-9508-1111')
        customer.save()
        # fresh_pers = Customer.objects().exclude('id').first()
        self.assertEqual(customer.name, 'Raven')

    def test0110_find_customer(self):
        customer_1 = Customer(name='Raven', phone='010-9508-1111')
        customer_1.save()
        customer_2 = Customer(name='Julia', phone='010-9508-1112')
        customer_2.save()
        # results = Customer.objects({}).exclude('id').as_pymongo()
        results = Customer.objects().fields(id=0).to_json()
        # results = Customer.objects().fields(id=0).to_mongo().to_dict()

        print(results)

    def test0120_patch_model_customer(self):
        customer = Customer(name='Raven', phone='010-9508-1111')
        customer.save()
        Customer.objects().update(name="Julia")
        customer.reload()
        # fresh_pers = Customer.objects().exclude('id').first()
        self.assertEqual(customer.name, 'Julia')
        self.assertEqual(customer.phone, '010-9508-1111')

    def test0130_delete_model_customer(self):
        customer = Customer(name='Raven', phone='010-9508-1111')
        customer.save()
        result = Customer.objects(customer_id=1).delete()
        print(result)
        result = Customer.objects(customer_id=1)
        print(result)
        # self.assertEqual(customer.name, 'Julia')
        # self.assertEqual(customer.phone, '010-9508-1111')

        # print([result.to_mongo().to_dict() for result in results])

    def test0200_create_rental(self):
        customer = Customer(name='Raven', phone='010-9508-1111')
        customer.save()
        book = Book(title="ABC", author='Julia', publisher='WinWin')
        book.save()

        rental = Rental(book=book, customer=customer)
        rental.rental_start = datetime.datetime(2020, 8, 15, 00, 00, 00)
        rental.save()

        result = Rental.objects().fields(id=0).first()
        print(result.to_json(follow_reference=True))


