#!/usr/bin/env python

import os
from flask import Flask, url_for, render_template, session, request, redirect, jsonify
import MySQLdb
import datetime
import json

def team_dict():
	return ({ 'Hawks':'Atlanta','Celtics':'Boston','Bobcats':'Charlotte',
				'Bulls':'Chicago','Cavaliers':'Cleveland','Mavericks':'Dallas',
				'Nuggets':'Denver','Pistons':'Detroit','Warriors':'Golden State',
				'Rockets':'Houston','Pacers':'Indiana','Clippers':'L.A. Clippers',
				'Lakers':'L.A. Lakers','Grizzlies':'Memphis','Heat':'Miami',
				'Bucks':'Milwaukee','Timberwolves':'Minnesota','Nets':'Brooklyn',
				'Hornets':'New Orleans','Knicks':'New York','Thunder':'Oklahoma City',
				'Magic':'Orlando','Sixers':'Philadelphia','76ers':'Philadelphia',
				'Suns':'Phoenix','TrailBlazers':'Portland','Trailblazers':'Portland',
				'Kings':'Sacramento','Spurs':'San Antonio','Raptors':'Toronto',
				'Jazz':'Utah','Wizards':'Washington' })

def team_abbr():
	return ({ 'Atlanta':'ATL','Boston':'BOS','Charlotte':'CHA','Chicago':'CHI',
				'Cleveland':'CLE','Dallas':'DAL','Denver':'DEN','Detroit':'DET',
				'Golden State':'GSW','Houston':'HOU','Indiana':'IND',
				'L.A. Clippers':'LAC','L.A. Lakers':'LAL','Memphis':'MEM','Miami':'MIA',
				'Milwaukee':'MIL','Minnesota':'MIN','Brooklyn':'BKN','New Orleans':'NOH',
				'New York':'NYK','Orlando':'ORL','Oklahoma City':'OKC',
				'Philadelphia':'PHI','Phoenix':'PHX','Portland':'POR','Sacramento':'SAC',
				'San Antonio':'SAS','Toronto':'TOR','Utah':'UTA','Washington':'WAS' })

def watchability_rating(
						home_team,away_team,win_predict,prob_predict,
						spread_predict,homescore_predict,awayscore_predict,
						home_win_percent,away_win_percent,fav_teams,playing_today
						):

	#favorite team component
	fav_score = 0.0
	for i in fav_teams:
		if i == home_team or i == away_team:
			fav_score = 1.0
	fav_score_weight = 1.0
	a = set(fav_teams)
	b = set(playing_today)
	if len(a.intersection(b)) == 0:
		fav_score_weight = 0.0

	#projected closeness component			
	closeness_score = 1.0-abs(spread_predict)/10.0
	if closeness_score <= 0.0:
		closeness_score = 0.0
	closeness_score_weight = 1.0

	#team quality component, uses geometric means of records
	wl_score = ((home_win_percent*away_win_percent)**(0.5)-0.35)/(0.65-0.35) 
	if wl_score > 1.0:
		wl_score = 1.0
	if wl_score < 0.0:
		wl_score = 0.0
	wl_score_weight = 2.0

	#projected high score component	
	highscore_score = ((homescore_predict+awayscore_predict)-185)/(215-185)
	if highscore_score > 1.0:
		highscore_score = 1.0
	if highscore_score < 0.0:
		highscore_score = 0.0
	highscore_score_weight = 1.0
	
	total_weight = (fav_score_weight+closeness_score_weight
						+wl_score_weight+highscore_score_weight)
	
	watchability_rating = (fav_score_weight*fav_score+
							closeness_score_weight*closeness_score+
							wl_score_weight*wl_score+
							highscore_score_weight*highscore_score)/total_weight
	#bumps up scores
	norm_watchability_rating = min(1.0, watchability_rating/0.8)

	#return both normalized and unnormalized, using watchability_rating to break ties	
	return norm_watchability_rating, watchability_rating

app = Flask(__name__)
app.secret_key = os.urandom(2**20)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/contact/')
def contact():
    return render_template('contact.html')

@app.route('/results/', methods=['POST'])
def results():
	session['date'] = request.form['user_date']
	session['teams'] = request.form['user_teams']    	
	return render_template('results.html')

@app.route('/view/')
def view(): 	
	return render_template('view.html')

@app.route('/predict/')
def predict():    
	return render_template('predict.html')

