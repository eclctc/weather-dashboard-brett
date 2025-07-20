import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from unittest.mock import patch, MagicMock
from models.pollen_model import PollenModel


class TestPollenModel(unittest.TestCase):

    @patch('models.pollen_model.requests.get')
    def test_fetch_pollen_data_success(self, mock_get):
        # Mock API response structure
        mock_response_data = {
            'dailyInfo': [
                {
                    'pollenTypeInfo': [
                        {
                            'code': 'GRASS',
                            'indexInfo': {'value': 3},
                            'healthRecommendations': ['Stay indoors during afternoon.']
                        },
                        {
                            'code': 'TREE',
                            'indexInfo': {'value': 2},
                            'healthRecommendations': ['Wear a mask if outside.']
                        },
                        {
                            'code': 'WEED',
                            'indexInfo': {'value': 4},
                            'healthRecommendations': []
                        }
                    ]
                }
            ]
        }

        # Configure mock
        mock_response = MagicMock()
        mock_response.json.return_value = mock_response_data
        mock_response.status_code = 200
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        model = PollenModel(api_key="fake-key")
        data, source = model.fetch_pollen_data()

        # Assertions
        self.assertIsNotNone(data)
        self.assertEqual(data['grass'], 3)
        self.assertEqual(data['tree'], 2)
        self.assertEqual(data['weed'], 4)

        self.assertIn("Grass:", data['health_recommendations'][0])
        self.assertIn("Tree:", data['health_recommendations'][1])
        self.assertEqual(source, "Google Pollen API Data")

        # Ensure API call made with correct params
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        self.assertIn("location.latitude", kwargs['params'])
        self.assertEqual(kwargs['params']['location.latitude'], 33.749)
        self.assertEqual(kwargs['params']['location.longitude'], -84.388)


if __name__ == "__main__":
    unittest.main()
