import logging
import sys
from app.utils.db_utils import search_games

LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
LOG.addHandler(handler)


class GameService:
    @classmethod
    def handle_request(cls, request):
        game_date, home_team, away_team = cls.validate_args(request)
        games = search_games(game_date, home_team, away_team)
        return {
            'games': games,
            'count': len(games),
            'date': game_date
        }

    @staticmethod
    def validate_args(request):
        home_team = request.args.get('homeTeam') if 'homeTeam' in request.args else ''
        away_team = request.args.get('awayTeam') if 'awayTeam' in request.args else ''
        game_date = request.args.get('gameDate') if 'gameDate' in request.args else ''
        if not isinstance(home_team, str) or not isinstance(away_team, str):
            raise Exception("homeTeam and awayTeam must be strings")
        home_team = False if home_team == '' else home_team.upper()
        away_team = False if away_team == '' else away_team.upper()
        game_date = False if game_date == '' else game_date
        return game_date, home_team, away_team
