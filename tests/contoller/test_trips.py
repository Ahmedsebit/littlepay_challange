import json
import unittest
from pathlib import Path
from app.app import create_app, db


class TripsContollerTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.file = open(Path('tests/trips.csv'), 'rb')
        
        with self.app.app_context():
            db.session.close()
            db.drop_all()
            db.create_all()
        
           
    def test_upload_trips(self):
        data = {"file":self.file}
        response = self.client().post('/api/littlepay/trips/upload', 
                                        data = data,
                                        content_type = 'multipart/form-data'
                                    )
        self.assertEqual(200, response.status_code)
    
    
    