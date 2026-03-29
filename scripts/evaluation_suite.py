import os
import unittest
import datetime
from app import create_app, db
from app.models.event import Event
from app.models.user import User
from app.services.nlp_utils import extract_keywords, tokenize_interests
from flask import json

class CERSComprehensiveTestSuite(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.app.config['TESTING'] = True
        cls.app.config['WTF_CSRF_ENABLED'] = False
        cls.client = cls.app.test_client()
        with cls.app.app_context():
            db.create_all()

    @classmethod
    def tearDownClass(cls):
        with cls.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_01_basic_home_screen_visible(self):
        """1. Basic: Test if available events are visible on Home Screen"""
        # We assume the mock_run already populated the DB, but let's check the route
        resp = self.client.get('/events/') # The catalog page
        self.assertEqual(resp.status_code, 200, "Events catalog should load successfully")

    def test_02_nltk_case_and_punctuation(self):
        """2a. NLTK Brain: Case Sensitivity & Punctuation"""
        # "Workshop," vs "workshop!" vs "WORKSHOP"
        res1 = extract_keywords("Workshop,")
        res2 = extract_keywords("workshop!")
        res3 = extract_keywords("WORKSHOP")
        self.assertEqual(res1, res2)
        self.assertEqual(res2, res3)
        self.assertTrue(len(res1) > 0, "Should extract 'workshop'")

    def test_03_nltk_stop_words(self):
        """2b. NLTK Brain: Stop Words"""
        res = extract_keywords("The boy and the dog went to a workshop")
        # Should not contain 'the', 'and', 'to', 'a'
        tokens = res.split(',')
        for word in ['the', 'and', 'to', 'a']:
            self.assertNotIn(word, tokens)
    
    def test_04_nltk_garbage_input(self):
        """2c. NLTK Brain: Garbage Input / Emojis"""
        try:
            res = extract_keywords("😎🔥 a b c 123 !")
            self.assertEqual(res, "", "Garbage should result in empty extraction without throwing ValueError")
        except ValueError:
            self.fail("extract_keywords threw ValueError on garbage input")

    def test_05_sqlite_data_types(self):
        """3b. SQLite Data Types Validation"""
        # Try to insert string into integer max_capacity column
        with self.app.app_context():
            # Test SQLAlchemy/form validation instead! 
            # Send string capacity to creation endpoint. Needs an admin.
            with self.client.session_transaction() as sess:
                sess['_user_id'] = '1' # Assuming admin created in setup
            resp = self.client.post('/events/new', data={
                'title': 'Test Invalid', 'description': 'Desc', 'category_id': '1', 
                'date': '2027-10-10', 'time': '14:00', 'location': 'Loc', 'capacity': 'STRING_CAPACITY'
            })
            self.assertEqual(resp.status_code, 200) # Form fails validation and re-renders with 200 ok
            self.assertIn(b"Not a valid integer value", resp.data)

    def test_06_flask_security_malformed_request(self):
        """6b. Test Malformed request / Bad Request"""
        # Send garbage json to a route, usually Flask drops it and redirects or returns 400
        resp = self.client.post('/register/1', data="GARBAGE_DATA_NOT_JSON_OR_FORM", content_type='application/json')
        self.assertEqual(resp.status_code, 302) # Since login_required intercepts first, it gives 302/redirect safely
        
    def test_07_no_match_search(self):
        """6a. Test 'No Match' search returning empty cleanly"""
        resp = self.client.get('/events/?q=Supercalifragilisticexpialidocious_EVENT_THAT_DOES_NOT_EXIST')
        self.assertEqual(resp.status_code, 200)
        # Verify it loads without throwing 500 error
        self.assertIn(b"Discover Events", resp.data)

if __name__ == '__main__':
    unittest.main(verbosity=2)
