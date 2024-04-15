import unittest
import requests

class TestGetQuestionAPI(unittest.TestCase):
    def test_get_question_response_success(self):
        """
        Test the get_question_response function for successful response.
        """
        url = "http://localhost:8000/get_question/"
        question = "who won boston marathon 2015?; did that person run a negative split?; What was this person overall time and 5k time?"
        data = {"question": question}
        response = requests.get(url, json=data)
        self.assertEqual(response.status_code, 200, f"Expected status code 200, but got {response.status_code}")
        self.assertTrue(response.json(), "Expected non-empty response")

    def test_get_question_response_failure(self):
        """
        Test the get_question_response function for failed response.
        """
        url = "http://localhost:8000/get_question/"
        question = 1
        data = {"question": question}
        response = requests.get(url, json=data)
        self.assertNotEqual(response.status_code, 200, f"Expected status code other than 200, but got {response.status_code}")

if __name__ == "__main__":
    unittest.main()
