import os
import logging
import sys
from postgres import Postgres
from app.models.player import PlayerModel
from app.models.aggregate_pitch import AggregatePitchModel

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


def generate_sql_for_searching_games(game_date, home_team, away_team):
    sql_stmt = "select distinct game_pk, home_team_abbrev, away_team_abbrev from pitches where "
    if not game_date and not home_team and not away_team:
        sql_stmt += "game_date = '2021-05-01'"
    else:
        counter = 0
        vals = [game_date, home_team, away_team]
        for idx, val in enumerate(vals):
            if val:
                counter += 1
                sql_stmt += "and " if counter > 1 and not sql_stmt.endswith("and ") else ""
                if idx == 0:
                    sql_stmt += "game_date = %(gameDate)s "
                if idx == 1:
                    sql_stmt += "home_team_abbrev = %(homeTeam)s "
                if idx == 2:
                    sql_stmt += "away_team_abbrev = %(awayTeam)s "
    LOG.info(f"Generated sql statement: {sql_stmt}")
    return sql_stmt


def search_games(game_date, home_team, away_team):
    sql_stmt = generate_sql_for_searching_games(game_date, home_team, away_team)
    values = PG_DB.all(sql_stmt, {
        "gameDate": game_date,
        "homeTeam": home_team,
        "awayTeam": away_team
    })
    games_array = []
    for value in values:
        games_array.append({"gameId": int(value[0]),
                            "homeTeam": value[1],
                            "awayTeam": value[2]})
    return games_array


def generate_sql_for_search(name_use, name_last):
    sql_stmt = "select player_id, name_use, name_last from players where "
    if name_use and name_last:
        sql_stmt += "name_use = %(name_use)s and name_last = %(name_last)s"
    elif name_use:
        sql_stmt += "name_use = %(name_use)s"
    elif name_last:
        sql_stmt += "name_last = %(name_last)s"
    else:
        raise Exception("firstName or lastName is needed in order to search for players")
    return sql_stmt


def get_players(name_use, name_last):
    sql_stmt = generate_sql_for_search(name_use, name_last)
    players = PG_DB.all(sql_stmt, {
        "name_use": name_use,
        "name_last": name_last
    })
    players_list = []
    for player in players:
        player_guy = PlayerModel(playerId=player[0], nameUse=player[1], nameLast=player[2])
        player_guy_dict = player_guy.to_dict()
        players_list.append(player_guy_dict)

    LOG.info(f"Retrieved players with first name: {name_use} and last name: {name_last}")
    return players_list


def get_pitches(pitcher_id):
    sql_stmt = 'select pitchtype, count(*) from pitches where pitcherId = %(pitcher_id)s group by pitchtype'
    pitches = PG_DB.all(sql_stmt, {
        "pitcher_id": pitcher_id
    })
    LOG.info(f"Retrieved all pitch types for pitcher {pitcher_id}")
    pitch_list = []
    for pitch in pitches:
        ah_pitch = AggregatePitchModel(pitchtype=pitch[0], count=int(pitch[1]))
        ah_pitch_dict = ah_pitch.to_dict()
        pitch_list.append(ah_pitch_dict)
    return pitch_list


def get_games(pitcher_id):
    sql_stmt = 'select distinct game_pk from pitches where pitcherId = %(pitcher_id)s'
    games_array = []
    games = PG_DB.all(sql_stmt, {
        "pitcher_id": pitcher_id
    })
    for game in games:
        games_array.append(int(game))
    LOG.info(f"Retrieved all games for pitcher {pitcher_id}")
    return games_array


def get_pitchers_for_game(game_id):
    sql_stmt = 'select distinct pitcherid from pitches where game_pk = %(gameId)s'
    pitchers_array = []
    pitchers = PG_DB.all(sql_stmt, {
        "gameId": game_id
    })
    for pitcher in pitchers:
        pitchers_array.append(int(pitcher))
    LOG.info(f"Retrieved all pitchers for game {game_id}")
    return pitchers_array


def get_pitch_types_by_game_id(pitcher_game, pitcher_id):
    sql_stmt = 'select pitchtype, count(*) from pitches where pitcherId = %(pitcher_id)s ' \
               'and game_pk = %(game)s group by pitchtype'
    pitch_types = PG_DB.all(sql_stmt, {
        "pitcher_id": pitcher_id,
        "game": pitcher_game
    })
    pitch_list = []
    for pitch in pitch_types:
        ah_pitch = AggregatePitchModel(pitchtype=pitch[0], count=int(pitch[1]))
        ah_pitch_dict = ah_pitch.to_dict()
        pitch_list.append(ah_pitch_dict)
    return pitch_list


def get_pitch_types_by_games(pitcher_games, pitcher_id):
    pitch_types_games_dict = {}
    for game in pitcher_games:
        pitch_types_games_dict[game] = get_pitch_types_by_game_id(game, pitcher_id)
        LOG.info(f"Retrieved all pitch types for pitcher {pitcher_id} in game {game}")
    return pitch_types_games_dict


def get_average_fastball_velocity(pitcher_id, game_id):
    sql_stmt = "select relspeed from pitches where pitcherid = %(pitcherId)s and game_pk = %(gameId)s and " \
               "(pitchtype = 'Fastball' or pitchtype = 'Sinker')"
    values = PG_DB.all(sql_stmt, {
        "pitcherId": pitcher_id,
        "gameId": game_id
    })
    fastball_speed = 0
    count_fastball = len(values)
    for value in values:
        fastball_speed += float(value)
    return fastball_speed / count_fastball if count_fastball > 0 else 0


def get_player_name_by_id(player_id):
    sql_stmt = "select name_use, name_last from players where player_id = %(playerId)s"
    value = PG_DB.one(sql_stmt, {
        "playerId": player_id,
    })
    return value[0], value[1]


def get_average_values_for_summary(pitcher_id, pitch_type):
    sql_stmt = "select relspeed, horzbreak, inducedvertbreak, spinrate, hitexitspeed, hitlaunchangle" \
               " from pitches where pitcherid = %(pitcherId)s and pitchtype = %(pitchtype)s"
    values = PG_DB.all(sql_stmt, {
        "pitcherId": pitcher_id,
        "pitchtype": pitch_type
    })
    LOG.info(f"Retrieved all {pitch_type} pitches for pitcher {pitcher_id}")
    number_rel_speed = 0
    number_horizontal_break = 0
    number_vertical_break = 0
    number_spin_rate = 0
    number_hit_exit_speed = 0
    number_hit_launch_angle = 0
    rel_speed = 0
    horizontal_break = 0
    vertical_break = 0
    spin_rate = 0
    hit_exit_speed = 0
    hit_launch_angle = 0
    for value in values:
        if value[0] != 'NA':
            rel_speed += float(value[0])
            number_rel_speed += 1
        if value[1] != 'NA':
            horizontal_break += float(value[1])
            number_horizontal_break += 1
        if value[2] != 'NA':
            vertical_break += float(value[2])
            number_vertical_break += 1
        if value[3] != 'NA':
            spin_rate += float(value[3])
            number_spin_rate += 1
        if value[4] != 'NA':
            hit_exit_speed += float(value[4])
            number_hit_exit_speed += 1
        if value[5] != 'NA':
            hit_launch_angle += float(value[5])
            number_hit_launch_angle += 1

    return [rel_speed / number_rel_speed, horizontal_break / number_horizontal_break,
            vertical_break / number_vertical_break, spin_rate / number_spin_rate,
            hit_exit_speed / number_hit_exit_speed, hit_launch_angle / number_hit_launch_angle]

