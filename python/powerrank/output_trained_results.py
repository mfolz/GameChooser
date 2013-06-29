'''
output_trained_results.py
Author: Matthew Folz
Project: GameChooser

This file takes in the .csv files output by the script output.py, which consist of all
simulated games between pairs of NBA teams on a given date, and outputs a single .csv
file containing the projected results of these games.  It is a modified version of the 
script ../main/output_trained_results.py

This is done via a machine learning model trained on 4000+ NBA games from before 
January 1, 2013.

We use random forest classifiers to predict winners and win probabilities, and
support vector regression to predict point spreads and points scored by each team.
'''

import sys
import csv
from pandas import *
from datetime import *
import numpy
from numpy import reshape
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm
from sklearn import preprocessing

#list of filenames to load
def filenames():
	return (['20121231-allgames.csv','20130107-allgames.csv','20130114-allgames.csv',
				'20130121-allgames.csv','20130128-allgames.csv','20130204-allgames.csv',
				'20130211-allgames.csv','20130225-allgames.csv','20130304-allgames.csv',
				'20130311-allgames.csv','20130318-allgames.csv','20130325-allgames.csv',
				'20130401-allgames.csv','20130408-allgames.csv','20130415-allgames.csv'])

#list of games
def list_of_teams():
	return (['Atlanta','Boston','Charlotte','Chicago','Cleveland','Dallas','Denver',
				'Detroit','Golden State','Houston','Indiana','L.A. Clippers',
				'L.A. Lakers','Memphis','Miami','Milwaukee','Minnesota','Brooklyn',
				'New Orleans','New York','Orlando','Oklahoma City','Philadelphia',
				'Phoenix','Portland','Sacramento','San Antonio','Toronto','Utah',
				'Washington'])

#load each simulated dataset into a numpy array
def csv_to_numpy(filename):

	df = DataFrame.from_csv(open(filename,'r'))
	test_set = df[df.columns[2:22]]
	
	return preprocessing.scale(numpy.array(test_set))

#load training set
def arrange_data():

	df = DataFrame.from_csv(open('final.csv'))

	#load all games before January 1, 2013 (training set).		
	X0_list = ([df[df.columns[2:22]][datetime(2006,12,15):datetime(2007,4,8)],
					df[df.columns[2:22]][datetime(2007,12,15):datetime(2008,4,8)],
					df[df.columns[2:22]][datetime(2008,12,15):datetime(2009,4,8)],
					df[df.columns[2:22]][datetime(2009,12,15):datetime(2010,4,8)],
					df[df.columns[2:22]][datetime(2010,12,15):datetime(2011,4,8)],
					df[df.columns[2:22]][datetime(2012,12,15):datetime(2013,1,1)]])
	
	Y0_list = ([df[df.columns[22:28]][datetime(2006,12,15):datetime(2007,4,8)],
					df[df.columns[22:28]][datetime(2007,12,15):datetime(2008,4,8)],
					df[df.columns[22:28]][datetime(2008,12,15):datetime(2009,4,8)],
					df[df.columns[22:28]][datetime(2009,12,15):datetime(2010,4,8)],
					df[df.columns[22:28]][datetime(2010,12,15):datetime(2011,4,8)],
					df[df.columns[22:28]][datetime(2012,12,15):datetime(2013,1,1)]])
	X0 = X0_list[0]
	for i in range(1,len(X0_list)):
		X0 = concat([X0,X0_list[i]])
	Y0 = Y0_list[0]
	for i in range(1,len(Y0_list)):
		Y0 = concat([Y0,Y0_list[i]])
	
	#convert to numpy arrays, leave Y unchanged for now
	X0 = preprocessing.scale(numpy.array(X0))
			
	return X0,Y0

def predict_winners(X0,Y0,X1):

	Y_train = numpy.array(Y0[Y0.columns[0:1]])
	Y_train = Y_train.reshape((len(Y_train),))
		
	clf = svm.SVC()
	clf.fit(X0,Y_train)
	
	win_predict = clf.predict(X1)
	
	return win_predict
	
def regress_spread(X0,Y0,X1):

	Y_spread_train = numpy.array(Y0[Y0.columns[1:2]])
	Y_spread_train = Y_spread_train.reshape((len(Y_spread_train),))
	
	clf_spread = svm.SVR(epsilon=0.1)
	clf_spread.fit(X0,Y_spread_train)
	spread_predict = clf_spread.predict(X1)

	return spread_predict
	
def main():

	final_list = []

	#iterate over all files	
	for filename in filenames():

		lines = [[s.strip() for s in line[:-1].split(',')] for line in open(filename,'r').readlines()]

		#put data in right form
		X0,Y0 = arrange_data()
		X1 = csv_to_numpy(filename)

		#get all predictions	
		win_predict = predict_winners(X0,Y0,X1)
		spread_predict = regress_spread(X0,Y0,X1)

		#reshape data	
		win_predict = [i[0] for i in win_predict.reshape((len(win_predict),1))]
		spread_predict = [i[0] for i in list(spread_predict.reshape((len(spread_predict),1)))]

		#put results in correct form (date,team,stats)	
		results = {i:[0,0,0,0,0] for i in list_of_teams()}
	
		for i in range(len(win_predict)):
			if win_predict[i]==1:
				results[lines[i+1][1]][0]+=1
				results[lines[i+1][2]][1]+=1
			if win_predict[i]==0:
				results[lines[i+1][1]][1]+=1
				results[lines[i+1][2]][0]+=1

		for i in range(len(spread_predict)):
			results[lines[i+1][1]][2]+=spread_predict[i]
			results[lines[i+1][2]][2]-=spread_predict[i]

		for i in range(len(spread_predict)):
			results[lines[i+1][1]][3]=lines[i+1][-2]
			num_wins = int(float(lines[i+1][7])*10)
			results[lines[i+1][1]][4]=str(num_wins)+"-"+str(10-num_wins)

		for key in results.keys():
			final_list.append([lines[1][0],key,results[key][3],
								results[key][4],results[key][0],results[key][1],
								results[key][2],
								str(results[key][0])+"-"+str(results[key][1])])
	
	#output to a single .csv
	output_file = csv.writer(open('powerrank.csv','wb'))
	output_file.writerows(final_list)
	
	
# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
  main()
