from app.services import HelloWorldService


class MockRequest:
	def __repr__(self):
		return 'test'


class TestHelloWorld:
	def test_hello_world(self):
		response = HelloWorldService.handle_request(MockRequest())
		assert 'Hello World' in response
