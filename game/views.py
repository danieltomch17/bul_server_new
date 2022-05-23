from ctypes import sizeof
from datetime import date
from hashlib import blake2b
import json
import random
from sqlite3 import Date
import numpy
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from enum import Enum
import time
import functools
from django.db.models import Q

from rest_framework.decorators import api_view

from cards.models import Card
from game.models import Game 
from leagues.models import League, LeagueEntry
from game.serializers import GameSerializer
from teams.models import Team

"""
TODO:
- 4 quarters, 2min each
- 3 zones of the court
- what positions does sam have and who starts the attack
- right now all players are equal (position is not a consideration)
"""

"""
court areas :
 _______________________
|      |        |       |
|      |        |       |
|  1   |    2   |   3   |
|      |        |       |
|______|________|_______|

Home team starts in area 1
Away team starts in area 3

"""

# Create your views here.

class team(Enum):
    HOME = 0
    AWAY = 1
    TIE = 2


class court_area(Enum):
    ONE = 1
    TWO = 2
    THREE = 3

class moves(Enum):
    PASS_SAME_AREA = 1
    PASS_NEXT_AREA = 2
    GO_TO_NEXT_AREA = 3
    SCORE = 4
    MISS = 5
    TURNOVER = 6

class miss_outcome(Enum):
    REBOUND = 1
    TURNOVER = 2
    OUT = 3

#### GLOBALS ####
cards = None
scores = None
possession = None
current_area = None
player_with_ball = None
rest_of_cards = None
events_log = None
def_stats = None
att_stats = None
def_bonuses = None
att_bonuses = None

# game logic constants (in percents)
c_home_advantage = 1.1

# the length of a quarter in seconds
quarter_time_sec = 3#60
qurter_delay = 0.3#3
attack_delay = 0.033#0.5
move_delay = 0.015#0.2

@api_view(['GET'])
def get_game_history(request):
    uid = request.user.id
    team = Team.objects.filter(user_id__id = uid)
    game_history_queryset = Game.objects.filter(team_a__team_id=team.first().team_id) | Game.objects.filter(team_b__team_id=team.first().team_id)
    game_history = list(game_history_queryset.order_by('-date','-time'))
    game_serializer = GameSerializer(game_history, many=True)

    return JsonResponse(game_serializer.data, status=200, safe=False)


@api_view(['GET'])
def get_logs(request, from_id):

    if from_id > len(events_log):
        return HttpResponse(status=204)

    res = events_log[from_id:-1]

    return JsonResponse(res, status=200, safe=False)

"""
def start_game(home_team, away_team):
"""
@api_view(['GET'])
def start_game(request, home_id, away_id): # for now team numbers are hard coded
    global cards, scores, possession, events_log, def_stats, att_stats, def_bonuses, att_bonuses

    events_log = []

    home_team_id = home_id # Temporary until
    away_team_id = away_id # we get team id from DB

    #get teams
    home_team = Team.objects.filter(team_id=home_team_id).first()
    away_team = Team.objects.filter(team_id=away_team_id).first()

    # get cards
    home_team_cards = list(Card.objects.filter(team_id__team_id=home_team_id).filter(is_first_five=True))
    away_team_cards = list(Card.objects.filter(team_id__team_id=away_team_id).filter(is_first_five=True))

    cards = [home_team_cards, away_team_cards]
    
    """ initialize statistics """
    # home team stats
    home_team_def_score = get_team_def_score(home_team_cards) * c_home_advantage
    home_team_att_score = get_team_att_score(home_team_cards) * c_home_advantage

    # away team stats
    away_team_def_score = get_team_def_score(away_team_cards)
    away_team_att_score = get_team_att_score(away_team_cards)

    # global stats
    def_stats = [home_team_def_score, away_team_def_score]
    att_stats = [home_team_att_score, away_team_att_score]

    home_def_bonus = calculate_bonus(home_team_def_score, away_team_def_score)
    home_att_bonus = calculate_bonus(home_team_att_score, away_team_att_score)
    
    away_def_bonus = calculate_bonus(away_team_def_score, home_team_def_score)
    away_att_bonus = calculate_bonus(away_team_att_score, home_team_att_score)

    # global bonuses
    def_bonuses = [home_def_bonus, home_att_bonus]
    att_bonuses = [away_def_bonus, away_att_bonus]

    print("def stats : ", end='')
    print(def_stats)
    print("att stats : ", end='')
    print(att_stats)
    print("def bonuses : ", end='')
    print(def_bonuses)
    print("att bonuses : ", end='')
    print(att_bonuses)

    # initialize scores
    scores = [0, 0]

    print("starting game : team {} vs team {}".format(home_team_id, away_team_id))
    log_event("starting game : team 2 vs team 5")

    # run 4 quarters
    for i in range(4) :
        print("quarter {} is starting !".format(i+1))
        log_event("quarter {} is starting !".format(i+1))
        possession = team.HOME if i%2 == 0 else team.AWAY
        start_quarter(i)
        time.sleep(qurter_delay)

    print("game over")
    log_event("game over")
    print("final score is {}".format(scores))
    log_event("final score is {}".format(scores))

    # save game to DB
    Game.objects.create(team_a=home_team, team_b=away_team, results="{} : {}".format(scores[team.HOME.value], scores[team.AWAY.value]))

    winner = team.TIE

    # update league entries
    if scores[team.HOME.value] > scores[team.AWAY.value]:
        winner = team.HOME
    elif scores[team.HOME.value] < scores[team.AWAY.value]:
        winner = team.AWAY

    update_league_entries(home_team, away_team, winner)

    return JsonResponse(events_log, status=200, safe=False)


