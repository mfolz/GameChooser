'''
output.py
Author: Matthew Folz
Project: GameChooser

This file takes in a list of .csv files containing the statistics for each NBA team at a 
given date, and outputs (for each file) another .csv file containing all pairs of games
(one home, one away) between the two teams.
'''

import sys
import csv
import datetime
import glob

def create_game(t1,t2): #create game with t1 as home team, t2 as away team
	
	'''
		labels=(['date','home_team','away_team','home_b2b','away_b2b',
				'home_win_%', 'home_home_win_%', 'home_win_%_L10','home_win_%_L5',
				'home_won_last','home_ppg','home_opp_ppg','home_home_ppg','home_home_opp_ppg',
				'away_win_%','away_away_win_%','away_win_%_L10','away_win_%_L5',
				'away_won_last','away_ppg','away_opp_ppg','away_away_ppg','away_away_opp_ppg',
				'home_is_winner','point_diff','home_pts','away_pts',
				'spread_size','over_under','home_record','away_record'])
	'''
	
	#initialize game
	game=[0]*31
	
	#populate
	game[0]=t1[0] #date
	game[1]=t1[1] #home_team
	game[2]=t2[1] #away_team
	game[3]=t1[3] #home_b2b
	game[4]=t2[3] #away_b2b
	game[5]=t1[10] #home_win_%
	game[6]=t1[11] #home_home_win_%
	game[7]=t1[15] #home_win_%_L10
	game[8]=t1[14] #home_win_%_L5
	game[9]=t1[13] #home_won_last
	game[10]=t1[4] #home_ppg
	game[11]=t1[5] #home_opp_ppg
	game[12]=t1[6] #home_home_ppg
	game[13]=t1[8] #home_home_opp_ppg
	game[14]=t2[10] #away_win_%
	game[15]=t2[12] #away_away_win_%
	game[16]=t2[15] #away_win_%_L10
	game[17]=t2[14] #away_win_%_L5
	game[18]=t2[13] #away_won_last
	game[19]=t2[4] #away_ppg
	game[20]=t2[5] #away_opp_ppg
	game[21]=t2[7] #away_away_ppg
	game[22]=t2[9] #away_away_opp_ppg
	game[23]=t1[-8] #home_is_winner
	game[24]=t1[-7] #point_diff
	game[25]=t1[-6] #home_pts
	game[26]=t1[-5] #away_pts
	game[27]=t1[-4] #spread_size
	game[28]=t1[-3] #over_under
	game[29]=t1[-1] #home_record
	game[30]=t2[-1] #away_record		
	
	return game
			
def main():
	
	#list of files containing team statistics on a given date
	filenames = (['20121231.csv','20130107.csv','20130114.csv','20130121.csv',
					'20130128.csv','20130204.csv','20130211.csv','20130225.csv',
					'20130304.csv','20130311.csv','20130318.csv','20130325.csv',
					'20130401.csv','20130408.csv','20130415.csv'])
	
	#create all pairs of games
	for name in filenames:
	
		#read and format game string from .csv into a list
		f = open(name,'r')	
		lines = [[s.strip() for s in line[:-1].split(',')] for line in f.readlines()]
	
		gamelist = []
		for t1 in lines:
			for t2 in lines:
				if t1!=t2 and t1<t2:	
					#one home game, one away game			
					g1 = create_game(t1,t2)
					g2 = create_game(t2,t1)
					gamelist.append(g1)
					gamelist.append(g2)
	
		new_filename = name[:-4]+'-allgames.csv'
	
		#output each file to a new csv
		output_file = csv.writer(open(new_filename,'wb'))
		output_file.writerows(gamelist)
				
				

# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
  main()
