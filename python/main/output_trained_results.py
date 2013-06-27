import sys
import csv
from pandas import *
from datetime import *
import numpy
from numpy import reshape
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm
from sklearn import preprocessing

def arrange_data():

	df = DataFrame.from_csv(open('final.csv'))
	
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
	
	X1 = df[df.columns[2:22]][datetime(2013,1,1):datetime(2013,4,18)]
	Y1 = df[df.columns[22:28]][datetime(2013,1,1):datetime(2013,4,18)]

	X0 = X0_list[0]
	for i in range(1,len(X0_list)):
		X0 = concat([X0,X0_list[i]])

	Y0 = Y0_list[0]
	for i in range(1,len(Y0_list)):
		Y0 = concat([Y0,Y0_list[i]])
	
	#convert to numpy arrays, leave Y unchanged for now
	X0 = preprocessing.scale(numpy.array(X0))
	X1 = preprocessing.scale(numpy.array(X1))
			
	return (X0,Y0,X1,Y1)

def predict_winners_and_probs(X0,Y0,X1,n_estimators=1000):

	Y_train = numpy.array(Y0[Y0.columns[0:1]])
	Y_train = Y_train.reshape((len(Y_train),))
		
	clf = RandomForestClassifier(n_estimators)
	clf.fit(X0,Y_train)
	
	win_predict = clf.predict(X1)
	prob_predict = clf.predict_proba(X1)
	
	return (win_predict,prob_predict)
	
def regress_spread_and_scores(X0,Y0,X1):

	Y_spread_train = numpy.array(Y0[Y0.columns[1:2]])
	Y_spread_train = Y_spread_train.reshape((len(Y_spread_train),))
	
	Y_homescore_train = numpy.array(Y0[Y0.columns[2:3]])
	Y_homescore_train = Y_homescore_train.reshape((len(Y_homescore_train),))
		
	Y_awayscore_train = numpy.array(Y0[Y0.columns[3:4]])
	Y_awayscore_train = Y_awayscore_train.reshape((len(Y_awayscore_train),))
	
	clf_spread = svm.SVR(epsilon=0.1)
	clf_spread.fit(X0,Y_spread_train)
	spread_predict = clf_spread.predict(X1)

	clf_homescore = svm.SVR(epsilon=0.1)
	clf_homescore.fit(X0,Y_homescore_train)
	homescore_predict = clf_homescore.predict(X1)
	
	clf_awayscore = svm.SVR(epsilon=0.1)
	clf_awayscore.fit(X0,Y_awayscore_train)
	awayscore_predict = clf_awayscore.predict(X1)	
	
	clf_totalscore = svm.SVR(epsilon=0.1)
	clf_totalscore.fit(X0,Y_awayscore_train+Y_homescore_train)
	totalscore_predict = clf_totalscore.predict(X1)

	return (spread_predict,homescore_predict,awayscore_predict,totalscore_predict)
	
def main():

	X0,Y0,X1,Y1 = arrange_data()
	
	win_predict,prob_predict = predict_winners_and_probs(X0,Y0,X1)
	spread_predict,homescore_predict,awayscore_predict,totalscore_predict = regress_spread_and_scores(X0,Y0,X1)
	
	win_predict = win_predict.reshape((len(win_predict),1))
	prob_predict = prob_predict[:,1]
	prob_predict = prob_predict.reshape((len(win_predict),1))
	spread_predict = spread_predict.reshape((len(spread_predict),1))
	homescore_predict = homescore_predict.reshape((len(homescore_predict),1))
	awayscore_predict = awayscore_predict.reshape((len(homescore_predict),1))
	totalscore_predict = totalscore_predict.reshape((len(homescore_predict),1))

	df = DataFrame.from_csv(open('final.csv'))

	df_selected = df[datetime(2013,1,1):datetime(2013,4,18)]
	df_selected['win_predict'] = win_predict
	df_selected['prob_predict'] = prob_predict
	df_selected['spread_predict'] = spread_predict
	df_selected['homescore_predict'] = homescore_predict
	df_selected['awayscore_predict'] = awayscore_predict
	df_selected['totalscore_predict'] = totalscore_predict
	
	df_selected.to_csv(open('predictions.csv','wb'))
	
# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
  main()
