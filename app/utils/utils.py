import logging
import sys
from app.utils.constants import MAX_SCHERZER, PHILLIES_GAME

LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
LOG.addHandler(handler)


def validate_args(request):
    if 'pitcherId' not in request.args or 'gameId' not in request.args:
        raise Exception("pitcherId and gameId is required to get pitcher's individual game summary")
    pitcher_id = request.args.get('pitcherId')
    game_id = request.args.get('gameId')
    if not pitcher_id:
        return MAX_SCHERZER, PHILLIES_GAME
    if not game_id:
        return MAX_SCHERZER, PHILLIES_GAME
    return pitcher_id, game_id


