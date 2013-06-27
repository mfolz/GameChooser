import sys
import csv
from pandas import *
import datetime
import glob
		
def main():

	for filename in glob.glob("*.csv"):
		file = open(filename)
	
		df = DataFrame.from_csv(file)
	
		col_len = len(df['is_home'])
	
		df['home_team']=""
		for i in range(col_len):
			if df['is_home'][i]==1:
				df['home_team'][i]=df['team'][i]
			elif df['is_home'][i]==0:
				df['home_team'][i]=df['opponent'][i]	

		df['away_team']=""
		for i in range(col_len):
			if df['is_home'][i]==0:
				df['away_team'][i]=df['team'][i]
			elif df['is_home'][i]==1:
				df['away_team'][i]=df['opponent'][i]
				
		df['game_number']=0
		for i in range(col_len):
			df['game_number'][i]=i+1
	
		df['points']=0
		df['points'][0]=df['own_score'][0]
		for i in range(1,col_len):
			df['points'][i]=df['points'][i-1]+df['own_score'][i]
	
		df['ppg']=0.0
		for i in range(1,col_len):
			df['ppg'][i]=1.0*df['points'][i-1]/df['game_number'][i-1]

		df['opp_points']=0
		df['opp_points'][0]=df['opponent_score'][0]
		for i in range(1,col_len):
			df['opp_points'][i]=df['opp_points'][i-1]+df['opponent_score'][i]

		df['opp_ppg']=0.0
		for i in range(1,col_len):
			df['opp_ppg'][i]=1.0*df['opp_points'][i-1]/df['game_number'][i-1]

		df['home_games']=0
		df['home_games'][0]=df['is_home'][0]
		for i in range(1,col_len):
			df['home_games'][i]=df['home_games'][i-1]+df['is_home'][i]
	
		df['home_points']=0
		cur_val = 0
		for i in range(0,col_len):
			cur_val += df['is_home'][i]*df['own_score'][i]
			df['home_points'][i]=cur_val
		
		df['home_ppg']=0.0
		for i in range(1,col_len):
			if df['home_games'][i-1]!=0:
				df['home_ppg'][i]=1.0*df['home_points'][i-1]/df['home_games'][i-1]
			
		df['home_opp_points']=0
		cur_val = 0
		for i in range(0,col_len):
			cur_val += df['is_home'][i]*df['opponent_score'][i]
			df['home_opp_points'][i]=cur_val
	
		df['home_opp_ppg']=0.0
		for i in range(1,col_len):
			if df['home_games'][i-1]!=0:
				df['home_opp_ppg'][i]=1.0*df['home_opp_points'][i-1]/df['home_games'][i-1]
	
		df['away_games']=0
		df['away_games'][0]=(1-df['is_home'][0])
		for i in range(1,col_len):
			df['away_games'][i]=df['away_games'][i-1]+(1-df['is_home'][i])
	
		df['away_points']=0
		cur_val = 0
		for i in range(0,col_len):
			cur_val += (1-df['is_home'][i])*df['own_score'][i]
			df['away_points'][i]=cur_val
	
		df['away_ppg']=0.0
		for i in range(1,col_len):
			if df['away_games'][i-1]!=0:
				df['away_ppg'][i]=1.0*df['away_points'][i-1]/df['away_games'][i-1]
	
		df['away_opp_points']=0
		cur_val = 0
		for i in range(0,col_len):
			cur_val += (1-df['is_home'][i])*df['opponent_score'][i]
			df['away_opp_points'][i]=cur_val	
	
		df['away_opp_ppg']=0.0
		for i in range(1,col_len):
			if df['away_games'][i-1]!=0:
				df['away_opp_ppg'][i]=1.0*df['away_opp_points'][i-1]/df['away_games'][i-1]

		df['num_wins']=0
		df['num_wins'][0] = df['win_outright'][0]
		for i in range(1,col_len):
			df['num_wins'][i] = df['num_wins'][i-1]+df['win_outright'][i]

		df['won_last']=0
		df['won_last'][0]=1
		for i in range(1,col_len):
			df['won_last'][i]=df['win_outright'][i-1]

		df['wins_L5']=0
		for i in range(col_len):
			if df['game_number'][i]>=5:
				df['wins_L5'][i]=df['num_wins'][i]-df['num_wins'][i-5]
	
		df['wins_L10']=0
		for i in range(col_len):
			if df['game_number'][i]>=10:
				df['wins_L10'][i]=df['num_wins'][i]-df['num_wins'][i-10]
	
		df['win_%']=0.0
		for i in range(1,col_len):
			df['win_%'][i] = 1.0*df['num_wins'][i-1]/df['game_number'][i-1]

		df['win_%_L5']=0.0
		for i in range(1,col_len):
			df['win_%_L5'][i]=1.0*df['wins_L5'][i-1]/5
	
		df['win_%_L10']=0.0
		for i in range(1,col_len):
			df['win_%_L10'][i]=1.0*df['wins_L10'][i-1]/10
	
		df['num_home_wins']=0
		df['num_home_wins'][0]=df['win_outright'][0]*df['is_home'][0]
		for i in range(1,col_len):
			df['num_home_wins'][i]=df['num_home_wins'][i-1]+df['win_outright'][i]*df['is_home'][i]
	
		df['home_win_%']=0.0
		for i in range(1,col_len):
			if df['home_games'][i-1]!=0:
				df['home_win_%'][i]=1.0*df['num_home_wins'][i-1]/df['home_games'][i-1]
			
	
		df['num_away_wins']=df['num_wins']-df['num_home_wins']
	
		df['away_win_%']=0.0
		for i in range(1,col_len):
			if df['away_games'][i-1]!=0:
				df['away_win_%'][i]=1.0*df['num_away_wins'][i-1]/df['away_games'][i-1]
	
		df['is_b2b']=0
		for i in range(1,col_len):
			diff = df.index[i]-df.index[i-1]
			if diff.days==1:
				df['is_b2b'][i]=1
			
		df['home_win']=0
		for i in range(col_len):
			if df['is_home'][i]+df['win_outright'][i]==2 or df['is_home'][i]+df['win_outright'][i]==0:
				df['home_win'][i]=1
	
		df['home_pts']=0
		for i in range(col_len):
			if df['is_home'][i]==1:
				df['home_pts'][i]=df['own_score'][i]
			elif df['is_home'][i]==0:
				df['home_pts'][i]=df['opponent_score'][i]
	
		df['away_pts']=df['total_score']-df['home_pts']
	
		df['point_diff'] = df['home_pts']-df['away_pts']

		df['record']='0-0'
		for i in range(1,col_len):
			df['record'][i]=str(df['num_wins'][i-1])+"-"+str(df['game_number'][i-1]-df['num_wins'][i-1])

	# should also do points L5/L10, points against L5/L10, etc...

		labels = (['home_team','away_team','is_b2b','ppg','opp_ppg','home_ppg','away_ppg',
					'home_opp_ppg','away_opp_ppg','win_%','home_win_%','away_win_%',
					'won_last','win_%_L5','win_%_L10','home_win','point_diff','home_pts',
					'away_pts','spread_size','over_under','is_home','record'])
				
		df_final = df[labels]
	
		df_final.to_csv(filename)
	

# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
  main()
