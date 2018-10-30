import unittest
import json
from webapp import create_app, db
from webapp.auth.models import User, Role
from webapp.admin import admin
from webapp.api import rest_api


class TestURLs(unittest.TestCase):

    def setUp(self):
        admin._views = []
        rest_api.resources = []

        app = create_app('config.TestConfig')
        self.client = app.test_client()
        db.app = app
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def _insert_user(self, username, password, role_name):
        test_role = Role(role_name)
        db.session.add(test_role)
        db.session.commit()

        test_user = User(username)
        test_user.set_password(password)
        db.session.add(test_user)
        db.session.commit()

    def test_root_redirect(self):
        """ Tests if the root URL gives a 302 """
        self._insert_user('test', 'test', 'default')
        result = self.client.get('/')
        self.assertEqual(result.status_code, 302)
        self.assertIn("/blog/", result.headers['Location'])

    def test_blog_home(self):
        """ Tests if the blog home page returns successfully """

        result = self.client.get('/blog/')
        self.assertEqual(result.status_code, 200)

    def test_login(self):
        """ Tests if the login form works correctly """

        self._insert_user('test', 'test', 'default')
        result = self.client.post('/auth/login', data=dict(
            username='test',
            password="test"
        ), follow_redirects=True)

        self.assertEqual(result.status_code, 200)
        self.assertIn('You have been logged in', str(result.data))

    def test_failed_login(self):
        self._insert_user('test', 'test', 'default')
        result = self.client.post('/auth/login', data=dict(
            username='test',
            password="badpassword"
        ), follow_redirects=True)

        self.assertEqual(result.status_code, 200)
        self.assertIn('Invalid username or password', str(result.data))
        result = self.client.get('/blog/new')
        self.assertEqual(result.status_code, 302)

    def test_unauthorized_access_to_admin(self):
        self._insert_user('test', 'test', 'default')
        result = self.client.post('/auth/login', data=dict(
            username='test',
            password="test"
        ), follow_redirects=True)
        result = self.client.get('/admin/customview/')
        self.assertEqual(result.status_code, 403)

    def test_unauthorized_access_to_post(self):
        self._insert_user('test', 'test', 'default')
        result = self.client.post('/auth/login', data=dict(
            username='test',
            password="test"
        ), follow_redirects=True)
        result = self.client.get('/blog/new')
        self.assertEqual(result.status_code, 403)

    def test_logout(self):
        """ Tests if the login form works correctly """

        self._insert_user('test', 'test', 'default')
        result = self.client.post('/auth/login', data=dict(
            username='test',
            password="test"
        ), follow_redirects=True)

        self.assertEqual(result.status_code, 200)
        self.assertIn('You have been logged in', str(result.data))

        result = self.client.get('/auth/logout', follow_redirects=True)

        self.assertEqual(result.status_code, 200)
        self.assertIn('You have been logged out', str(result.data))

    def test_api_jwt_login(self):
        self._insert_user('test', 'test', 'default')
        headers = {'content-type': 'application/json'}
        result = self.client.post('/auth/api', headers=headers, data='{"username":"test","password":"test"}')
        self.assertEqual(result.status_code, 200)

    def test_api_jwt_login(self):
        self._insert_user('test', 'test', 'default')
        headers = {'content-type': 'application/json'}
        result = self.client.post('/auth/api', headers=headers, data='{"username":"test","password":"test"}')
        self.assertEqual(result.status_code, 200)

    def test_api_jwt_failed_login(self):
        self._insert_user('test', 'test', 'default')
        headers = {'content-type': 'application/json'}
        result = self.client.post('/auth/api', headers=headers, data='{"username":"test","password":"test123"}')
        self.assertEqual(result.status_code, 401)

    def test_api_new_post(self):
        self._insert_user('test', 'test', 'default')
        headers = {'content-type': 'application/json'}
        result = self.client.post('/auth/api', headers=headers, data='{"username":"test","password":"test"}')
        access_token = json.loads(result.data)['access_token']
        headers['Authorization'] = "Bearer %s" % access_token
        result = self.client.post('api/post', headers=headers, data='{"title":"Text Title","text":"Changed"}')
        self.assertEqual(result.status_code, 201)


if __name__ == '__main__':
    unittest.main()
