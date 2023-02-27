import unittest
from datetime import datetime
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from Ecommerce.model import Admin, User, Seller, Category, Product, Order, ShippingAddress, Review, Cart, CartItem, Payment
from Ecommerce import create_app, db

class TestModels(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.app = create_app('testing')
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        db.create_all()

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()

    def setUp(self):
        db.session.begin(subtransactions=True)

    def tearDown(self):
        db.session.rollback()

    def test_admin_serialization(self):
        admin = Admin(name='John Doe', email='john.doe@example.com', password='secret')
        admin_schema = SQLAlchemyAutoSchema(model=Admin)
        result = admin_schema.dump(admin)
        expected = {'id': None, 'name': 'John Doe', 'email': 'john.doe@example.com', 'password': 'secret'}
        self.assertEqual(result, expected)

    def test_user_serialization(self):
        user = User(name='Jane Doe', email='jane.doe@example.com', public_id='abc123', password='secret')
        user_schema = SQLAlchemyAutoSchema(model=User)
        result = user_schema.dump(user)
        expected = {'id': None, 'name': 'Jane Doe', 'email': 'jane.doe@example.com', 'public_id': 'abc123', 'password': 'secret', 'is_confirmed': False, 'is_seller': False, 'categories': []}
        self.assertEqual(result, expected)

    def test_seller_serialization(self):
        seller = Seller(user_id=1)
        seller_schema = SQLAlchemyAutoSchema(model=Seller)
        result = seller_schema.dump(seller)
        expected = {'id': None, 'user_id': 1, 'products': []}
        self.assertEqual(result, expected)

    # More tests for other models

if __name__ == '__main__':
    unittest.main()
