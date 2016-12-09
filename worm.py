__Author__="Guoliang Lin"

import urllib.request
from bs4 import BeautifulSoup
import ftpdownload as fd
import sys
import xlsxwriter



def getHtml(url):
    page = urllib.request.urlopen(url)
    html =page.read()
    return html

def getfilelink(href: str):
    if href.find("ftp://")==0:
        href=href.replace("ftp://",'')
    HOST,DIR=href.split('/',1)
    DIR=DIR.strip('/')
    return HOST,DIR



def downloadacc(prefix,acc):
    html=getHtml(prefix+acc)
    soup=BeautifulSoup(html,"html.parser")
    m=soup.findAll("table")
    #第-6表中包含所有的信息，第-2表格中包含要下载的数据来源

    information=m[-6].text
    # print(information)
    # print(m[-2].text)
    length=len(m[-2])
    for tags in m[-2]:
        # type(tags)
        if type(tags)==type(m[-2]) and  tags.text.find("SRX")!=-1:
            q=tags.find("a")
            HOST,DIR=getfilelink(q["href"])
            listfile=fd.DownloadFile(HOST,DIR)
            # print(q["href"])
            break
    return [acc,listfile,information]

if __name__=='__main__':
    with open(sys.argv[1],'r') as imputfile:
        with open("datacollect.csv",'w') as csvfile:
            workbook=xlsxwriter.Workbook("collectdata.xlsx")
            worksheet=workbook.add_worksheet()
            worksheetrow=0
            worksheetcol=0
            for item in imputfile:
                item=item.strip()
                m=downloadacc(sys.argv[2],item)
                if len(m[1])==1:
                    worksheet.write(worksheetrow,worksheetcol,m[0])
                    worksheet.write(worksheetrow,worksheetcol+5,m[2])
                else:
                    worksheet.merge_range(worksheetrow,worksheetcol,worksheetrow+len(m[1])-1,worksheetcol,m[0])
                    worksheet.merge_range(worksheetrow,worksheetcol+5,worksheetrow+len(m[1])-1,worksheetcol+5,m[2])
                for item in m[1]:
                    for x in range(len(item)):
                        worksheet.write(worksheetrow,worksheetcol+x+1,item[x])
                    worksheetrow+=1
            # except:
            #     print("error")
            # finally:
            workbook.close()