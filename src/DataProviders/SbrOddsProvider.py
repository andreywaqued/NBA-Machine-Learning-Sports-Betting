from sbrscrape import Scoreboard

class SbrOddsProvider:
    
    """ Abbreviations dictionary for team location which are sometimes saved with abbrev instead of full name. 
    Moneyline options name require always full name
    Returns:
        string: Full location name
    """    

    def __init__(self, sportsbook="fanduel"):
        
       self.games = Scoreboard(sport="NBA").games
       self.sportsbook = sportsbook
       print(self.games)

    
    def get_odds(self):
        """Function returning odds from Sbr server's json content

        Returns:
            dictionary: [home_team_name + ':' + away_team_name: { home_team: money_line_odds, away_team: money_line_odds }, under_over_odds: {val, under_odds, over_odds}]
        """
        dict_res = {}
        for game in self.games:
            # Get team names
            home_team_name = game['home_team'].replace("Los Angeles Clippers", "LA Clippers")
            away_team_name = game['away_team'].replace("Los Angeles Clippers", "LA Clippers")
            
            money_line_home_value = money_line_away_value = totals_value = under_odds = over_odds = None

            # Get money line bet values
            if self.sportsbook in game['home_ml']:
                money_line_home_value = game['home_ml'][self.sportsbook]
            if self.sportsbook in game['away_ml']:
                money_line_away_value = game['away_ml'][self.sportsbook]
            
            # Get totals bet value
            if self.sportsbook in game['total']:
                totals_value = game['total'][self.sportsbook]

            # Get under/over bet value
            if self.sportsbook in game['under_odds']:
                under_odds = game['under_odds'][self.sportsbook]
            if self.sportsbook in game['over_odds']:
                over_odds = game['over_odds'][self.sportsbook]

            
            dict_res[home_team_name + ':' + away_team_name] =  { 
                'under_over_odds': { 'total':totals_value, 'under':under_odds, 'over':over_odds },
                home_team_name: { 'money_line_odds': money_line_home_value }, 
                away_team_name: { 'money_line_odds': money_line_away_value }
            }
        return dict_res