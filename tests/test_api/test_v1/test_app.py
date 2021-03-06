#!/usr/bin/python3
"""
Unit tests for app.py
"""
from models import storage
from api.v1.app import app
import json
from sys import getdefaultencoding as defenc
import unittest


class Test_app_py(unittest.TestCase):
    """
    Tests the app.py file to see if the methods and endpoints are working
    properly.
    """
    def setUp(self):
        """
        Sets up the app for testing
        """
        self.test_app = app.test_client()

    def test_app_error_handler_404(self):
        """
        Tests the errorhandler(404) method
        """
        response = self.test_app.get('/api/v1/views/error')
        self.assertEqual(json.loads(
            response.get_data().decode(defenc())), {'error': 'Not found'})
