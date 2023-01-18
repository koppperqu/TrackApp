# #This file will ask user if they want the most recent track meet results or if they want to enter in a meet manualy
# #in the event a meet took place and this file was not executed
# response=input('Do you want PR\'s from the most recent track meet? (y/n): ')
# #n
# Y              # FOR TESTING IN CMD comment out for running the file to work
# correctResponse=False
# validResponses=['y','n','Y','N']
# while not correctResponse:
    # for eachValidResponse in validResponses:
        # if response==eachValidResponse:
            # correctResponse=True
    # if not correctResponse:
        # response=input ('please enter valid answer y or n: ')

# response=response.lower()
# if response =='y':
    # url = 'https://www.tfrrs.org/teams/WI_college_m_Wis_Stevens_Point.html'

# if response =='n':
    # url = input('Please go to the meet you would like to get the PR\'s from and paste the URL here ')
    # goodURL=False
    # while not goodURL:
        # if 'https://www.tfrrs.org' not in url:
            # url = input('Please paste a valid TFRRS link -> ')
        # else:
            # goodURL=True

# print ('Getting PR\'s from most recent results')

#VVVVComments are me debating on how to go about cheking for pr's

#TWO PATHS CAN BE TAKEN TO SEE IF SOMEONE PR
#1 check the persons tffrs page like whats done to get prs in first place
#See if the number changed if it did=pr

#2 go to the most recent meet and go through every event to see if a person pr'd
#This avoid unneisarliy checking people who did not compete, however it would be more work as
#different events are displayed differently, probably easier in the end to do method 1,

#Method 1 would also midigate the issue of missing a meet, but could miss someones pr if the 
#pr twice at two meets or something if meets are back to back and different

#Code below here will go the the given url, if none is given then it get the most recent meet url
#After going to the meet the urls for womens events and mens events all get grabbed and put into 2 lists menEventURLs and womenEventURLS
#For each event 


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

#Template rows
prTemplate=['Name','60','100','200','300','400','600','800','1000','1500','8K (XC)','6K (XC)','2 MILE','MILE','3000','5000','10,000','100H','110H','60H','55H','400H','3000S','4x100','4x400','DMR','HJ','PV','LJ','TJ','SP','WT','DT','HT','JT','DEC','HEP','PENT']
newPRLine=['name','nomark','nomark','nomark','nomark','nomark','nomark','nomark','nomark','nomark','nomark','nomark','nomark','nomark','nomark','nomark','nomark','nomark','nomark','nomark','nomark','nomark','nomark','nomark','nomark','nomark','nomark','nomark','nomark','nomark','nomark','nomark','nomark','nomark','nomark','nomark','nomark','nomark','nomark']
#only needed if someone is not in the list

#Puts each row from the pr text file into a list
teamPRS=open('team_prs.txt','r')
holdEachLine = []
holdEachLine.append(prTemplate)
for eachLine in teamPRS:
    holdEachLine.append(eachLine.split('|'))

teamPRS.close()

import copy
forUpdatingPRFile=copy.deepcopy(holdEachLine)

#This code goes to each URL in the tffrsLink list and sees if the person has any pr's

#ABOVE SHOULD WORK (UNTESTED) BELOW NEEDS TO BE MODIFED

for tffrLinkindex,eachLink in enumerate(tffrsLink):#goes through each persons tffrs page and finds the row in the holdEachLine list
    html = urlopen('https://www.tfrrs.org'+eachLink)
    soup=BeautifulSoup(html.read(), "html.parser")
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
        newPRLine[0]=names[tffrLinkindex]
        holdEachLine.append(copy.deepcopy(newPRLine))
    for eventIndex,eachEvent in enumerate(events):#for each event on the persons page go to the row with their name
    #and set pr mark(eventIndex) on correct spot (prTemplate.index(formatEvent))
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
        #This will find the index(row) the person is in holdEachLine
        for correctRowInHoldEachLine,eachLine in enumerate(holdEachLine):
            if eachLine[0]==names[tffrLinkindex]:
                break
        for correctRowInforUpdatingPRFile,eachLine in enumerate(forUpdatingPRFile):
            if eachLine[0]==names[tffrLinkindex]:
                break
        if formatEvent != "":
            holdEachLine[correctRowInHoldEachLine][prTemplate.index(formatEvent)]=formatMark.strip()
            if forUpdatingPRFile[correctRowInforUpdatingPRFile][prTemplate.index(formatEvent)]!=holdEachLine[correctRowInHoldEachLine][prTemplate.index(formatEvent)]:
                if forUpdatingPRFile[correctRowInforUpdatingPRFile][prTemplate.index(formatEvent)]=='nomark':
                    print (names[tffrLinkindex]+' did the ' + formatEvent + ' for the fist time their pr is '+ holdEachLine[correctRowInHoldEachLine][prTemplate.index(formatEvent)])
                else:
                    print (names[tffrLinkindex]+' pr\'d in ' + formatEvent + ' their old one was ' + forUpdatingPRFile[correctRowInforUpdatingPRFile][prTemplate.index(formatEvent)] + ' new pr is ' + holdEachLine[correctRowInHoldEachLine][prTemplate.index(formatEvent)])

# print (url)





input('Press Enter to Close')