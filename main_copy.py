from sbrscrape import Scoreboard

def averageValues(values):
    return sum(values)/len(values)

def conversor_odds(oddsAmericanas):
	oddsDecimal = 0
	if oddsAmericanas > 0:
		oddsDecimal = (oddsAmericanas / 100) + 1
	elif oddsAmericanas < 0:
		oddsDecimal = (-100 / oddsAmericanas) + 1
	return round(oddsDecimal, 2)


class SbrOddsProvider:
    
	""" Abbreviations dictionary for team location which are sometimes saved with abbrev instead of full name. 
	Moneyline options name require always full name
	Returns:
		string: Full location name
	"""    

	def __init__(self, sport, sportsbook=""):	
		self.games = Scoreboard(sport).games
		self.sportsbook = sportsbook
		#print(self.games)
		for game in self.games:
			total = 1/conversor_odds(averageValues(game["home_ml"].values())) + 1/conversor_odds(averageValues(game["away_ml"].values()))
			homeWin = 1/conversor_odds(averageValues(game["home_ml"].values()))/total
			awayWin = 1/conversor_odds(averageValues(game["away_ml"].values()))/total
			totalUO = 1/conversor_odds(averageValues(game["under_odds"].values())) + 1/conversor_odds(averageValues(game["over_odds"].values()))
			underWin = 1/conversor_odds(averageValues(game["under_odds"].values()))/totalUO
			overWin = 1/conversor_odds(averageValues(game["over_odds"].values()))/totalUO
			# print("home_ml: (O.A.: " + str(averageValues(game["home_ml"].values())) + ") (O.D.: " + str(conversor_odds(averageValues(game["home_ml"].values()))) + ") WIN% :" + str(homeWin))
			# print("away_ml: (O.A.: " + str(averageValues(game["away_ml"].values())) + ") (O.D.: " + str(conversor_odds(averageValues(game["away_ml"].values()))) + ") WIN% :" + str(awayWin))
			# print("total: " + str(averageValues(game["total"].values())))
			# print("under_odds: (O.A.: " + str(averageValues(game["under_odds"].values())) + ") (O.D.: " + str(conversor_odds(averageValues(game["under_odds"].values()))) + ") WIN% :" + str(underWin))
			# print("over_odds: (O.A.: " + str(averageValues(game["over_odds"].values())) + ") (O.D.: " + str(conversor_odds(averageValues(game["over_odds"].values()))) + ") WIN% :" + str(overWin))
			print(game["home_team"] + " (WIN% " + str(round(homeWin, 2)) + ") (BEOdds " + str(round(1/homeWin,2)) + ") X " + game["away_team"] + " (WIN% " + str(round(awayWin,2)) + ") (BEOdds " + str(round(1/awayWin, 2)) + ")")
			print("under " + str(round(averageValues(game["total"].values()), 2)) + " (WIN% " + str(round(underWin, 2)) + ") (BEOdds " + str(round(1/underWin,2)) + " / over " + str(round(averageValues(game["total"].values()), 2)) + " (WIN% " + str(round(overWin,2)) + ") (BEOdds " + str(round(1/overWin, 2)) + ")")
			for provider, oa in game["home_ml"].items():
				if conversor_odds(oa) * homeWin > 1:
					print(provider + " home_ml : (O.A. " + str(oa) + ") (O.D. " + str(conversor_odds(oa)) + ") WIN%: " + str(round(homeWin, 2)) + " EV: " + str(round((conversor_odds(oa) * homeWin - 1) * 100, 2)) + "%")
			for provider, oa in game["away_ml"].items():
				if conversor_odds(oa) * awayWin > 1:
					print(provider + " away_ml : (O.A. " + str(oa) + ") (O.D. " + str(conversor_odds(oa)) + ") WIN%: " + str(round(awayWin, 2)) + " EV: " + str(round((conversor_odds(oa) * awayWin - 1) * 100, 2)) + "%")
			for provider, oa in game["under_odds"].items():
				if conversor_odds(oa) * underWin > 1:
					print(provider + " under " + str(round(game["total"][provider], 2)) + ": (O.A. " + str(oa) + ") (O.D. " + str(conversor_odds(oa)) + ") WIN%: " + str(round(underWin, 2)) + " EV: " + str(round((conversor_odds(oa) * underWin - 1) * 100, 2)) + "%")
			for provider, oa in game["over_odds"].items():
				if conversor_odds(oa) * overWin > 1:
					print(provider + " over " + str(round(game["total"][provider], 2)) + ": (O.A. " + str(oa) + ") (O.D. " + str(conversor_odds(oa)) + ") WIN%: " + str(round(overWin, 2)) + " EV: " + str(round((conversor_odds(oa) * overWin - 1) * 100, 2)) + "%")
			print()
		
oddsProvider = SbrOddsProvider(sport="NHL")