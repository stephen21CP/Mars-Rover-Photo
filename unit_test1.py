import unittest
from flask import Flask
from flask_testing import TestCase
from travel_data_controller import app, collection

class EditRecordTestCase(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        return app

    def setUp(self):
        # Add a sample record to the test database
        sample_record = {
            "ref_number": "TEST001",
            "disclosure_group": "Test Group",
        }
        collection.insert_one(sample_record)

    def tearDown(self):
        # Remove the sample record from the test database after the test
        collection.delete_one({"ref_number": "TEST001"})

    def test_edit_record(self):
        # Edit the sample record
        response = self.client.post('/edit_record/TEST001', data={
            'ref_number': 'TEST001',
            'disclosure_group': 'Updated Test Group'
        }, follow_redirects=True)

        # Check if the response is successful (status code 200)
        self.assert200(response)

        # Check if the edited record is displayed on the list_records page
        self.assertIn(b'Updated Test Group', response.data)
        # Add other assertions for the edited fields as needed for the test

if __name__ == '__main__':
    unittest.main()
