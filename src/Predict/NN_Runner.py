import copy
import numpy as np
import pandas as pd
import tensorflow as tf
from colorama import Fore, Style, init, deinit
from tensorflow.keras.models import load_model
from src.Utils import Expected_Value

init()
model = load_model('Models/NN_Models/Trained-Model-ML')
ou_model = load_model("Models/NN_Models/Trained-Model-OU")

def conversor_odds(oddsAmericanas):
  oddsDecimal = 0
  if oddsAmericanas > 0:
    oddsDecimal = (oddsAmericanas / 100) + 1
  elif oddsAmericanas < 0:
    oddsDecimal = (-100 / oddsAmericanas) + 1
  return round(oddsDecimal, 2)

def nn_runner(data, todays_games_uo, frame_ml, games, home_team_odds, away_team_odds, under_odds, over_odds):
    ml_predictions_array = []

    for row in data:
        ml_predictions_array.append(model.predict(np.array([row])))

    frame_uo = copy.deepcopy(frame_ml)
    limit = False
    #modificar aqui para adicionar/remover total score para calcular as odds de limite do bet365
    # limit = True
    # for i in range(len(todays_games_uo)):
    #   if todays_games_uo[i] != None:
    #       todays_games_uo[i] += 8
    frame_uo['OU'] = np.asarray(todays_games_uo)
    data = frame_uo.values
    data = data.astype(float)
    data = tf.keras.utils.normalize(data, axis=1)

    ou_predictions_array = []

    for row in data:
        ou_predictions_array.append(ou_model.predict(np.array([row])))

    count = 0
    for game in games:
        home_team = game[0]
        away_team = game[1]
        winner = int(np.argmax(ml_predictions_array[count]))
        under_over = int(np.argmax(ou_predictions_array[count]))
        winner_confidence = ml_predictions_array[count]
        un_confidence = ou_predictions_array[count]
        if winner == 1:
            winner_confidence = round(winner_confidence[0][1] * 100, 1)
            if under_over == 0:
                un_confidence = round(ou_predictions_array[count][0][0] * 100, 1)
                print(Fore.GREEN + home_team + Style.RESET_ALL + Fore.CYAN + f" ({winner_confidence}%)" + Style.RESET_ALL + ' vs ' + Fore.RED + away_team + Style.RESET_ALL + ': ' +
                      Fore.MAGENTA + 'UNDER ' + Style.RESET_ALL + str(todays_games_uo[count]) + Style.RESET_ALL + Fore.CYAN + f" ({un_confidence}%)" + Style.RESET_ALL)
            else:
                un_confidence = round(ou_predictions_array[count][0][1] * 100, 1)
                print(Fore.GREEN + home_team + Style.RESET_ALL + Fore.CYAN + f" ({winner_confidence}%)" + Style.RESET_ALL + ' vs ' + Fore.RED + away_team + Style.RESET_ALL + ': ' +
                      Fore.BLUE + 'OVER ' + Style.RESET_ALL + str(todays_games_uo[count]) + Style.RESET_ALL + Fore.CYAN + f" ({un_confidence}%)" + Style.RESET_ALL)
        else:
            winner_confidence = round(winner_confidence[0][0] * 100, 1)
            if under_over == 0:
                un_confidence = round(ou_predictions_array[count][0][0] * 100, 1)
                print(Fore.RED + home_team + Style.RESET_ALL + ' vs ' + Fore.GREEN + away_team + Style.RESET_ALL + Fore.CYAN + f" ({winner_confidence}%)" + Style.RESET_ALL + ': ' +
                      Fore.MAGENTA + 'UNDER ' + Style.RESET_ALL + str(todays_games_uo[count]) + Style.RESET_ALL + Fore.CYAN + f" ({un_confidence}%)" + Style.RESET_ALL)
            else:
                un_confidence = round(ou_predictions_array[count][0][1] * 100, 1)
                print(Fore.RED + home_team + Style.RESET_ALL + ' vs ' + Fore.GREEN + away_team + Style.RESET_ALL + Fore.CYAN + f" ({winner_confidence}%)" + Style.RESET_ALL + ': ' +
                      Fore.BLUE + 'OVER ' + Style.RESET_ALL + str(todays_games_uo[count]) + Style.RESET_ALL + Fore.CYAN + f" ({un_confidence}%)" + Style.RESET_ALL)
        count += 1

    print("--------------------Expected Value---------------------")
    count = 0
    for game in games:
        home_team = game[0]
        away_team = game[1]
        under_over = int(np.argmax(ou_predictions_array[count]))
        if under_over == 0:
          uo_string = "Under " + str(todays_games_uo[count])
          uo_odds = under_odds[count]
        else:
          uo_string = "Over " + str(todays_games_uo[count])
          uo_odds = over_odds[count]
        if limit:
          uo_odds = -233
        ev_home = ev_away = ev_uo = 0
        if home_team_odds[count] and away_team_odds[count] and todays_games_uo[count]:
          ev_home = float(Expected_Value.expected_value(ml_predictions_array[count][0][1], int(home_team_odds[count])))
          ev_away = float(Expected_Value.expected_value(ml_predictions_array[count][0][0], int(away_team_odds[count])))
          ev_uo = float(Expected_Value.expected_value(ou_predictions_array[count][0][under_over], int(uo_odds)))
        if ev_home > 0:
            print(Fore.GREEN + home_team + '(O.A. ' + str(home_team_odds[count]) + ') (O.D. ' + str(conversor_odds(home_team_odds[count]))  + ') Win%: ' + str(round(ml_predictions_array[count][0][1]*100, 2)) + ': EV: ' + Fore.GREEN + str(ev_home) + Style.RESET_ALL)
        else:
            print(Fore.RED + home_team + '(O.A. ' + str(home_team_odds[count]) + ') (O.D. ' + str(conversor_odds(home_team_odds[count])) + ') Win%: ' + str(round(ml_predictions_array[count][0][1]*100, 2)) + ': EV: ' + Fore.RED + str(ev_home) + Style.RESET_ALL)

        if ev_away > 0:
            print(Fore.GREEN + away_team + '(O.A. ' + str(away_team_odds[count]) + ') (O.D. ' + str(conversor_odds(away_team_odds[count])) + ') Win%: ' + str(round(ml_predictions_array[count][0][0]*100, 2)) + ': EV: ' + Fore.GREEN + str(ev_away) + Style.RESET_ALL)
        else:
            print(Fore.RED + away_team + '(O.A. ' + str(away_team_odds[count]) + ') (O.D. ' + str(conversor_odds(away_team_odds[count])) + ') Win%: ' + str(round(ml_predictions_array[count][0][0]*100, 2)) + ': EV: ' + Fore.RED + str(ev_away) + Style.RESET_ALL)
            
        if ev_uo > 0:
            print(Fore.GREEN + uo_string + '(O.A. ' + str(uo_odds) + ') (O.D. ' + str(conversor_odds(uo_odds)) + ') Win%: ' + str(round(ou_predictions_array[count][0][under_over]*100, 2)) + ': EV: ' + str(ev_uo) + Style.RESET_ALL)
        else:
            print(Fore.RED + uo_string + '(O.A. ' + str(uo_odds) + ') (O.D. ' + str(conversor_odds(uo_odds)) + ') Win%: ' + str(round(ou_predictions_array[count][0][under_over]*100, 2)) + ': EV: ' + Fore.RED + str(ev_uo) + Style.RESET_ALL)
        print("------------------------------------------------------")
        count += 1

    deinit()
