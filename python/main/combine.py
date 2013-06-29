'''
combine.py
Author: Matthew Folz
Project: GameChooser

This file takes in the .csv files output by the script augment-shifted.py, and inputs
them into a single file, which contains duplicates of each game.  Some other minor
formatting is done.
'''

import sys
import csv
from pandas import *
import datetime
import glob
		
def main():

	#load all files into a Pandas dataframe
	for filename in glob.glob("*.csv"):
		file = open(filename)	
		new_frame = DataFrame.from_csv(file)

		try:
			df = concat([df,new_frame])
		except(NameError):
			df = new_frame

	#write dataframe to CSV
	df = df.sort()
	f = open('results.csv','wb')
	df.to_csv(f)

	#do some formatting on the CSV (mainly replacing New Jersey with Brooklyn -- team
	#moved in 2012-2013.
	f = open('results.csv')
	
	count = 0
	output = []
	for line in f.readlines():
		if count == 0:
			first_line = [s.strip() for s in line[:-1].split(',')]
			count+=1
		else:
			s = [s.strip() for s in line[:-1].split(',')]
			for i in range(len(s)):
				if s[i]=="New Jersey":
					s[i]="Brooklyn"
			output.append(s)
	
	output = sorted(output)
	output.insert(0,first_line)
	
	#write to new CSV file
	output_file = csv.writer(open('output_file.csv','wb'))
	output_file.writerows(output)

# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
  main()
