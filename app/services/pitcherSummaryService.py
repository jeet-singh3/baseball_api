import logging
import sys
from app.utils.constants import MAX_SCHERZER
from app.utils.db_utils import get_pitches, get_average_values_for_summary, get_player_name_by_id

LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
LOG.addHandler(handler)


class PitcherSummaryService:
    @classmethod
    def handle_request(cls, request):
        pitcher_id = cls.validate_args(request)
        players_pitches = get_pitches(pitcher_id)
        summary_list = cls.calculate_summary(players_pitches, pitcher_id)
        first_name, last_name = get_player_name_by_id(pitcher_id)
        return {"pitches_summary": summary_list,
                "name": f"{first_name} {last_name}"}

    @staticmethod
    def validate_args(request):
        if 'pitcherId' not in request.args:
            raise Exception('pitcherId is required to get pitcher summary')
        pitcher_id = request.args.get('pitcherId')
        if not pitcher_id:
            return MAX_SCHERZER
        return pitcher_id

    @staticmethod
    def calculate_summary(pitches, pitcher):
        count = 0
        pitch_list = []
        for pitch in pitches:
            pitches_thrown = int(pitch["count"])
            count += pitches_thrown

        for pitch in pitches:
            pitch_type = pitch["pitchtype"]
            average_values = get_average_values_for_summary(pitcher, pitch_type)
            pitch_list.append({'pitchType': pitch_type,
                               'count': int(pitch["count"]),
                               "percentage": 100 * int(pitch["count"]) / count if count > 0 else 0,
                               "avgPitchSpeed": average_values[0],
                               "avgHorizontalMovement": average_values[1],
                               "avgVerticalMovement": average_values[2],
                               "avgSpinRate": average_values[3],
                               "avgHitSpeed": average_values[4],
                               "avgLaunchAngle": average_values[5]
                               })

        return pitch_list

