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
    nameParts=eachLink.getText().split(', ')
    names.append(nameParts[1]+' '+nameParts[0])
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
    nameParts=eachLink.getText().split(', ')
    names.append(nameParts[1]+' '+nameParts[0])
    tffrsLink.append(eachLink['href'])
#
#Works really good up till this point need to decided how to go through all names/pages to update the pr's most effienclty
#do I rewrite the whole file everytime getting all prs from the team page at the end or just update the existing list adding
#new people and updating old peoples pr's?
#
#Puts each line in the pr file into a string array so they can be modified if needed or added then rewrote to the pr file
teamPRS=open('team_prs.txt','r')
holdEachLine = []
prTemplate=['Name','60','100','200','300','400','600','800','1000','1500','8K (XC)','6K (XC)','2 MILE','MILE','3000','5000','10,000','100H','110H','60H','55H','400H','3000S','4x100','4x400','DMR','HJ','PV','LJ','TJ','SP','WT','DT','HT','JT','DEC','HEP','PENT']
newPRLine=['name','nomark','nomark','nomark','nomark','nomark','nomark','nomark','nomark','nomark','nomark','nomark','nomark','nomark','nomark','nomark','nomark','nomark','nomark','nomark','nomark','nomark','nomark','nomark','nomark','nomark','nomark','nomark','nomark','nomark','nomark','nomark']
for eachLine in teamPRS:
    holdEachLine.append(eachLine.split('|'))

teamPRS.close()
for index,eachLink in enumerate(tffrsLink):#goes through each persons tffrs page
    html = urlopen('https:'+eachLink)
    soup=BeautifulSoup(html.read(), "html.parser")
    if names[index] in soup.find('title').getText():#checks to make sure it is correct person
        soup=soup.find('table',class_='table bests')#grabs the personal bests table
        soup=soup.findAll('td')
        events=[]
        marks=[]
        for index,each in enumerate(soup):
            if index%2==0:
                events.append(each)
            else:
                marks.append(each)
        for eachLine in holdEachLine:#check to see if the person is in the pr list if not add it with newPRLine
            notFoundInList=True
            if names[index] in holdEachLine[0]:#if not in the list then add row change new prLine name to correct name
                print('bool set bc it was found')
                notFoundInList=False
        if notFoundInList:
            import copy
            newPRLine[0]=names[index]
            holdEachLine.append(copy.deepcopy(newPRLine))
        for eachEvent in events:#for each event on the persons page look for the row in holdEachLine then change it to be correct pr
            eventFound=False
            formatEvent=eachEvent.getText().strip()
            specialEvents=['8K','6K','2 MILE']#special case events that must get formmate different because space in the name
            for each in specialEvents:
                if each in formatEvent:
                    split=formatEvent.split(' ')
                    formatEvent=split[0].strip()+' '+split[1].strip()
            for eventIndex,event in enumerate(prTemplate):#checks to make sure all events are in the pr template
                if formatEvent==event:
                    eventFound=True
            if not eventFound:
                if formatEvent!='':
                    print(formatEvent.strip()+' not found')
            for eachPRRow in holdEachLine:
                if names[index] in holdEachLine[0]:
                    holdEachLine[prTemplate.index(eachEvent)]=marks[prTemplate.index(eachEvent)]
    else :
        print('skipped '+names[index]+' wrong tffrs page')

html = urlopen('https:'+tffrsLink[0])
soup=BeautifulSoup(html.read(), "html.parser")
soup=soup.find('table',class_='table bests')#grabs the personal bests table
soup=soup.findAll('td')
print(soup[1].getText().strip())

print (names)
print (tffrsLink)