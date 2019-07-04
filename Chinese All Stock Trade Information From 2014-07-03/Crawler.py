import requests
import re
import os
from bs4 import BeautifulSoup
from multiprocessing import Pool

_URL1_ = 'https://query1.finance.yahoo.com/v7/finance/download/'
_URL2_ = '.SS?period1=1404397800&period2=1562164200&interval=1d&events=history&crumb=PXouoNWzdUz'
_PATH_ = './stockInfo'

def openFileToWrite (root):
	if not os.path.exists(root):
		os.mkdir(root)

def getTheStockList ():
	try:
		stockList = []
		url = 'http://quote.eastmoney.com/stock_list.html#sh'
		html = requests.get(url)
		html.raise_for_status()
		html.encoding = html.apparent_encoding
		soup = BeautifulSoup(html.text,'html.parser')
		soup = soup.find(attrs = 'qox').ul
		soup = soup.find_all('li')
		# soup = soup.a.string
		for x in soup:
			info = x.a.string
			info2 = re.search(r'\d{6}',info)
			if info2 is not None:
				stockList.append(info2.group(0))
		return stockList
	except:
		return None

def getInfoAndWrite (stockUrl):
	try:
		url = _URL1_+stockUrl+_URL2_
		cookiesDict = {'cookie':'APID=UP82ff4df7-01a2-11e9-983b-0a02e8ef0008; GUC=AQEBAQFdGWZd9kIb2AQY&s=AQAAAJsN78Ub&g=XRgdoA; PRF=t%3D600004.SS%252B%255EDJI; APIDTS=1562218968; B=628jmehe1e21u&b=3&s=1i; cmp=t=1562222947&j=0'}
		html = requests.get(url, cookies = cookiesDict)
		html.raise_for_status()
		path = _PATH_ +'/'+ stockUrl + '.csv'
		f = open(path,'wb')
		f.write(html.content)
		f.close()
		print(stockUrl,'Succeed!')
	except:
		print(stockUrl,'Faild!')
		pass

def main ():
	openFileToWrite(_PATH_)
	stockList = getTheStockList ()
	pool = Pool (5)
	pool.map(getInfoAndWrite,stockList)

main()









