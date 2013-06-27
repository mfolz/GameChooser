import sys
import csv
from pandas import *
		
def main():

	labels=(['date','home_team','away_team','home_b2b','away_b2b',
				'home_win_%', 'home_home_win_%', 'home_win_%_L10','home_win_%_L5',
				'home_won_last','home_ppg','home_opp_ppg','home_home_ppg','home_home_opp_ppg',
				'away_win_%','away_away_win_%','away_win_%_L10','away_win_%_L5',
				'away_won_last','away_ppg','away_opp_ppg','away_away_ppg','away_away_opp_ppg',
				'home_is_winner','point_diff','home_pts','away_pts',
				'spread_size','over_under','home_record','away_record'])
	
	#date,home_team,away_team,is_b2b,ppg,home_ppg,away_ppg,home_opp_ppg,away_opp_ppg,win_%,(9)
	#home_win_%,away_win_%,won_last,win_%_L5,win_%_L10,home_win,point_diff,home_pts,away_pts

				
	len_labels = len(labels)

	f = open('output_file.csv')
	
	list_of_lines = [[s.strip() for s in line[:-1].split(',')] for line in f.readlines()]
	final = [labels]
	
	for i in range(1,len(list_of_lines),2):
		game=[0]*len_labels
		home_ind = i
		away_ind = i+1
		if float(list_of_lines[i][-2])<0.5: #if line i corresponds to away team instead
			home_ind = i+1
			away_ind = i			
		
		game[0]=list_of_lines[home_ind][0] #date
		game[1]=list_of_lines[home_ind][1] #home_team
		game[2]=list_of_lines[home_ind][2] #away_team
		game[3]=list_of_lines[home_ind][3] #home_b2b
		game[4]=list_of_lines[away_ind][3] #away_b2b
		game[5]=list_of_lines[home_ind][10] #home_win_%
		game[6]=list_of_lines[home_ind][11] #home_home_win_%
		game[7]=list_of_lines[home_ind][15] #home_win_%_L10
		game[8]=list_of_lines[home_ind][14] #home_win_%_L5
		game[9]=list_of_lines[home_ind][13] #home_won_last
		game[10]=list_of_lines[home_ind][4] #home_ppg
		game[11]=list_of_lines[home_ind][5] #home_opp_ppg
		game[12]=list_of_lines[home_ind][6] #home_home_ppg
		game[13]=list_of_lines[home_ind][8] #home_home_opp_ppg
		game[14]=list_of_lines[away_ind][10] #away_win_%
		game[15]=list_of_lines[away_ind][12] #away_away_win_%
		game[16]=list_of_lines[away_ind][15] #away_win_%_L10
		game[17]=list_of_lines[away_ind][14] #away_win_%_L5
		game[18]=list_of_lines[away_ind][13] #away_won_last
		game[19]=list_of_lines[away_ind][4] #away_ppg
		game[20]=list_of_lines[away_ind][5] #away_opp_ppg
		game[21]=list_of_lines[away_ind][7] #away_away_ppg
		game[22]=list_of_lines[away_ind][9] #away_away_opp_ppg
		game[23]=list_of_lines[home_ind][-8] #home_is_winner
		game[24]=list_of_lines[home_ind][-7] #point_diff
		game[25]=list_of_lines[home_ind][-6] #home_pts
		game[26]=list_of_lines[home_ind][-5] #away_pts
		game[27]=list_of_lines[home_ind][-4] #spread_size
		game[28]=list_of_lines[home_ind][-3] #over_under
		game[29]=list_of_lines[home_ind][-1] #home_record
		game[30]=list_of_lines[away_ind][-1] #away_record	
		final.append(game)
		
	output_file = csv.writer(open('final.csv','wb'))
	output_file.writerows(final)

# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
  main()
