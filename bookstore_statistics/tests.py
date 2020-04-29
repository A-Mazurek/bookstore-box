from django.test import TestCase, Client
from django.core.management import call_command


class APITestCase(TestCase):
    def setUp(self):
        self.client = Client(HTTP_USER_AGENT='Mozilla/5.0')

        call_command('csv_load', 'all')

    def test_if_response_of_api_end_point_works_properly(self):
        # checking for incorrect url, it should be status 404
        error_response = self.client.get('/api/summarry/alll')
        self.assertEqual(error_response.status_code, 404)
        # checking for correct url, it should be status 200
        response = self.client.get('/api/summary/all')
        self.assertEqual(response.status_code, 200)

    def test_if_json_of_end_point_contain_right_data(self):
        response = self.client.get('/api/summary/all')
        json_response = response.json()
        self.assertEqual(json_response['total_number_of_books'], 3)
        self.assertEqual(json_response['total_number_of_books_publisher_name'], 1)
        self.assertEqual(json_response['books_price_statistics']['price_diff'], 1.0)
        self.assertEqual(json_response['books_price_statistics']['price__min'], 10.0)
        self.assertEqual(json_response['books_price_statistics']['price__max'], 12.0)
        self.assertEqual(json_response['books_price_statistics']['price__avg'], 11.0)
        self.assertEqual(json_response['publisher_num_books']['Publisher1'], 1)
        self.assertEqual(json_response['publisher_num_books']['Publisher2'], 1)
        self.assertEqual(json_response['publisher_num_books']['Publisher3'], 1)
        self.assertEqual(json_response['books_rank_below_2']['Publisher1'], 1)
        self.assertEqual(json_response['books_rank_below_2']['Publisher2'], 1)
        self.assertEqual(json_response['books_rank_below_2']['Publisher3'], 0)
        self.assertEqual(json_response['books_rank_above_2']['Publisher1'], 0)
        self.assertEqual(json_response['books_rank_above_2']['Publisher2'], 0)
        self.assertEqual(json_response['books_rank_above_2']['Publisher3'], 1)
        self.assertEqual(json_response['top_2_publishers_number_of_books']['Publisher2'], 1)
        self.assertEqual(json_response['top_2_publishers_number_of_books']['Publisher3'], 1)
