import unittest
import os

'''
Make sure that weather logger exists
'''
class TestBasicFunctionality(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue(os.path.exists("data/weather_log.csv"),
                        "weather_log.csv does not exist")

if __name__ == "__main__":
    unittest.main()
