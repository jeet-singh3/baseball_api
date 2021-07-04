import logging
import sys
from app.utils.db_utils import get_players

LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
LOG.addHandler(handler)


class PlayerService:
    @classmethod
    def handle_request(cls, request):
        name_use, name_last = cls.validate_args(request)
        players = get_players(name_use, name_last)
        return {
            'players': players,
            'count': len(players)
        }

    @staticmethod
    def validate_args(request):
        name_use = request.args.get('firstName') if 'firstName' in request.args else ''
        name_last = request.args.get('lastName') if 'lastName' in request.args else ''
        if not isinstance(name_use, str) or not isinstance(name_last, str):
            raise Exception("firstName and lastName must be strings")
        name_use = False if name_use == '' else name_use.capitalize()
        name_last = False if name_last == '' else name_last.capitalize()
        return name_use, name_last
