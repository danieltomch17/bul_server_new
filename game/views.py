from ctypes import sizeof
from hashlib import blake2b
import json
import random
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from enum import Enum
import time

from rest_framework.decorators import api_view

from cards.models import Card

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

class miss_outcome(Enum):
    REBOUND = 1
    TURNOVER = 2
    OUT = 3

#### GLOBALS ####
home_team_cards = None
away_team_cards = None
cards = None
scores = None
possession = None
current_area = None
player_with_ball = None
rest_of_cards = None
events_log = None

# the length of a quarter in seconds
quarter_time_sec = 120
qurter_delay = 3
attack_delay = 1
move_delay = 0.5

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
def start_game(request): # for now team numbers are hard coded
    global home_team_cards, away_team_cards, cards, scores, possession, events_log

    events_log = []

    home_team_id = 2 # Temporary until
    away_team_id = 5 # we get team id from DB

    home_team_cards = list(Card.objects.filter(team_id__team_id=home_team_id).filter(is_first_five=True))
    away_team_cards = list(Card.objects.filter(team_id__team_id=away_team_id).filter(is_first_five=True))
    cards = [home_team_cards, away_team_cards]

    scores = [0, 0]


    print("starting game : team 2 vs team 5")
    log_event("starting game : team 2 vs team 5")

    # run 4 quarters
    for i in range(1) :
        print("quarter {} is starting !".format(i+1))
        log_event("quarter {} is starting !".format(i+1))
        possession = team.HOME if i%2 == 0 else team.AWAY
        start_quarter(i)
        time.sleep(qurter_delay)

    print("game over")
    log_event("game over")
    print("final score is {}".format(scores))
    log_event("final score is {}".format(scores))

    #json_res = json.dump(events_log)
    return JsonResponse(events_log, status=200, safe=False)


def start_quarter(q_num):
    start_time = time.perf_counter()
    while(time.perf_counter() - start_time < 7) : # temporary 7 seconds for testing purposes
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
    global player_with_ball, rest_of_cards, current_area, possession, scores

    if current_area == court_area.ONE or current_area == court_area.TWO :
        move = random.choice([moves.PASS_SAME_AREA, moves.PASS_NEXT_AREA, moves.GO_TO_NEXT_AREA])

    elif current_area == court_area.THREE :
        move = random.choice([moves.PASS_SAME_AREA, moves.SCORE, moves.MISS])
    

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

    elif move == moves.MISS :
        print("{} shoots and misses".format(player_with_ball.player_name))
        log_event("{} shoots and misses".format(player_with_ball.player_name))
        outcome = random.choice([miss_outcome.OUT, miss_outcome.REBOUND, miss_outcome.TURNOVER])

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