import unittest
import json
import os
from unittest.mock import MagicMock, patch
from Task import DataProcessor

class TestDataProcessor(unittest.TestCase):
    def setUp(self):
        self.data_processor = DataProcessor()

    def test_load_replacements(self):
        with open('test_replacements.json', 'w') as temp_file:
            json.dump([{'replacement': 'foo', 'source': 'bar'}], temp_file)

        replacements = self.data_processor.load_replacements('test_replacements.json')

        self.assertEqual(replacements, [{'replacement': 'foo', 'source': 'bar'}])

    def test_load_original_data(self):
        mock_response = MagicMock()
        mock_response.text = json.dumps(['message1', 'message2'])
        with patch('requests.get', return_value=mock_response):
            data_url = 'https://example.com/data.json'
            original_data = self.data_processor.load_original_data(data_url)

        self.assertEqual(original_data, ['message1', 'message2'])

    def test_apply_replacements(self):
        original_data = ['hello, world!', 'foo is great']
        replacements = [{'replacement': 'foo', 'source': 'bar'}, {'replacement': 'world', 'source': None}]
        fixed_data = self.data_processor.apply_replacements(original_data, replacements)

        expected_fixed_data = ['hello, !', 'bar is great']
        self.assertEqual(fixed_data, expected_fixed_data)

    def tearDown(self):
        try:
            os.remove('test_replacements.json')
            os.remove('test_result.json')
        except FileNotFoundError:
            pass

if __name__ == '__main__':
    unittest.main()