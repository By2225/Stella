import app
import os
import unittest
import keys

class AppTestCase(unittest.TestCase):

    def setUp(self):
        os.environ['ACCESS_TOKEN'] = 'Test_Access'
        os.environ['VERIFY_TOKEN'] = 'Test_Verify'
        #app.config['TESTING'] = True

        self.app = app.app.test_client()

    # executed after each test
    def tearDown(self):
        pass

    """Begin Tests"""
    def test_main_page(self):
        response = self.app.get('/',follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    #TODO write send message test
    def test_send_message(self):
        pass

    #TODO write send payments test
    def test_send_payments(self):
        pass


if __name__ == '__main__':
    unittest.main()
