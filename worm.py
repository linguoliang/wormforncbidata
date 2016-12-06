__Author__="Guoliang Lin"

import urllib.request
from bs4 import BeautifulSoup

def getHtml(url):
    page = urllib.request.urlopen(url)
    html =page.read()
    return html

def getfilelink(Tags):
    herf=Tags["herf"]
    herf=herf+'/'

html=getHtml("https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSM1014631")
soup=BeautifulSoup(html,"html.parser")
m=soup.findAll("table")
#第-6表中包含所有的信息，第-2表格中包含要下载的数据来源

information=m[-6].text
print(information)
print(m[-2].text)
#assert isinstance(tagdownload,list)
# for x in range(len(m)-1):
#     y=m[x+1].find(text="Supplementary file")

print(m[1].string)