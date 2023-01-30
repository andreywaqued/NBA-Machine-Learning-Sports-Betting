import requests
import xlsxwriter
import pandas as pd
import numpy as np
import openpyxl
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Border, Side, Font, Alignment, PatternFill, numbers

class odds_api_provider:
	def __init__(self, sport='basketball_nba', regions='eu', markets='h2h,totals', odds_format='decimal', date_format='iso'):
		API_KEY = 'b44c22cbc286679ea1ff4759ec62497e'
		SPORT = sport #'basketball_nba' # use the sport_key from the /sports endpoint below, or use 'upcoming' to see the next 8 games across all sports

		REGIONS = regions #'eu' # uk | us | eu | au. Multiple can be specified if comma delimited

		MARKETS = markets #'h2h,totals' # h2h | spreads | totals. Multiple can be specified if comma delimited

		ODDS_FORMAT = odds_format #'decimal' # decimal | american

		DATE_FORMAT = date_format #'iso' # iso | unix

		BET_SIZE = 10

		self.odds_response = requests.get(
			f'https://api.the-odds-api.com/v4/sports/{SPORT}/odds',
			params={
				'api_key': 'b44c22cbc286679ea1ff4759ec62497e',
				'regions': REGIONS,
				'markets': MARKETS,
				'oddsFormat': ODDS_FORMAT,
				'dateFormat': DATE_FORMAT,
			}
		).json()
	def get_odds(self):
		# odds_response
		#print(odds_response)
		#dictionary: [home_team_name + ':' + away_team_name: { home_team: money_line_odds, away_team: money_line_odds }, under_over_odds: {val, under_odds, over_odds}]
		oddsDict = {}
		for game in self.odds_response:
			#print(game["bookmakers"])
			for bookmaker in game["bookmakers"]:
				if bookmaker["key"] == "pinnacle":
					for markets in bookmaker["markets"]:
						if markets["outcomes"][0]["name"] == "Over":
							oddsDict[homeTeam + ":" + awayTeam].update({"under_over_odds" : {"total":markets["outcomes"][0]["point"], "under":markets["outcomes"][0]["price"], "over":markets["outcomes"][1]["price"]}})
							continue
						else:
							homeTeam = markets["outcomes"][0]["name"]
							awayTeam = markets["outcomes"][1]["name"]
							oddsDict[homeTeam + ":" + awayTeam] = {homeTeam : markets["outcomes"][0]["price"], awayTeam : markets["outcomes"][1]["price"]} #, "under_over_odds" : {"total" : total, "under": under_odds, "over": over_odds} 
						#print(oddsDict)
		print(oddsDict)
					# for odds in markets["outcomes"]:
					#     print(odds)

#odds_api_provider().get_odds()
