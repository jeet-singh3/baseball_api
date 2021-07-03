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


def initial_table_creation():
    db = Postgres(db_string)
    db.run(
        "create table if not exists users(name varchar(1024), logins numeric)"
    )
    LOG.info("Executed command 0")
    db.run(
        "create unique index if not exists users_ux_01 on users(name)"
    )
    LOG.info("Executed command 1")
    db.run(
        "insert into users (name, logins) select 'random_person', 5 on conflict do nothing"
    )
    LOG.info("Executed command 2")


initial_table_creation()
