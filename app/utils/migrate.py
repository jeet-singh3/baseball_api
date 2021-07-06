import os
import logging
import sys
from postgres import Postgres
import csv

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
    LOG.info("Executed command: created table users=")
    db.run(
        "create unique index if not exists users_ux_01 on users(name)"
    )
    LOG.info("Executed command: created unique index on users(name)")
    db.run(
        "insert into users (name, logins) select 'random_person', 5 on conflict do nothing"
    )
    LOG.info("Executed command: inserted started value into users table")
    db.run(
        "create table if not exists players(player_id numeric, name_use varchar(1024), name_last varchar(1024))"
    )
    LOG.info("Executed command: created table players")
    db.run(
        "create unique index if not exists players_ux_01 on players(player_id)"
    )
    LOG.info("Executed command: create unique index on players(player_id)")
    db.run(
        "create index if not exists players_ix_01 on players(name_use)"
    )
    LOG.info("Executed command: create index on players(name_use)")
    db.run(
        "create index if not exists players_ix_02 on players(name_last)"
    )
    LOG.info("Executed command: create index on players(name_last)")
    LOG.info("Checking if players are there")
    num_players = db.one("select count(*) from players")
    if num_players == 87292:
        LOG.info("Skipping player.py insert as players are already there.")
    else:
        open_file = open('/app/app/utils/players.csv', 'r')
        csv_file = csv.reader(open_file)
        _ = next(csv_file)
        sql_stmt = "insert into players (player_id, name_use, name_last) select %(player_id)s, %(name_use)s, " \
                   "%(name_last)s on conflict (player_id) do update set name_use = %(name_use)s, " \
                   "name_last = %(name_last)s"
        for row in csv_file:
            db.run(sql_stmt, {
                "player_id": row[0],
                "name_use": row[1],
                "name_last": row[2]
            })
        open_file.close()
        LOG.info("Executed command: Inputting players")

    db.run(
        "create table if not exists pitches(game_pk numeric, game_date date, home_team_id numeric, "
        "away_team_id numeric, home_team_name varchar(1024), home_team_abbrev varchar(1024), "
        "away_team_name varchar(1024), away_team_abbrev varchar(1024), venue_id numeric, venue_name varchar(1024), "
        "PitchUID varchar(1024), PitcherId numeric, PitcherThrows varchar(1024), BatterId numeric, "
        "BatterSide varchar(1024), PitchNo numeric, Inning numeric, Top_Bottom varchar(1024), Outs numeric, "
        "Balls numeric,Strikes numeric, PitchType varchar(1024), PitchTypeAbbrev varchar(1024), "
        "PitchCall varchar(1024), KorBB varchar(1024), HitType varchar(1024), PlayResult varchar(1024), "
        "RelSpeed varchar(1024), SpinRate varchar(1024), SpinAxis varchar(1024), Tilt varchar(1024), "
        "HorzBreak varchar(1024), InducedVertBreak varchar(1024), PlateLocHeight varchar(1024), "
        "PlateLocSide varchar(1024), HitExitSpeed varchar(1024), HitLaunchAngle varchar(1024), "
        "HitLaunchDirection varchar(1024), HitLandingDistance varchar(1024), HitLandingAngle varchar(1024), "
        "HitHangTime varchar(1024), video_url varchar(1024))"
    )
    LOG.info("Executed command: created table pitches")
    db.run(
        "create index if not exists pitches_ix_01 on pitches(PitcherId)"
    )
    LOG.info("Executed command: created index on pitches(PitcherId)")
    db.run(
        "create index if not exists pitches_ix_02 on pitches(game_pk, PitcherId)"
    )
    LOG.info("Executed command: created index on pitches(game_pk, PitcherId)")
    db.run(
        "create index if not exists pitches_ix_03 on pitches(game_date)"
    )
    LOG.info("Executed command: created index on pitches(game_date)")
    num_pitches = db.one("select count(*) from pitches")
    if num_pitches == 349178:
        LOG.info("Skipping pitches insert as pitches are already there.")
    else:
        open_file = open('/app/app/utils/mlb_2021_pitches.csv', 'r')
        csv_file = csv.reader(open_file)
        _ = next(csv_file)
        sql_stmt = "INSERT INTO public.pitches (game_pk, game_date, home_team_id, away_team_id, home_team_name, " \
                   "home_team_abbrev, away_team_name, away_team_abbrev, venue_id, venue_name, pitchuid, pitcherid, " \
                   "pitcherthrows, batterid, batterside, pitchno, inning, top_bottom, outs, balls, strikes, pitchtype, " \
                   "pitchtypeabbrev, pitchcall, korbb, hittype, playresult, relspeed, spinrate, spinaxis, tilt, " \
                   "horzbreak, inducedvertbreak, platelocheight, platelocside, hitexitspeed, hitlaunchangle, " \
                   "hitlaunchdirection, hitlandingdistance, hitlandingangle, hithangtime, video_url) select %(game_pk)s, " \
                   "%(game_date)s, %(home_team_id)s, %(away_team_id)s, %(home_team_name)s, %(home_team_abbrev)s, " \
                   "%(away_team_name)s, %(away_team_abbrev)s, %(venue_id)s, %(venue_name)s, %(pitchuid)s, %(pitcherid)s, " \
                   "%(pitcherthrows)s, %(batterid)s, %(batterside)s, %(pitchno)s, %(inning)s, %(top_bottom)s, %(outs)s, " \
                   "%(balls)s, %(strikes)s, %(pitchtype)s, %(pitchtypeabbrev)s, %(pitchcall)s, %(korbb)s, %(hittype)s, " \
                   "%(playresult)s, %(relspeed)s, %(spinrate)s, %(spinaxis)s, %(tilt)s, %(horzbreak)s, " \
                   "%(inducedvertbreak)s, %(platelocheight)s, %(platelocside)s, %(hitexitspeed)s, %(hitlaunchangle)s, " \
                   "%(hitlaunchdirection)s, %(hitlandingdistance)s, %(hitlandingangle)s, %(hithangtime)s, %(video_url)s " \
                   "on conflict do nothing"
        for row in csv_file:
            db.run(sql_stmt, {
                "game_pk": row[0],
                "game_date": row[1],
                "home_team_id": row[2],
                "away_team_id": row[3],
                "home_team_name": row[4],
                "home_team_abbrev": row[5],
                "away_team_name": row[6],
                "away_team_abbrev": row[7],
                "venue_id": row[8],
                "venue_name": row[9],
                "pitchuid": row[10],
                "pitcherid": row[11],
                "pitcherthrows": row[12],
                "batterid": row[13],
                "batterside": row[14],
                "pitchno": row[15],
                "inning": row[16],
                "top_bottom": row[17],
                "outs": row[18],
                "balls": row[19],
                "strikes": row[20],
                "pitchtype": row[21],
                "pitchtypeabbrev": row[22],
                "pitchcall": row[23],
                "korbb": row[24],
                "hittype": row[25],
                "playresult": row[26],
                "relspeed": row[27],
                "spinrate": row[28],
                "spinaxis": row[29],
                "tilt": row[30],
                "horzbreak": row[31],
                "inducedvertbreak": row[32],
                "platelocheight": row[33],
                "platelocside": row[34],
                "hitexitspeed": row[35],
                "hitlaunchangle": row[36],
                "hitlaunchdirection": row[37],
                "hitlandingdistance": row[38],
                "hitlandingangle": row[39],
                "hithangtime": row[40],
                "video_url": row[41]
            })
        open_file.close()
        LOG.info("Executed command: inserted pitches")
    LOG.info("Up and ready!")


initial_table_creation()
