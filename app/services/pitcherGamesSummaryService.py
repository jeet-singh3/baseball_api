import logging
import sys
from app.utils.constants import MAX_SCHERZER
from app.utils.db_utils import (
    get_games,
    get_pitch_types_by_games,
    get_average_fastball_velocity,
    get_player_name_by_id,
    get_game_info
)

LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
LOG.addHandler(handler)


class PitcherGamesSummaryService:
    @classmethod
    def handle_request(cls, request):
        pitcher_id = cls.validate_args(request)
        pitcher_games = get_games(pitcher_id)
        player_pitch_types_by_game = get_pitch_types_by_games(pitcher_games, pitcher_id)
        game_summary_list = []
        for game in player_pitch_types_by_game:
            game_summary, pitch_count = cls.calculate_game_summary(player_pitch_types_by_game[game])
            home_team, away_team, game_date = get_game_info(game)
            game_summary_list.append({"gameId": game,
                                      "summary": game_summary,
                                      "pitchCount": pitch_count,
                                      "homeTeam": home_team,
                                      "awayTeam": away_team,
                                      "gameDate": game_date.strftime('%Y-%m-%d'),
                                      "averageFastballVelocity": get_average_fastball_velocity(pitcher_id, game)})

        first_name, last_name = get_player_name_by_id(pitcher_id)

        return {"games_summary": game_summary_list,
                "name": f"{first_name} {last_name}"}

    @staticmethod
    def validate_args(request):
        if 'pitcherId' not in request.args:
            raise Exception('pitcherId is required to get pitcher game summary')
        pitcher_id = request.args.get('pitcherId')
        if not pitcher_id:
            return MAX_SCHERZER
        return pitcher_id

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


