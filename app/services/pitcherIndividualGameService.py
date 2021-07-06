import logging
import sys
from app.utils.db_utils import get_pitch_types_by_game_id, get_average_fastball_velocity, get_player_name_by_id

LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
LOG.addHandler(handler)


class PitcherIndividualGameService:
    @classmethod
    def handle_request(cls, pitcher_id, game_id):
        player_pitch_types_by_game = get_pitch_types_by_game_id(game_id, pitcher_id)
        game_summary, pitch_count = cls.calculate_game_summary(player_pitch_types_by_game)
        summary = {"gameId": game_id,
                   "summary": game_summary,
                   "pitchCount": pitch_count,
                   "averageFastballVelocity": get_average_fastball_velocity(pitcher_id, game_id)}

        first_name, last_name = get_player_name_by_id(pitcher_id)

        return {"individual_game_summary": summary,
                "name": f"{first_name} {last_name}"}

    @staticmethod
    def calculate_game_summary(pitches):
        count = 0
        pitch_list = []
        for pitch in pitches:
            pitches_thrown = int(pitch["count"])
            count += pitches_thrown

        for pitch in pitches:
            pitch_type = pitch["pitchtype"]
            pitch_list.append({'pitchType': pitch_type,
                               'count': int(pitch["count"]),
                               "percentage": 100 * int(pitch["count"]) / count if count > 0 else 0,
                               })
        return pitch_list, count


