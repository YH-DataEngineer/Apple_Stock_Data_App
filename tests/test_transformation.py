#local testing 

import unittest
import json
from transformation import transform_json_to_relational  # Your main function

class TestTransformation(unittest.TestCase):
    
    def setUp(self):
        # Load sample JSON fixture
        with open('tests/test_data.json', 'r') as f:
            self.sample_json = json.load(f)
    
    def test_transform_shape(self):
        """Test JSON → rows transformation"""
        rows = transform_json_to_relational(self.sample_json)
        
        self.assertEqual(len(rows), 5)  # Expect 5 days
        self.assertEqual(rows[0]['symbol'], 'AAPL')
        self.assertIsInstance(rows[0]['date'], str)
        self.assertIsInstance(rows[0]['volume'], int)
    
    def test_handles_missing_data(self):
        """Test graceful handling of incomplete OHLCV arrays"""
        rows = transform_json_to_relational(self.sample_json)
        # Should handle arrays of different lengths safely
        self.assertIsNotNone(rows[-1]['close'])  # Last row still works

if __name__ == '__main__':
    unittest.main()