@app.route('/table/')
def table():

	date =  session['date']
	str_teams = session['teams']

	#parse and store team input
	location_name_dict = team_dict()

	fav_teams = []	
	if str_teams != "":
		str_teams = str_teams.replace(" ","")
		fav_teams =  str_teams.split(",")
		teams = []
		for i in fav_teams:
			try:
				val = location_name_dict[i]
				teams.append(val)
			except KeyError:
				pass				
		fav_teams = teams

	#parse dates
	formatted_date = datetime.datetime.strptime(session['date'],'%Y-%m-%d')
	final_date = formatted_date.strftime('%B %e, %Y')
	date_for_url = formatted_date.strftime('%Y%m%d')

	con = MySQLdb.connect(host='localhost', user='root', passwd='', db='2013_data')
	cur = con.cursor()
	cur.execute("""SELECT home_team,away_team,win_predict,prob_predict,spread_predict,
					homescore_predict_noOT,awayscore_predict_noOT,home_win_percent,
					away_win_percent,home_record,away_record,spread_size,over_under,
					total_predict_noOT,tipoff_time FROM season_data WHERE game_date='"""
					+date+"';")
					
	all_games = cur.fetchall()

	game_list = []

	playing_today = []
	for game in all_games:
		playing_today.append(game[0])
		playing_today.append(game[1])

	abbr_dict = team_abbr()

	if len(all_games) == 0:
		#print error message (there were no NBA games tonight)
		True
	else:
		for game in all_games:
			game_dict = {}
			game_dict['home_team'] = game[0]
			game_dict['away_team'] = game[1]
			game_dict['home_team_abbr'] = abbr_dict[game[0]]
			game_dict['away_team_abbr'] = abbr_dict[game[1]]			
			game_dict['win_predict'] = game[2]
			game_dict['prob_predict'] = game[3]
			game_dict['spread_predict'] = -1.0*game[4]
			game_dict['homescore_predict_round'] = round(game[5])
			game_dict['awayscore_predict_round'] = round(game[6])
			game_dict['homescore_predict'] = game[5]
			game_dict['awayscore_predict'] = game[6]
			game_dict['total_predict'] = game[13]
			game_dict['tipoff_time'] = game[14]
			
			if round(game[5]) == round(game[6]):
				if game[5] > game[6]:
					game_dict['homescore_predict_round'] = round(game[5])+1
				else:
					game_dict['awayscore_predict_round'] = round(game[6])+1
			
			nwr,wr = watchability_rating(game[0], game[1], game[2],
											game[3], game[4], game[5], game[6],
											game[7], game[8], fav_teams,playing_today)
			game_dict['norm_watchability_rating'] = round(100*nwr)
			game_dict['watchability_rating']=round(100*wr)
			
			game_dict['home_WL'] = game[7]
			game_dict['away_WL'] = game[8]
			game_dict['home_record'] = game[9]
			game_dict['away_record'] = game[10]
			game_dict['spread_size'] = game[11]
			game_dict['over_under'] = game[12]
			
			game_list.append(game_dict)

	game_list = sorted(game_list,
						key = lambda x:(x['watchability_rating'], game[7]+game[8]),
						reverse = True)
						
	#convert list of dicts to ordered dict of dicts 					
	final_dict = {i:game_list[i] for i in range(len(game_list))} 

	#pass date, game information in JSON
	final_dict['date'] = final_date
	final_dict['date_url'] = date_for_url
		
	if playing_today == []:
		final_dict['empty'] = 1
	else:
		final_dict['empty'] = 0

	return jsonify(final_dict)

@app.route('/teamrank/')
def teamrank():
	return render_template('teamrank.html')

@app.route('/teamdata/')
def teamdata():

	date =  session['date']

	week_starts = (["2012-12-31","2013-01-07","2013-01-14","2013-01-21","2013-01-28",
					"2013-02-04","2013-02-11","2013-02-25","2013-03-04","2013-03-11",
					"2013-03-18","2013-03-25","2013-04-01","2013-04-08","2013-04-15",
					"2013-04-18"])
	
	for i in range(len(week_starts)-1):
		if date >= week_starts[i] and date < week_starts[i+1]:
			str_date = week_starts[i]
			start_date = datetime.datetime.strptime(week_starts[i], '%Y-%m-%d')
			display_start_date = start_date.strftime('%B %e, %Y')
			end_date = (datetime.datetime.strptime(week_starts[i+1], '%Y-%m-%d')
							-datetime.timedelta(days = 1))
			display_end_date = end_date.strftime('%B %e, %Y')
			
	
	con = MySQLdb.connect(host='localhost', user='root', passwd='', db='2013_data')
	cur = con.cursor()
	cur.execute("""SELECT team,record,L10,predict_point_diff,predict_record FROM powerrank 
					WHERE game_date='"""+str_date+"';")	

	all_games = cur.fetchall()

	game_list = []
	
	for game in all_games:
		game_dict = {}
		game_dict['team'] = game[0]
		game_dict['record'] = game[1]
		game_dict['L10'] = game[2]
		game_dict['predict_point_diff'] = game[3]
		game_dict['predict_record'] = game[4]

		game_list.append(game_dict)
		
	game_list = sorted(game_list,
						key = lambda x:x['predict_point_diff'],
						reverse = True)	

	#convert list of dicts to ordered dict of dicts 					
	final_dict = {i:game_list[i] for i in range(len(game_list))} 

	#pass dates in JSON
	final_dict['start_date'] = display_start_date
	final_dict['end_date'] = display_end_date
	
	return jsonify(final_dict)
	
if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 80)
