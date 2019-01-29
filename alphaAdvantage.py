import requests
import json
import plotly.plotly as py
import plotly.graph_objs as go

#configureing plotly
#plotly.tools.set_credentials_file(username='baubrey1995', api_key='MhknaPvemAoRWETVOW5q')

#My API Key
API_KEY = "DX51OTRPXJAVT9O2"

#URL to access our info
#stock symbols(Required)
#datatype(Optional) can be JSON(Default) or CSV
#outputsize can be compact(limits to 100 data points) or full
#interval(Required)  can be 1, 5, 15, 30, 60 minutes
URL = "https://www.alphavantage.co/query?"
INTRA_DAY_URL = "function=TIME_SERIES_INTRADAY"
DAILY_URL = "function=TIME_SERIES_DAILY"
SYMBOLS = ["MSFT","ATVI","AAPL"]
SIZE = "compact" 
INTERVAL = "5min"

#Constants used to extract data
OPEN = "1. open"
HIGH = "2. high"
LOW = "3. low"
CLOSE = "4. close" 
VOL = "5. volume" 


#function for making request to Alpha Advantage. Symbol is expected to be stock Ticker symbol
def makeIntraDayRequest(self, symbol = None):
	req = URL + INTRA_DAY_URL + '&symbol=' + s + '&interval=' + INTERVAL + '&outputsize=' + SIZE + '&apikey=' + API_KEY
	data = requests.get(req)
	data = data.json()
	return data

#function for making request to Alpha Advantage. Symbol is expected to be stock Ticker symbol	
def makeDailyRequest(self, symbol = None):
	req = URL + DAILY_URL + '&symbol=' + s + '&outputsize=' + SIZE + '&apikey=' + API_KEY
	print("Making request to: " + req)
	data = requests.get(req)
	data = data.json()
	return data

#Function used to save to a file. Symbol: stock ticker symbol. Data: information to save
def saveFile(symbol, data):
	filename = s + ".json"
	with open(filename, 'w') as outfile:
		json.dump(data, outfile, indent=4)
	
#Function that does things
def processData(s, data):
	#Selects the data
	entries = data["Time Series (Daily)"]
		
	opening = {}
	highs = {}
	lows = {}
	closing = {}
	volume = {}
	#Each entry has a time stamp for a key and a dict of values	
	for date, entry in entries.items():
		opening[date] = entry["1. open"]
		highs[date] = entry["2. high"]
		lows[date] = entry["3. low"]
		closing[date] = entry["4. close"]
		volume[date] = entry["5. volume"]
		
	#use our function to format data into a trace object used for plotly	
	ohlcData = makeOhlcTrace(
		s,
		[*entries],
		[*opening.values()],
		[*highs.values()],
		[*lows.values()],
		[*closing.values()]
	)
	return ohlcData
		
#Converts dict with (Key, value) pairs into trace object with x=key, y=value 
#Used for plotly line charts
def makeLineTrace(dict, label, type):
	trace = go.Scatter(
		x = [*dict],
		y = [*dict.values()],
		name = label,
		mode = type
	)
	
	return trace

#Converts 5 lists into trace object 
#Used for plotly stock charts
def makeOhlcTrace(label,dates, opens, highs, lows, closes):
	trace = go.Ohlc(
		name=label,
		x=dates,
		open=opens,
		high=highs,
		low=lows,
		close=closes
	)
	
	return trace	
			
	
traces = []	
for s in SYMBOLS:
	data = makeDailyRequest(s)
	saveFile(s, data)
	traces.append(processData(s, data))
	
py.iplot(traces, filename='stock_data')	




