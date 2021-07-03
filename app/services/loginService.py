import logging
import sys
from app.utils.db_utils import new_login, get_current_logins

LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
LOG.addHandler(handler)


class LoginService:
	@classmethod
	def handle_request(cls, request):
		username = request.form['username']
		login_successful = new_login(username)
		current_logins = int(get_current_logins(username))
		message_string = f"Login succeeded for user {username}, currently at {current_logins}" if \
			login_successful else f"Login failed for user {username}, currently remain at {current_logins}"
		return {
			"Login": login_successful,
			"Number": current_logins,
			"Message": message_string
		}
