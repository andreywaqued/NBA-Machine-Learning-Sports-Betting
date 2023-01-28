import requests
from bs4 import BeautifulSoup

url = "https://www.pinnacle.com/en/basketball/nba/matchups#period:0"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

games = soup.find_all('span', {'class': 'ellipsis event-row-participant style_participant__H8-ku'})
print(games)
for game in games:
    teams = game.find('div', {'class': 'team-names'}).text.strip().split('\n')
    home_team = teams[0]
    away_team = teams[1]
    odds = game.find('div', {'class': 'odds'}).text.strip()
    print(f'{home_team} vs {away_team} - Odds: {odds}')
