import requests
import bs4

# def getHtml (url,key):
def getHtmlInfo (url,key):
    try:
        dic = {'keyword' : key }
        browser = {'User-Agent' : 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'}
        html = requests.get(url,params = dic, headers = browser)
        html.raise_for_status()
        html.encoding = html.apparent_encoding
        return html.text
    except:
        return ''

def getSinglePage (html):
    soup = bs4.BeautifulSoup(html,'html.parser')
    infoForEach = [] #productName / prize / shopName
    for eachProduct in soup.find_all('div',attrs = 'gl-i-wrap'):
        if isinstance (eachProduct,bs4.element.Tag):
            nameInfo = eachProduct.find(attrs = 'p-name p-name-type-2').em.contents[-1]
            prizeInfo = eachProduct.strong.i.string
            shop = eachProduct.find(attrs = 'p-shop')
            if shop.a is not None:
                shopInfo = shop.a.string
                infoForEach.append([prizeInfo,nameInfo,shopInfo])
    return infoForEach

def printList (productList):
    print('prize \t\t\t product \t\t\t shop')
    for x in productList:
        print(x)

def main ():
    url = 'https://search.jd.com/Search'
    product = 'air jordan'
    html = getHtmlInfo(url,product)
    productList = getSinglePage(html)
    printList(productList)

main()