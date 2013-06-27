import sys
import urllib2
import bs4
import csv

def scrape_url(url,team):

	html = urllib2.urlopen(url).read()
	soup = bs4.BeautifulSoup(html)
	
	rows = soup.findAll("tr",{"class":"datarow"})
	entries = [i.findAll("td") for i in rows]
	
	game_results = []
	for i in entries:
		raw_data = [j.text for j in i]
		
		date = str(raw_data[0])[-8:]
		
		opp_str = str(raw_data[1])
		
		home = 0
		if opp_str.find("@") == -1:
			home = 1
		
		if home == 1:
			opponent = opp_str[1:-1]
		elif home == 0:
			opponent = opp_str[opp_str.rfind("@")+2:-1]
		
		spread_size = 0
		if str(raw_data[4]).rfind("W")!=-1:
			win_spread = 1
			if str(raw_data[4])[str(raw_data[4]).rfind("W")+2:]=="PK":
				spread_size = 0			
			else:
				spread_size = float(str(raw_data[4])[str(raw_data[4]).rfind("W")+2:])	
		elif str(raw_data[4]).rfind("L")!=-1:
			win_spread = 0
			if str(raw_data[4])[str(raw_data[4]).rfind("L")+2:]=="PK":
				spread_size = 0
			else:
				spread_size = float(str(raw_data[4])[str(raw_data[4]).rfind("L")+2:])	
		elif str(raw_data[4]).rfind("P")!=-1:
			win_spread = 0.5
			spread_size = float(str(raw_data[4])[str(raw_data[4]).rfind("P")+2:])	

		over_under = 0
		
		if str(raw_data[5]).rfind("O")!=-1:
			win_total = 1
			over_under = float(str(raw_data[5])[str(raw_data[5]).rfind("O")+2:])
		elif str(raw_data[5]).rfind("P")!=-1:
			win_total = 0.5
			over_under = float(str(raw_data[5])[str(raw_data[5]).rfind("P")+2:])		
		elif str(raw_data[5]).rfind("U")!=-1:
			win_total = 0
			over_under = float(str(raw_data[5])[str(raw_data[5]).rfind("U")+2:])	

		
		win_outright = 1
		if str(raw_data[2]).rfind("W") == -1:
			win_outright = 0


		overtime = 0
		
		score_str = str(raw_data[2])[str(raw_data[2]).rfind("  ")+1:].split("-")
		if score_str[1].rfind("(") == -1:
			own_score,opponent_score = int(score_str[0]),int(score_str[1])
		else:
			overtime = 1
			own_score = int(score_str[0])
			opponent_score = int(score_str[1][:score_str[1].rfind("(")-1])

		total_score = own_score+opponent_score
		
		data = [date,home,team,opponent,spread_size,over_under,win_outright,win_spread,win_total,own_score,opponent_score,total_score,overtime]
		if str(raw_data[3])[-6:]=='Season' and overtime==0:
			game_results.append(data)
	
	game_results.reverse()
	
	return game_results
		
def main():

	labels = (['date','is_home','team','opponent','spread_size','over_under','win_outright',
				'win_spread','win_total','own_score','opponent_score','total_score',
				'overtime'])

	team_num_dict = ({'Boston':'404169', 'Brooklyn':'404117', 'New York':'404288',
						'Philadelphia':'404083','Toronto':'404330','Chicago':'404198',
						'Cleveland':'404213','Detroit':'404153','Indiana':'404155',
						'Milwaukee':'404011','Atlanta':'404085','Charlotte':'664421',
						'Miami':'404171','Orlando':'404013','Washington':'404067',
						'Denver':'404065','Minnesota':'403995','Oklahoma City':'404316',
						'Portland':'403993','Utah':'404031','Golden State':'404119',
						'L.A. Clippers':'404135','L.A. Lakers':'403977','Phoenix':'404029',
						'Sacramento':'403975','Dallas':'404047','Houston':'404137',
						'Memphis':'404049','New Orleans':'404101','San Antonio':'404302'})
						
	url_prefix = "http://www.covers.com/pageLoader/pageLoader.aspx?page=/data/nba/teams/pastresults/"
	year = [str(i)+"-"+str(i+1) for i in range(2006,2013)]		

	for i,j in team_num_dict.iteritems():
		for k in year:
			output_filename = i+"_"+k+".csv"
			output_file = open(output_filename,'wb')
			rows = csv.writer(output_file)
			url = url_prefix+"/"+k+"/team"+j+".html"
			formatted_data = scrape_url(url,i)
			formatted_data.insert(0,labels)
			rows.writerows(formatted_data)			
	
# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
  main()
