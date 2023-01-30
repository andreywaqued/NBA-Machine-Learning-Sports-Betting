from sbrscrape import Scoreboard


def averageTotal(values):
    return sum(values)/len(values)

def averageValues(values):
    totalOdds = 0
    for value in values:
        totalOdds += conversor_odds(value)
    return totalOdds/len(values)

def conversor_odds(oddsAmericanas):
	oddsDecimal = 0
	if oddsAmericanas > 0:
		oddsDecimal = (oddsAmericanas / 100) + 1
	elif oddsAmericanas < 0:
		oddsDecimal = (100 / abs(oddsAmericanas)) + 1
	return oddsDecimal


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
			total = 1/averageValues(game["home_ml"].values()) + 1/averageValues(game["away_ml"].values())
			homeWin = 1/averageValues(game["home_ml"].values())/total
			awayWin = 1/averageValues(game["away_ml"].values())/total
			totalUO = 1/averageValues(game["under_odds"].values()) + 1/averageValues(game["over_odds"].values())
			underWin = 1/averageValues(game["under_odds"].values())/totalUO
			overWin = 1/averageValues(game["over_odds"].values())/totalUO
			print(game["home_team"] + " (WIN% " + str(round(homeWin, 2)) + ") (BEOdds " + str(round(1/homeWin,2)) + ") X " + game["away_team"] + " (WIN% " + str(round(awayWin,2)) + ") (BEOdds " + str(round(1/awayWin, 2)) + ")")
			print("under " + str(round(averageTotal(game["total"].values()), 2)) + " (WIN% " + str(round(underWin, 2)) + ") (BEOdds " + str(round(1/underWin,2)) + " / over " + str(round(averageTotal(game["total"].values()), 2)) + " (WIN% " + str(round(overWin,2)) + ") (BEOdds " + str(round(1/overWin, 2)) + ")")
			# print("home_ml: (O.D.: " + str(averageValues(game["home_ml"].values())) + ") WIN% :" + str(homeWin))
			# print(game["home_ml"])
			# print("away_ml: (O.D.: " + str(averageValues(game["away_ml"].values())) + ") WIN% :" + str(awayWin))
			# print("total: " + str(averageValues(game["total"].values())))
			# print("under_odds: (O.D.: " + str(averageValues(game["under_odds"].values())) + ") WIN% :" + str(underWin))
			# print("over_odds: (O.D.: " + str(averageValues(game["over_odds"].values())) + ") WIN% :" + str(overWin))
			for provider, oa in game["home_ml"].items():
				if conversor_odds(oa) * homeWin > 1:
					print(provider + "* home_ml : (O.D. " + str(conversor_odds(oa)) + ") WIN%: " + str(round(homeWin, 2)) + " EV: " + str(round((conversor_odds(oa) * homeWin - 1) * 100, 2)) + "%")
			for provider, oa in game["away_ml"].items():
				if conversor_odds(oa) * awayWin > 1:
					print(provider + "* away_ml : (O.D. " + str(conversor_odds(oa)) + ") WIN%: " + str(round(awayWin, 2)) + " EV: " + str(round((conversor_odds(oa) * awayWin - 1) * 100, 2)) + "%")
			for provider, oa in game["under_odds"].items():
				if conversor_odds(oa) * underWin > 1:
					print(provider + "* under " + str(game["total"][provider], 2) + ": (O.D. " + str(round(conversor_odds(oa), 2)) + ") WIN%: " + str(round(underWin, 2)) + " EV: " + str(round((conversor_odds(oa) * underWin - 1) * 100, 2)) + "%")
			for provider, oa in game["over_odds"].items():
				if conversor_odds(oa) * overWin > 1:
					print(provider + "* over " + str(game["total"][provider], 2) + ": (O.D. " + str(round(conversor_odds(oa), 2)) + ") WIN%: " + str(round(overWin, 2)) + " EV: " + str(round((conversor_odds(oa) * overWin - 1) * 100, 2)) + "%")
			print()
		
oddsProvider = SbrOddsProvider(sport="NBA")