import requests
import re
from bs4 import BeautifulSoup
import bs4

class Uni:
	def __init__(self, rank = -99,name = "Unkown",score = -99):
		self.rank = rank
		self.name = name
		self.score = score

	def display (self):
		print(self.rank,'\t\t',self.name[:5],'\t\t',self.score)



# this method is to get the code of website
def getHTMLText(url):
	try:
		r = requests.get(url)
		r.raise_for_status()
		r.encoding = r.apparent_encoding
		return r.text
	except:
		print("Error!")
		return None

# this method is to get the info and write into classes
def fillUniList(r):
	soup = BeautifulSoup(r,'html.parser')
	uniList = []
	for demo in soup.find('tbody').children:
		if isinstance (demo,bs4.element.Tag):
			uniInfo = []
			for demo2 in demo.find_all('td'):
				uniInfo.append(demo2.string)
			uni = Uni(uniInfo[0],uniInfo[1],uniInfo[4])
			uniList.append(uni)
	return uniList


def printUniList(lists):
	print('rank','\t\t','name','\t\t\t',"score")
	for i in range (0,100):
		lists[i].display()


def main ():
	url = 'http://www.zuihaodaxue.cn/ARWU2018.html'
	demo = getHTMLText(url)
	uniList = fillUniList(demo)
	printUniList(uniList)


main()


