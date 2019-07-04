# 本代码运行后将截取所有中国股票的近五年的交易信息
# this program will download all Chinese stocks' trading information in the recent 5 years.

import requests
import re
import os
from bs4 import BeautifulSoup
from multiprocessing import Pool

# 本代码从东方财富网截取所有股票代码，从雅虎财经下载所有近五年的股票信息(2014/7/3 - 2019/7/3)
# this code will get All stock number from eastmoney, 
# this code will download all stocks trading information in the recent 5 years (3rd,Jul,2014 - 3rd,Jul,2019)
# 本代码采用多进程形式，降低运行时间
# this code will use multi processing to reduce the running time
# 完全遵守相关爬虫协议
# this coide follows the /Robots.txt



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









