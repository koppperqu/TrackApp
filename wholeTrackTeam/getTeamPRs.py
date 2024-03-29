#This file will go out and grab all the prs of the team before the season starts (or whenever) so everyone has an entry.
#If someone is added to the team during the season then they will just be added to the list as the season goes on.
#I.E. look in pr list is name not found go get their pr's from tffrs.
#Should also say print something in console if a event is found that is not recorded
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
html = urlopen('https://www.tfrrs.org'+womensURL)
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

#Create backup of old list then create new pr file with the people on the team when the script is ran (right now)
#Old files can be used for other fun things im sure
#Creates backups works as of 03/16/2022
import time
current_date_and_time = time.strftime("%m_%d_%Y_%H_%M")
dt = time.strftime("%m_%d_%Y_%H_%M")
teamPRSToBeBackedUp = open('team_prs.txt','r')
filename = "backups/team_prs_"+dt+'.txt'
teamPRBackup = open(filename, "a")
teamPRBackup.write(teamPRSToBeBackedUp.read())
teamPRBackup.close()
teamPRSToBeBackedUp.close()
clearteamPRS = open('team_prs.txt','w')
clearteamPRS.close()

#Puts each line in the pr file into a string array so they can be modified if needed or added then rewrote to the pr file


prTemplate=['Name','60','100','200','300','400','600','800','1000','1500','8K (XC)','6K (XC)','2 MILE','MILE','3000','5000','10,000','100H','110H','60H','55H','400H','3000S','4x100','4x400','DMR','HJ','PV','LJ','TJ','SP','WT','DT','HT','JT','DEC','HEP','PENT']
newPRLine=['name','nomark','nomark','nomark','nomark','nomark','nomark','nomark','nomark','nomark','nomark','nomark','nomark','nomark','nomark','nomark','nomark','nomark','nomark','nomark','nomark','nomark','nomark','nomark','nomark','nomark','nomark','nomark','nomark','nomark','nomark','nomark','nomark','nomark','nomark','nomark','nomark','nomark','nomark']
#only needed if updating the list
teamPRS=open('team_prs.txt','r')
holdEachLine = []
holdEachLine.append(prTemplate)
for eachLine in teamPRS:
    holdEachLine.append(eachLine.split('|'))

teamPRS.close()

#This code will look through the list but wont find anything because file will be empty
#legacy code should be fixed

for tffrLinkindex,eachLink in enumerate(tffrsLink):#goes through each persons tffrs page
    html = urlopen('https://www.tfrrs.org'+eachLink)
    soup=BeautifulSoup(html.read(), "html.parser")
    if names[tffrLinkindex] in soup.find('title').getText():#checks to make sure it is correct person
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
            if names[tffrLinkindex] in holdEachLine[0]:#bool set bc it was found in list
                notFoundInList=False
        if notFoundInList:#adds newPRLine with persons name
            import copy
            newPRLine[0]=names[tffrLinkindex]
            holdEachLine.append(copy.deepcopy(newPRLine))
        for eventIndex,eachEvent in enumerate(events):#for each event on the persons page go to the row with their name (tffrLinkindex + 1) since list is being created from scratch and set pr mark(eventIndex) on correct spot (prTemplate.index(formatEvent))
            formatEvent=eachEvent.getText().strip()
            specialEvents=['8K','6K','2 MILE']#special case events that must get formmate different because space in the name
            for each in specialEvents:
                if each in formatEvent:
                    split=formatEvent.split(' ')
                    formatEvent=split[0].strip()+' '+split[1].strip()
            #prTemplate.index(formatEvent) gives the index of the event in each row
            #Maybe add error handling for if event not in prTemplate when using index function here <prTemplate.index(formatEvent)>
            #print (eachEvent)
            #################MUST FORMAT MARKS####################
            #formats mark
            formatMark=marks[eventIndex].getText().strip()
            if formatEvent in ['HJ','PV','LJ','TJ','SP','WT','DT','HT','JT','100','200','110H','100H']:
                holdCharacters=[]
                tempmark=''
                #Need to go through mark and find m then only use what before m for the mark.
                for eachLetter in formatMark:
                    if eachLetter=='m' or eachLetter=='(':
                        break
                    holdCharacters.append(eachLetter)
                for each in holdCharacters:
                    tempmark=tempmark+each
                formatMark=tempmark
            if formatEvent != "":
                holdEachLine[tffrLinkindex +1][prTemplate.index(formatEvent)]=formatMark.strip()
    else :
        print('skipped '+names[index]+' wrong tffrs page')

teamPRS=open('team_prs.txt','w')
for eachRow in holdEachLine:
    lineToAdd=''
    eachRowLength=len(eachRow)-1
    for columnIndex, eachColumn in enumerate(eachRow):
        if columnIndex == eachRowLength:
            lineToAdd=lineToAdd+eachColumn
        else:
            lineToAdd=lineToAdd+eachColumn+'|'
    teamPRS.write(lineToAdd.strip()+'\n')

teamPRS.close()
print('Done :)')
input()
# html = urlopen('https:'+tffrsLink[0])
# soup=BeautifulSoup(html.read(), "html.parser")
# soup=soup.find('table',class_='table bests')#grabs the personal bests table
# soup=soup.findAll('td')
# print(soup[1].getText().strip())

# print (names)
# print (tffrsLink)