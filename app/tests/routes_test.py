from . import app


def test_health_check():
	response = app.test_client().get('/api/v1/healthcheck')
	assert b'Ok' in response.data


def test_health_check_fail():
	try:
		response = app.test_client().get('/api/v1/healthchec')
	except Exception as error:
		assert b'404 NOT FOUND' in response.data
