from urllib.request import urlopen
from bs4 import BeautifulSoup
html = urlopen('https://www.tfrrs.org/teams/WI_college_m_Wis_Stevens_Point.html')
soup=BeautifulSoup(html.read(), "html.parser")
toWomensURL=soup.find('div',class_='col-lg-12 pt-5')
womensURL=toWomensURL.findAll('a')
for aTag in womensURL:
    if aTag.getText()=='Women\'s Track & Field':
        womensURL=aTag['href'] #sets womens url so their prs can be gotten and added after the mens are done
        break
#gets the mens roster div
menRoster = soup.findAll('div',class_='col-lg-4')
for div in menRoster:
    if div.find('h3'):
        if 'ROSTER' in div.find('h3'):
            menRoster=div
            break
#adds all the mens names to the names list and the links to the tffrsLink list corresponsing with index number
menRoster=menRoster.findAll('a')
names=[]
tffrsLink=[]
for eachLink in menRoster:
    names.append(eachLink.getText())
    tffrsLink.append(eachLink['href'])

#gets the womens roster div
html = urlopen('https:'+womensURL)
soup=BeautifulSoup(html.read(), "html.parser")
womenRoster = soup.findAll('div',class_='col-lg-4')
for div in womenRoster:
    if div.find('h3'):
        if 'ROSTER' in div.find('h3'):
            womenRoster=div
            break
#adds all the womens names to the names list and the links to the tffrsLink list corresponsing with index number
womenRoster=womenRoster.findAll('a')
for eachLink in womenRoster:
    names.append(eachLink.getText())
    tffrsLink.append(eachLink['href'])

#NEXT TO DO IS CLICK EACH LINK FIGURE OUT WHAT EVENTS THEY DO THEN ADD THEM TO THE PR FILE AND WHAT THEIR PR IS
print (names)
print (tffrsLink)