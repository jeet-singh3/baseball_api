import logging
import sys
from app.utils.constants import PHILLIES_GAME
from app.utils.db_utils import get_pitchers_for_game
from app.services.pitcherIndividualGameService import PitcherIndividualGameService

LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
LOG.addHandler(handler)


class IndividualGameService:
    @classmethod
    def handle_request(cls, request):
        game_id = cls.validate_args(request)
        pitchers_for_game = get_pitchers_for_game(game_id)
        pitchers = []
        for pitcher in pitchers_for_game:
            pitcher_game_summary = PitcherIndividualGameService.handle_request(pitcher, game_id)
            pitchers.append(
                {
                    "pitcherId": pitcher,
                    "summary": pitcher_game_summary
                }
            )
        return pitchers

    @staticmethod
    def validate_args(request):
        if 'gameId' not in request.args:
            raise Exception('gameId is required to get pitcher game summary')
        game_id = request.args.get('gameId')
        if not game_id:
            return PHILLIES_GAME
        return game_id

