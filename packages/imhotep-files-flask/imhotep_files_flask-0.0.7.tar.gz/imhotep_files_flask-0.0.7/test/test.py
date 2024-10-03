import unittest
import os
import json
from imhotep_files_flask.app import app  # Use absolute import

class FlaskAppTests(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.app = app
        cls.client = cls.app.test_client()
        cls.app.config['TESTING'] = True
        cls.upload_folder = 'uploads'
        os.makedirs(cls.upload_folder, exist_ok=True)

    @classmethod
    def tearDownClass(cls):
        # Clean up after tests
        for file in os.listdir(cls.upload_folder):
            os.remove(os.path.join(cls.upload_folder, file))
        os.rmdir(cls.upload_folder)

    def test_upload_file_valid(self):
        data = {
            'file_name': 'test_file',
        }
        with open('test_file.txt', 'w') as f:  # Create a sample file for testing
            f.write('This is a test file.')

        with open('test_file.txt', 'rb') as f:
            response = self.client.post('/upload', data={'file': f, **data})

        self.assertEqual(response.status_code, 200)
        self.assertIn('file_path', json.loads(response.data))

    def test_upload_file_invalid_extension(self):
        data = {
            'file_name': 'test_file_invalid',
        }
        with open('test_file_invalid.pdf', 'w') as f:  # Create an invalid file for testing
            f.write('This is an invalid file.')

        with open('test_file_invalid.pdf', 'rb') as f:
            response = self.client.post('/upload', data={'file': f, **data})

        self.assertEqual(response.status_code, 400)
        self.assertIn('error', json.loads(response.data))

    def test_delete_file_valid(self):
        # First, upload a valid file
        data = {
            'file_name': 'delete_test',
        }
        with open('delete_test.txt', 'w') as f:  # Create a sample file for uploading
            f.write('This file will be deleted.')

        with open('delete_test.txt', 'rb') as f:
            self.client.post('/upload', data={'file': f, **data})

        # Attempt to delete the file
        file_path = os.path.join(self.upload_folder, 'delete_test.txt')
        response = self.client.delete('/delete', json={'file_path': file_path})

        self.assertEqual(response.status_code, 200)
        self.assertIn('message', json.loads(response.data))

    def test_delete_file_not_exist(self):
        response = self.client.delete('/delete', json={'file_path': 'non_existent_file.txt'})
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', json.loads(response.data))

if __name__ == '__main__':
    unittest.main()
