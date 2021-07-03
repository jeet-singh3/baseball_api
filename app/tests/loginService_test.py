from app.services.loginService import LoginService


class MockRequest:
	def __repr__(self):
		return 'test'
	form = {
		'username': 'test_username'
	}


class TestLoginService:
	def test_login_service(self):
		request = MockRequest()
		response = LoginService.handle_request(request)
		assert response["Login"]
		assert response["Number"] == 1
		assert 'Login succeeded' in response["Message"]


