"""
BaseTest

This class should be the parent class to each non-unit test.
It allows for instantiation of the database dynamically
and makes sure that it is a new, blank database each time.
IT IS USED FOR EVERY TESTS EXCEPT UNITTEST
"""

from unittest import TestCase
from app import app
from db import db


class BaseTest(TestCase):
        
    @classmethod
    def setUpClass(cls):
        """ runs once for each test class """
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'
        app.config['DEBUG'] = False  # this prevents flask from throwing error to say we initialised app_context twice, when we do so in the system test item_test.py
        app.config['PROPAGATE_EXCEPTIONS'] = True  # ensures when an errror occurs in the application, it is caught only by the @app.errorhandler. PROPAGATE_EXCEPTIONS is automatically set to true when debug is false. since we changed debug's value to false, it affects the exception too
        with app.app_context():
            # initialise app once 
            db.init_app(app)
            
    def setUp(self):
        # runs once for each test case
        # Make sure database exists
        with app.app_context():
            db.create_all()
        # Get a test client
        self.app = app.test_client  # gives us new test client for every test
        self.app_context = app.app_context

    def tearDown(self):
        # ensure Database is blank at the end of each test
        with app.app_context():
            db.session.remove()
            db.drop_all()

