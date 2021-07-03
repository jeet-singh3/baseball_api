from app.utils.db_utils import get_current_logins, new_login


def test_get_current_logins():
	logins_for_tes_person = get_current_logins('random_person')
	assert logins_for_tes_person == 5


def test_new_login():
	new_user_login = new_login("new_user")
	assert new_user_login
