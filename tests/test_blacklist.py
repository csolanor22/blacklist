import json
from application import application
from faker import Faker
from unittest import TestCase

class TestEmailBlackList(TestCase):

    def setUp(self):
        self.client = application.test_client()
        self.data_factory = Faker()

        self.endpoint_health = '/'
        self.endpoint_create = '/blacklists/'
        self.endpoint_check = '/blacklists/'

        self.headers = {'Content-Type': 'application/json'}
        self.headers_token = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format("bearer_token")}
        self.headers_token_not_valid = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format("token")}

        self.uuid = self.data_factory.uuid4()
        self.email = self.data_factory.email()
        self.email_notvalid = self.data_factory.word()
        self.reason = self.data_factory.text()


    def test_health(self):
        req_health = self.client.get(self.endpoint_health, headers = self.headers)
        # print(req_health.get_data())
        self.assertEqual(req_health.status_code, 200)

    def test_create_400_token_not_in_header(self):
        new_email = {}
        req_create = self.client.post(self.endpoint_create, data=json.dumps(new_email), headers=self.headers)
        #print(req_create.get_data())
        self.assertEqual(req_create.status_code, 400)

    def test_create_401_token_notvalid(self):
        new_email = {}
        req_create = self.client.post(self.endpoint_create, data=json.dumps(new_email), headers=self.headers_token_not_valid)
        #print(req_create.get_data())
        self.assertEqual(req_create.status_code, 401)

    def test_create_400_email_missing(self):
        new_email = {}
        req_create = self.client.post(self.endpoint_create, data=json.dumps(new_email), headers=self.headers_token)
        #print(req_create.get_data())
        self.assertEqual(req_create.status_code, 400)

    def test_create_400_email_empty(self):
        new_email = {
            "email": ""
        }
        req_create = self.client.post(self.endpoint_create, data=json.dumps(new_email), headers=self.headers_token)
        #print(req_create.get_data())
        self.assertEqual(req_create.status_code, 400)

    def test_create_400_email_format_notvalid(self):
        new_email = {
            "email": self.email_notvalid
        }
        req_create = self.client.post(self.endpoint_create, data=json.dumps(new_email), headers=self.headers_token)
        #print(req_create.get_data())
        self.assertEqual(req_create.status_code, 400)

    def test_create_400_app_uuid_missing(self):
        new_email = {
            "email": self.email
        }
        req_create = self.client.post(self.endpoint_create, data=json.dumps(new_email), headers=self.headers_token)
        #print(req_create.get_data())
        self.assertEqual(req_create.status_code, 400)

    def test_create_400_app_uuid_empty(self):
        new_email = {
            "email": self.email,
            "app_uuid": ''
        }
        req_create = self.client.post(self.endpoint_create, data=json.dumps(new_email), headers=self.headers_token)
        #print(req_create.get_data())
        self.assertEqual(req_create.status_code, 400)

    def test_create_400_app_uuid_empty(self):
        new_email = {
            "email": self.email,
            "app_uuid": ''
        }
        req_create = self.client.post(self.endpoint_create, data=json.dumps(new_email), headers=self.headers_token)
        #print(req_create.get_data())
        self.assertEqual(req_create.status_code, 400)

    def test_create_201_reason_missing(self):
        new_email = {
            "email": self.email,
            "app_uuid": self.uuid
        }
        req_create = self.client.post(self.endpoint_create, data=json.dumps(new_email), headers=self.headers_token)
        #print(req_create.get_data())
        self.assertEqual(req_create.status_code, 201)

    def test_create_201_reason_empty(self):
        new_email = {
            "email": self.email,
            "app_uuid": self.uuid,
            "blocked_reason": ''
        }
        req_create = self.client.post(self.endpoint_create, data=json.dumps(new_email), headers=self.headers_token)
        #print(req_create.get_data())
        self.assertEqual(req_create.status_code, 201)

    def test_create_201_reason(self):
        new_email = {
            "email": self.email,
            "app_uuid": self.uuid,
            "blocked_reason": self.reason
        }
        req_create = self.client.post(self.endpoint_create, data=json.dumps(new_email), headers=self.headers_token)
        #print(req_create.get_data())
        self.assertEqual(req_create.status_code, 201)

'''
    def test_get_404(self):
        new_offer = {
            "postId": self.data_factory.random_number(digits=3, fix_len=True),
            "description": self.data_factory.text(),
            "size": "MEDIUM",
            "fragile": True, #self.data_factory.boolean,
            "offer": self.data_factory.random_number(digits=3, fix_len=True)
        }
        mock_token_validation.return_value = self.token_validation_resp
        req_create = self.client.post(self.endpoint_create, data=json.dumps(new_offer), headers=self.headers_token)
        resp_create = json.loads(req_create.get_data())
        self.assertEqual(req_create.status_code, 201)

        endpoint_get = '/offers/{}000'.format(str(resp_create["id"])) 
        req_get = self.client.get(endpoint_get, headers=self.headers_token)
        json.loads(req_get.get_data())
        self.assertEqual(req_get.status_code, 404)

    def test_get_401_notvalid(self):
        mock_token_validation.return_value = {'msg': 'not valid token', 'status_code': 401}
        endpoint_get = '/offers/{}000'.format(str(self.data_factory.random_number(digits=3, fix_len=True))) 
        req_get = self.client.get(endpoint_get, headers=self.headers_token)
        json.loads(req_get.get_data())
        self.assertEqual(req_get.status_code, 401)

    def test_get_401_expired(self):
        mock_token_validation.return_value = {'msg': 'expired token', 'status_code': 401}
        endpoint_get = '/offers/{}000'.format(str(self.data_factory.random_number(digits=3, fix_len=True))) 
        req_get = self.client.get(endpoint_get, headers=self.headers_token)
        json.loads(req_get.get_data())
        self.assertEqual(req_get.status_code, 401)

    def test_get_400(self):
        mock_token_validation.return_value = self.token_validation_resp
        endpoint_get = '/offers/{}'.format("test") 
        req_get = self.client.get(endpoint_get, headers=self.headers_token)
        req_get.get_data()
        self.assertEqual(req_get.status_code, 400)

    def test_get_200(self):
        new_offer = {
            "postId": self.data_factory.random_number(digits=3, fix_len=True),
            "description": self.data_factory.text(),
            "size": "MEDIUM",
            "fragile": True, #self.data_factory.boolean,
            "offer": self.data_factory.random_number(digits=3, fix_len=True)
        }
        mock_token_validation.return_value = self.token_validation_resp
        req_create = self.client.post(self.endpoint_create, data=json.dumps(new_offer), headers=self.headers_token)
        resp_create = json.loads(req_create.get_data())
        self.assertEqual(req_create.status_code, 201)

        mock_token_validation.return_value = self.token_validation_resp
        endpoint_get = '/offers/{}'.format(str(resp_create["id"])) 
        req_get = self.client.get(endpoint_get, headers=self.headers_token)
        resp_get = json.loads(req_get.get_data())
        self.assertEqual(new_offer["postId"], resp_get["postId"])
        self.assertEqual(new_offer["offer"], resp_get["offer"])
        self.assertEqual(req_get.status_code, 200)
'''