import json
from application import application
from faker import Faker
from unittest import TestCase

class TestEmailBlackList(TestCase):

    def setUp(self):
        self.client = application.test_client()
        self.data_factory = Faker()

        self.headers = {'Content-Type': 'application/json'}
        self.headers_token = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format("bearer_token")}
        self.headers_token_not_valid = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format("token")}

        self.uuid = self.data_factory.uuid4()
        self.email = self.data_factory.email()
        self.email_notvalid = self.data_factory.word()
        self.reason = self.data_factory.text()

        self.endpoint_health = '/'
        self.endpoint_create = '/blacklists/'
        self.endpoint_check = '/blacklists/{}'.format(self.email)
        self.endpoint_check_not_exist = '/blacklists/{}'.format(self.email_notvalid)

    def test_health(self):
        print('Starting test_health')
        req_health = self.client.get(self.endpoint_health, headers = self.headers)
        # print(req_health.get_data())
        self.assertEqual(req_health.status_code, 200)

    def test_create_400_token_not_in_header(self):
        print('Starting test_create_400_token_not_in_header')
        new_email = {}
        req_create = self.client.post(self.endpoint_create, data=json.dumps(new_email), headers=self.headers)
        #print(req_create.get_data())
        self.assertEqual(req_create.status_code, 400)

    def test_create_401_token_notvalid(self):
        print('Starting test_create_401_token_notvalid')
        new_email = {}
        req_create = self.client.post(self.endpoint_create, data=json.dumps(new_email), headers=self.headers_token_not_valid)
        #print(req_create.get_data())
        self.assertEqual(req_create.status_code, 401)

    def test_create_400_email_missing(self):
        print('Starting test_create_400_email_missing')
        new_email = {}
        req_create = self.client.post(self.endpoint_create, data=json.dumps(new_email), headers=self.headers_token)
        #print(req_create.get_data())
        self.assertEqual(req_create.status_code, 400)

    def test_create_400_email_empty(self):
        print('Starting test_create_400_email_empty')
        new_email = {
            "email": ""
        }
        req_create = self.client.post(self.endpoint_create, data=json.dumps(new_email), headers=self.headers_token)
        #print(req_create.get_data())
        self.assertEqual(req_create.status_code, 400)

    def test_create_400_email_format_notvalid(self):
        print('Starting test_create_400_email_format_notvalid')
        new_email = {
            "email": self.email_notvalid
        }
        req_create = self.client.post(self.endpoint_create, data=json.dumps(new_email), headers=self.headers_token)
        #print(req_create.get_data())
        self.assertEqual(req_create.status_code, 400)

    def test_create_400_app_uuid_missing(self):
        print('Starting test_create_400_app_uuid_missing')
        new_email = {
            "email": self.email
        }
        req_create = self.client.post(self.endpoint_create, data=json.dumps(new_email), headers=self.headers_token)
        #print(req_create.get_data())
        self.assertEqual(req_create.status_code, 400)

    def test_create_400_app_uuid_empty(self):
        print('Starting test_create_400_app_uuid_empty')
        new_email = {
            "email": self.email,
            "app_uuid": ''
        }
        req_create = self.client.post(self.endpoint_create, data=json.dumps(new_email), headers=self.headers_token)
        #print(req_create.get_data())
        self.assertEqual(req_create.status_code, 400)

    def test_create_201_reason_missing(self):
        print('Starting test_create_201_reason_missing')
        new_email = {
            "email": self.email,
            "app_uuid": self.uuid
        }
        req_create = self.client.post(self.endpoint_create, data=json.dumps(new_email), headers=self.headers_token)
        #print(req_create.get_data())
        self.assertEqual(req_create.status_code, 201)

    def test_create_201_reason_empty(self):
        print('Starting test_create_201_reason_empty')
        new_email = {
            "email": self.email,
            "app_uuid": self.uuid,
            "blocked_reason": ''
        }
        req_create = self.client.post(self.endpoint_create, data=json.dumps(new_email), headers=self.headers_token)
        #print(req_create.get_data())
        self.assertEqual(req_create.status_code, 201)

    def test_create_201_reason(self):
        print('Starting test_create_201_reason')
        new_email = {
            "email": self.email,
            "app_uuid": self.uuid,
            "blocked_reason": self.reason
        }
        req_create = self.client.post(self.endpoint_create, data=json.dumps(new_email), headers=self.headers_token)
        #print(req_create.get_data())
        self.assertEqual(req_create.status_code, 201)        
        
    def test_check_400_token_not_in_header(self):
        print('Starting test_check_400_token_not_in_header')
        req = self.client.get(self.endpoint_check, headers=self.headers)
        #print(req.get_data())
        self.assertEqual(req.status_code, 400)

    def test_check_401_token_notvalid(self):
        print('Starting test_check_401_token_notvalid')
        req = self.client.get(self.endpoint_check, headers=self.headers_token_not_valid)
        #print(req.get_data())
        self.assertEqual(req.status_code, 401)

    def test_check_200_email_not_blocked(self):
        print('Starting test_check_200_email_not_blocked')
        req = self.client.get(self.endpoint_check_not_exist, headers=self.headers_token)
        resp = json.loads(req.get_data())
        self.assertEqual(req.status_code, 200)
        self.assertFalse(resp["blocked"])

    def test_check_200_email_blocked(self):
        print('Starting test_check_200_email_blocked')
        new_email = {
            "email": self.email,
            "app_uuid": self.uuid,
            "blocked_reason": self.reason
        }
        req_create = self.client.post(self.endpoint_create, data=json.dumps(new_email), headers=self.headers_token)
        #print(req_create.get_data())
        self.assertEqual(req_create.status_code, 201)

        #print(self.endpoint_check)
        req = self.client.get(self.endpoint_check, headers=self.headers_token)
        resp = json.loads(req.get_data())
        self.assertEqual(req.status_code, 200)
        self.assertTrue(resp["blocked"])
    
    def test_failed_test(self):
        print('Starting test_failed_test')
        self.assertTrue(False)
