import os
import logging
import sys
from postgres import Postgres

LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
LOG.addHandler(handler)

db_string = f"postgres://{os.getenv('PG_USER')}:{os.getenv('PG_PASS')}@" \
            f"{os.getenv('PG_HOST')}:{os.getenv('PG_PORT')}/{os.getenv('PG_NAME')}"

PG_DB = Postgres(db_string)


def get_current_logins(username):
	try:
		current_logins = PG_DB.one("SELECT logins from users where name=%(name)s", {
			"name": username
		})
		return current_logins
	except Exception as error:
		LOG.error(f"Something broke: {error}")
		raise Exception("Database Error")


def new_login(username):
	current_logins = get_current_logins(username)
	current_logins = 0 if current_logins is None else current_logins
	current_logins += 1
	sql_stmt = "insert into users (name, logins) select %(user_name)s, %(user_logins)s on conflict (name) " \
	           "do update set name = %(user_name)s, logins = %(user_logins)s"

	try:
		PG_DB.run(sql_stmt, {
			"user_name": username,
			"user_logins": current_logins
		})
		return True
	except Exception as error:
		LOG.error(f"Error running sql statement: {error}")
		return False