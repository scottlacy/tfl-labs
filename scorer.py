import json
import requests

game = '2013091513'
url = 'http://www.nfl.com/liveupdate/game-center/%s/%s_gtd.json' % (game,game)


### CONSTANTS ###
RUSHING_THRESHOLD = 25
RECEIVING_THRESHOLD = 25
PASSING_THRESHOLD = 75
TOUCHDOWN_VALUE = 6
FIELD_GOAL_VALUE = 3
SIX_POINT_DEFENSIVE_SCORES = ('interception return', 'fumble return', 'return of blocked punt', 'return of blocked field goal')

home_defense = 0
visitor_defense = 0

json_data = requests.get(url)

data = json_data.json()

home = data[game]['home']['abbr']
visitor = data[game]['away']['abbr']


# Step through scoring summary in search of defensive scoring plays
scoring_plays = data[game]['scrsummary']

for id in scoring_plays:
	desc = scoring_plays[id]['desc']
	print scoring_plays[id]['desc']
	if any (s in desc for s in SIX_POINT_DEFENSIVE_SCORES):
		if scoring_plays[id]['team'] == home:
			home_defense += 6
		else:
			visitor_defense += 6
	elif 'Safety' in desc:
		if scoring_plays[id]['team'] == home:
			home_defense += 2
		else:
			visitor_defense += 2

print '+++ ' + home + ' vs. ' + visitor + ' +++'

# Parse individual performances and convert NFL totals into TFL points
teams = ['home', 'away']

for team in teams:

	t = data[game][team]['stats']

	rushing = t['rushing']
	receiving = t['receiving']
	passing = t['passing']
	kicking = t['kicking']

	team_score = data[game][team]['score']['T']
	print team, team_score
	if team_score < 10:
		if team == 'home':
			visitor_defense += 3
		elif team == 'away':
			home_defense += 3
	elif team_score == 0:
		if team == 'home':
			visitor_defense += 6
		elif team == 'away':
			home_defense += 6
	
	print '********'
	print data[game][team]['abbr']
	print '********'
	
	print '\n/RUSHING/ \n'

	for id in rushing:
	    points = abs(rushing[id]['yds'] / RUSHING_THRESHOLD) + (rushing[id]['tds'] * TOUCHDOWN_VALUE)
	    print rushing[id]['name'], points

	print
	print '/PASSING/'
	print

	for id in passing:
	    points = abs(passing[id]['yds'] / PASSING_THRESHOLD) + (passing[id]['tds'] * TOUCHDOWN_VALUE)
	    print passing[id]['name'], points

	print
	print '/RECEIVING/'
	print

	for id in receiving:
	    points = abs(receiving[id]['yds'] / RECEIVING_THRESHOLD) + (receiving[id]['tds'] * TOUCHDOWN_VALUE)
	    print receiving[id]['name'], points

	print
	print '/KICKING/'
	print

	for id in kicking:
	    points = (kicking[id]['fgm'] * FIELD_GOAL_VALUE) + kicking[id]['xpmade']
	    print kicking[id]['name'], points

	print '\n'

	print

print '/DEFENSE/'
print home + ' defense: %d points' % (home_defense,)
print visitor + ' defense: %d points' % (visitor_defense,)