def update_league_entries(home_team, away_team, winner):
    home_entry_queryset = LeagueEntry.objects.filter(team=home_team).filter(is_active=True)
    away_entry_queryset = LeagueEntry.objects.filter(team=away_team).filter(is_active=True)

    home_entry = home_entry_queryset.first()
    away_entry = away_entry_queryset.first()

    if winner == team.HOME:
        home_entry_queryset.update(wins=home_entry.wins+1)
        away_entry_queryset.update(losses=away_entry.losses+1)
    elif winner == team.AWAY:
        home_entry_queryset.update(losses=home_entry.losses+1)
        away_entry_queryset.update(wins=away_entry.wins+1)
    elif winner == team.TIE:
        home_entry_queryset.update(ties=home_entry.ties+1)
        away_entry_queryset.update(ties=away_entry.ties+1)

# add more statistic considerations here
def get_team_def_score(cards) :
    all_stats = [card.blocks_for for card in cards]
    res = functools.reduce(lambda a, b: a+ b, all_stats) / len(all_stats)

    return res

# add more statistic considerations here
def get_team_att_score(cards) :
    all_stats = [card.p21 for card in cards]
    res = functools.reduce(lambda a, b: a + b, all_stats) / len(all_stats)

    return res

"""
returns a bonus for teamA based on the differences
between the statistics (a value between 0 and 0.5)
which is then added to the odds of that team in certain
random decisions
we want team A's bonus + team B's bonus to be 0.5
hence :
mul = teamA_score / teamB_score
teamA_Bouns + teamB_Bonus = 0.5 |=> teamA_Bonus = 0.5 * mul / (mul+1)
teamA_Bonus = mul * teamB_bonus |=> teamB_Bonus = 0.5 / (mul + 1)
"""
def calculate_bonus(teamA_score, teamB_score):
    mul = teamA_score/teamB_score
    res = (0.5 * (mul / (mul+1)))

    return res


def start_quarter(q_num):
    start_time = time.perf_counter()
    while(time.perf_counter() - start_time < quarter_time_sec) :
        time.sleep(attack_delay)
        start_attack()

    print("quarter {} ended\n".format(q_num + 1))
    log_event("quarter {} ended".format(q_num + 1))

def start_attack():
    global cards, rest_of_cards, possession, player_with_ball, current_area

    # get a random player to start the attack
    player_starting_attack = random.choice(cards[possession.value])
    rest_of_cards = [card for card in cards[possession.value] if card.id != player_starting_attack.id]

    current_area = court_area.ONE

    # pass the ball to start the attack
    pass_to(random.choice(rest_of_cards))

    print("{} starts an attack with a pass to {}".format(player_starting_attack.player_name, player_with_ball.player_name))
    log_event("{} starts an attack with a pass to {}".format(player_starting_attack.player_name, player_with_ball.player_name))
    time.sleep(move_delay)

    end_attack = False

    while not end_attack: # ass some sort of timeout
        end_attack = next_move()
        time.sleep(move_delay)

    print("\n")


def next_move():
    global player_with_ball, rest_of_cards, current_area, possession, scores, def_stats, att_stats, def_bonuses, att_bonuses

    reb_prob = 0.3 + def_bonuses[possession.value]

    # choose move
    if current_area == court_area.ONE or current_area == court_area.TWO :
        move = numpy.random.choice([moves.PASS_SAME_AREA, moves.PASS_NEXT_AREA, moves.GO_TO_NEXT_AREA, moves.TURNOVER], p=[0.2,0.3,0.3,0.2])

    elif current_area == court_area.THREE :
        score_prob = None
        if player_with_ball.p22 == 0:
            score_prob = 0.4
        else:
            score_prob = 0.2 + player_with_ball.p21 / player_with_ball.p22 # should be a number between 0 and 1 representing the success rate of the current player to score
            if score_prob > 0.4 : score_prob = 0.4

        print("p21 is : " + str(player_with_ball.p21))
        print("p22 is : " + str(player_with_ball.p22))
        print("score_prob is : " + str(score_prob))
        move = numpy.random.choice([moves.PASS_SAME_AREA, moves.SCORE, moves.MISS], p=[0.2, score_prob, 0.8 - score_prob])
    

    # act according to chosen move
    if move == moves.PASS_SAME_AREA :
        tmp_player = player_with_ball
        pass_to(random.choice(rest_of_cards))
        print("{} passes the ball to {}. the ball stays in area {}".format(tmp_player, player_with_ball.player_name, current_area.name))
        log_event("{} passes the ball to {}. the ball stays in area {}".format(tmp_player, player_with_ball.player_name, current_area.name))

    elif move == moves.PASS_NEXT_AREA :
        tmp_player = player_with_ball
        pass_to(random.choice(rest_of_cards))
        go_to_next_area()
        print("{} passes the ball to {}, moving the ball to area  {}".format(tmp_player, player_with_ball.player_name, current_area.name))
        log_event("{} passes the ball to {}, moving the ball to area  {}".format(tmp_player, player_with_ball.player_name, current_area.name))

    elif move == moves.GO_TO_NEXT_AREA :
        go_to_next_area()
        print("{} is moving forward to area {}".format(player_with_ball.player_name, current_area.name))
        log_event("{} is moving forward to area {}".format(player_with_ball.player_name, current_area.name))

    elif move == moves.TURNOVER :
        possession = team((possession.value + 1) % 2)
        player_with_ball = random.choice(cards[possession.value])
        rest_of_cards = [card for card in cards[possession.value] if card.id != player_with_ball.id]
        current_area = court_area(4 - current_area.value)
        print("{} takes the ball, starting a counter attack !".format(player_with_ball.player_name))
        log_event("{} take the ball, starting a counter attack !".format(player_with_ball.player_name))

    elif move == moves.MISS :
        print("{} shoots and misses".format(player_with_ball.player_name))
        log_event("{} shoots and misses".format(player_with_ball.player_name))
        outcome = numpy.random.choice([miss_outcome.OUT, miss_outcome.REBOUND, miss_outcome.TURNOVER], p=[0.2, reb_prob, 0.8 - reb_prob])

        if outcome is miss_outcome.OUT :
            possession = team((possession.value + 1) % 2)
            print("and it's out of the court ..")
            log_event("and it's out of the court ..")
            return True

        elif outcome is miss_outcome.REBOUND :
            pass_to(random.choice(rest_of_cards))
            print("{} takes the rebound !".format(player_with_ball.player_name))
            log_event("{} takes the rebound !".format(player_with_ball.player_name))

        elif outcome is miss_outcome.TURNOVER :
            possession = team((possession.value + 1) % 2)
            player_with_ball = random.choice(cards[possession.value])
            rest_of_cards = [card for card in cards[possession.value] if card.id != player_with_ball.id]
            current_area = court_area.ONE
            print("{} take the rebound, starting a counter attack !".format(player_with_ball.player_name))
            log_event("{} take the rebound, starting a counter attack !".format(player_with_ball.player_name))

    elif move == moves.SCORE :
        print("{} shoots and scores !!".format(player_with_ball.player_name))
        log_event("{} shoots and scores !!".format(player_with_ball.player_name))
        scores[possession.value] += 2
        print("score is : {}".format(scores))
        log_event("score is : {}".format(scores))
        possession = team((possession.value + 1) % 2)
        return True

    return False

def pass_to(player):
    global player_with_ball, rest_of_cards, possession

    player_with_ball = player
    rest_of_cards = [card for card in cards[possession.value] if card.id != player.id]

def go_to_next_area():
    global current_area

    current_area = court_area(current_area.value + 1)

def log_event(event):
    global events_log

    events_log.append({len(events_log):event})