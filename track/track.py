#Things to add
#Get peoples pr to display * is throw was a pr
#Grab meet name to display what meet results are from
#Find a way to grab results for men/women shot and weight (4 time running script get correct link to the events
    #I think if I use meet page then look for mens table then shot's href and weight href then same for women it would work
#Start with exporting the results to a txt file then maybe later implement php or js to put it into a webpage(html)
#Go back and look at code to see if it could be made better? (refactor)
#If website route is gone down maybe add a list option to see other schools results or conference standings eventually

from urllib.request import urlopen
from bs4 import BeautifulSoup
#function take 2 lists and gives the difference between the two
#in the use in this app it will hopefully give one round that is the one being displayed
def Diff(li1, li2):
    li_dif = [i for i in li1 + li2 if i not in li1 or i not in li2]
    return li_dif

#grabs the corresponding event urls for each gender.
#take the event name as a parameter must be as shown in TFFRS to work.
def GetGenderEventURLs(eventsRows, eventName):
    for eachEvent in eventsRows:
        if eventName in eachEvent.getText():
            return 'https:'+(eachEvent.find('a', href=True)['href'])
    return 'No event found for ' + eventName

#This function takes a url and returns 2 lists first being names second being the formattedmarks for that name orginized by index 
def PointerResults(url):
    if 'https' in url:
        html = urlopen(url)
        soup=BeautifulSoup(html.read(), "html.parser");
        #Gets style tags (inlkine style)
        styles=soup.findAll('style')
        text=styles[1].getText()
        wrongRounds=[]
        round=''
        classFoundFlag=False
        #Goes through second style tag to find out which class are not displayed to be able to grab right "round" to get right name and marks.
        for each in text:
            if each=='{':
                classFoundFlag=False
                wrongRounds.append(round.strip())
                round=''
            if classFoundFlag:
                round=round+each
            if each=='.':
                classFoundFlag=True
        resultsTable=soup.find("tbody")
        allRoundsNotFound=True
        foundRounds=[]
        #stops looking for classes when duplicate is found
        while allRoundsNotFound:
            for each in resultsTable.findAll('td'):
                if each.attrs['class'][0] in foundRounds:
                    allRoundsNotFound=False
                    break
                foundRounds.append(each.attrs['class'][0])
        rightRound=(Diff(foundRounds,wrongRounds)[0])#CAUSE EARRORS MAYBE IF MORE THAN one RIGHT ROUND
        namesRows = []
        marksRows = []
        names=[]#will get returned
        marks=[]#will get returned
    #Goes through the resultsAndNamesRows list every even row is a names row odd rows are marks rows
    #Due to how the HTML is formatted on the site
        resultsAndNamesRows=resultsTable.findAll('tr')
        for index,eachRow in enumerate(resultsAndNamesRows):
            if index%2==0:
                tabledData=eachRow.findAll('td',class_=rightRound)
                if (type(tabledData[1].find("a"))) != type(None):
                    if "Wis_Stevens_Point" in tabledData[1].find("a")["href"]:#Grabs first <a> tag which is the correct thrower
                        names.append(tabledData[1].find("a").getText()) #got rid of for loop with adding to names here
                        marksRows.append(resultsAndNamesRows[index+1])#adds that persons marks row so same index
        marksFormatted=[]
        for i in marksRows:
            marks=i.findAll("li")
            c=[]
            for i in marks:
                i=i.getText().strip().strip("m")
                if i=='' :
                    break
                c.append(i)
            marksFormatted.append(c)
        
        for index,eachname in enumerate(names):
            nameparts=eachname.strip().split(',')
            names[index]=nameparts[1].strip()+' '+nameparts[0]
        #made into own function
        # highestMarks = []
        # throwNumbers = []
        for eachRowOfMarks in marksFormatted:
            # championMark=0
            # throwNumber=0
             for index,mark in enumerate(eachRowOfMarks):
                 if mark =='FOUL':
                     eachRowOfMarks[index]='0'
                     #must set mark =0 otherwise it still reads as string 'foul' if on set mark then 'foul' doesnt change to 0 in the output
                    # mark='0'
                # if float(mark)>championMark:
                    # championMark=float(mark)
                    # throwNumber=index+1
            # highestMarks.append(championMark)
            # throwNumbers.append(throwNumber)
            #prints who threw highest mark on what throw
        # for index,name in enumerate(names):
            # print(name, " threw ", highestMarks[index], " on throw ", throwNumbers[index])
        return names,marksFormatted
    return 'EVENT NOT THROWN'

def GetEventURLS(UWSPTFFRSmain):
    html = urlopen(UWSPTFFRSmain)
    soup=BeautifulSoup(html.read(), "html.parser")
    latestResults=soup.findAll('div',class_='col-lg-8')[1]
    mostRecentRow = latestResults.find('tbody').find('tr').findAll('td')
    mostRecentDate=mostRecentRow[0].getText()
    mostRecentMeet=mostRecentRow[1]
    mostRecentMeetURL= mostRecentMeet.find('a', href=True)['href']
    html = urlopen('http:'+mostRecentMeetURL)
    soup=BeautifulSoup(html.read(), "html.parser")
    events=soup.findAll('div',class_='col-lg-6')
    menEvents=events[0].find('tbody')
    womenEvents=events[1].find('tbody')
    menEventsRows=menEvents.findAll('tr')
    womenEventsRows=womenEvents.findAll('tr')
    listOfEventsURLs=[menEventsRows,womenEvents]
    return listOfEventsURLs

def GetHighestMarksAndThrowNumber(marksFormatted):
    highestMarks = []
    throwNumbers = []
    for eachRowOfMarks in marksFormatted:
        championMark=0
        throwNumber=0
        for index,mark in enumerate(eachRowOfMarks):
            if float(mark)>championMark:
                championMark=float(mark)
                throwNumber=index+1
        highestMarks.append(championMark)
        throwNumbers.append(throwNumber)
    return (highestMarks,throwNumbers)

def ResultsAndIfPersonalRecord (namesInput,highestMarks,eventName):
    prs = open("pr.txt", "r")
    header=prs.readline()#discards first line which just tells what order prs are in for later use
    Names=[]
    WeightPRS=[]
    ShotPRS=[]
    HammerPRS=[]
    DiscusPRS=[]
    NamesToReturn=[]
    HighestMarksToReturn=[]
    for eachLine in prs:
        splitline=eachLine.strip().split(",")
        Names.append(splitline[0])
        WeightPRS.append(splitline[1])
        ShotPRS.append(splitline[2])
        HammerPRS.append(splitline[3])
        DiscusPRS.append(splitline[4])
    prs.close()
    indexsOfThingsToRemove=[]
    #removes people there are no prs for
    for index,eachName in enumerate(namesInput):
        #had to add weird work around because would skip next name if just removed one
        if eachName not in Names:
            indexsOfThingsToRemove.append(index)
            print('!!!!!No prs removed!!!!! ' + eachName)
    offSetList=0
    for eachIndex in indexsOfThingsToRemove:
        namesInput.remove(namesInput[eachIndex+offSetList])
        highestMarks.remove(highestMarks[eachIndex+offSetList])
        offSetList=offSetList-1
    #figure out what row or pr is needed for each person by taking names that come from tffrs and searching through pr
    #list to find out what row (index) their prs are on them put that in a list so its goes in order of index from first name in 
    #list of names from tffrs to last
    prRow=[]
    for eachName in namesInput:
        for index,eachName2 in enumerate(Names):
            if eachName==eachName2:
                prRow.append(index)
                break #stop going through list saves some time.
    #Goes through each highest mark to check if it is higher than the corresponding pr
    import time
    time.sleep(1)
    current_date_and_time = time.strftime("%m_%d_%Y_%H_%M_%S")
    #Makes a backup file of the pr's before they are updated just in case
    pr = open('pr.txt', 'r')
    prBackup = open('prBackup_'+current_date_and_time+'.txt', 'x')
    prBackup.write(pr.read())
    pr.close()
    prBackup.close()
    pr = open('pr.txt', 'w')
    pr.write(header.strip())
    if(eventName=='Shot Put'):
        for index,eachHighestMark in enumerate(highestMarks):
            if(eachHighestMark>float(ShotPRS[prRow[index]])):
                print ('PR!! OLD MARK '+ ShotPRS[prRow[index]]+' new mark ' + str(eachHighestMark) + ' for ' + namesInput[index])
                ShotPRS[prRow[index]]=eachHighestMark
                NamesToReturn.append(namesInput[index])
                HighestMarksToReturn.append(eachHighestMark)
    if(eventName=='Weight Throw'):
        for index,eachHighestMark in enumerate(highestMarks):
            if(eachHighestMark>float(WeightPRS[prRow[index]])):
                print ('PR!! OLD MARK '+ WeightPRS[prRow[index]]+' new mark ' + str(eachHighestMark) + ' for ' + namesInput[index])
                WeightPRS[prRow[index]]=eachHighestMark
                NamesToReturn.append(namesInput[index])
                HighestMarksToReturn.append(eachHighestMark)
    if(eventName=='Hammer'):
        for index,eachHighestMark in enumerate(highestMarks):
            if(eachHighestMark>float(HammerPRS[prRow[index]])):
                print ('PR!! OLD MARK '+ HammerPRS[prRow[index]]+' new mark ' + str(eachHighestMark) + ' for ' + namesInput[index])
                HammerPRS[prRow[index]]=eachHighestMark
                NamesToReturn.append(namesInput[index])
                HighestMarksToReturn.append(eachHighestMark)
    if(eventName=='Discus'):
        for index,eachHighestMark in enumerate(highestMarks):
            if(eachHighestMark>float(DiscusPRS[prRow[index]])):
                print ('PR!! OLD MARK '+ DiscusPRS[prRow[index]]+' new mark ' + str(eachHighestMark) + ' for ' + namesInput[index])
                DiscusPRS[prRow[index]]=eachHighestMark
                NamesToReturn.append(namesInput[index])
                HighestMarksToReturn.append(eachHighestMark)
    for index,eachName in enumerate(Names):
        pr.write('\n'+Names[index]+','+str(WeightPRS[index])+','+str(ShotPRS[index])+','+str(HammerPRS[index])+','+str(DiscusPRS[index]))
    pr.close()
    return NamesToReturn,HighestMarksToReturn

url = 'https://www.tfrrs.org/teams/WI_college_m_Wis_Stevens_Point.html'
menANDwomenURL=GetEventURLS(url)

menShotURL=GetGenderEventURLs(menANDwomenURL[0],'Shot Put')
menWeightURL=GetGenderEventURLs(menANDwomenURL[0],'Weight Throw')
menDiscusURL=GetGenderEventURLs(menANDwomenURL[0],'Discus')
menHammerURL=GetGenderEventURLs(menANDwomenURL[0],'Hammer')

womenShotURL=GetGenderEventURLs(menANDwomenURL[1],'Shot Put')
womenWeightURL=GetGenderEventURLs(menANDwomenURL[1],'Weight Throw')
womenDiscusURL=GetGenderEventURLs(menANDwomenURL[1],'Discus')
womenHammerURL=GetGenderEventURLs(menANDwomenURL[1],'Hammer')

#This code was for my testing/formatting
menShotPointerResults=PointerResults(menShotURL)
if menShotPointerResults!='EVENT NOT THROWN':
    print('\nMen Shot Put \n------------------------------------------')
    resultsMenShot=GetHighestMarksAndThrowNumber(menShotPointerResults[1])
    NamesOfMenPR_Shotput=ResultsAndIfPersonalRecord(menShotPointerResults[0],resultsMenShot[0],'Shot Put')

menWeightPointerResults=PointerResults(menWeightURL)
if menWeightPointerResults!='EVENT NOT THROWN':
    print('\nMen Weight Throw \n------------------------------------------')
    resultsMenWeight=GetHighestMarksAndThrowNumber(menWeightPointerResults[1])
    NamesOfMenPR_Weight=ResultsAndIfPersonalRecord(menWeightPointerResults[0],resultsMenWeight[0],'Weight Throw')

menHammerPointerResults=PointerResults(menHammerURL)
if menHammerPointerResults!='EVENT NOT THROWN':
    print('\nMen Hammer \n------------------------------------------')
    resultsMenHammer=GetHighestMarksAndThrowNumber(menHammerPointerResults[1])
    NamesOfMenPR_Hammer=ResultsAndIfPersonalRecord(menHammerPointerResults[0],resultsMenHammer[0],'Hammer')

menDiscusPointerResults=PointerResults(menDiscusURL)
if menDiscusPointerResults!='EVENT NOT THROWN':
    print('\nMen Discus \n------------------------------------------')
    resultsMenDiscus=GetHighestMarksAndThrowNumber(menDiscusPointerResults[1])
    NamesOfMenPR_Discus=ResultsAndIfPersonalRecord(menDiscusPointerResults[0],resultsMenDiscus[0],'Discus')

womenShotPointerResults=PointerResults(womenShotURL)
if womenShotPointerResults!='EVENT NOT THROWN':
    print('\nWomen Shot Put \n------------------------------------------')
    resultsWomenShot=GetHighestMarksAndThrowNumber(womenShotPointerResults[1])
    NamesOfWomenPR_Shotput=ResultsAndIfPersonalRecord(womenShotPointerResults[0],resultsWomenShot[0],'Shot Put')

womenWeightPointerResults=PointerResults(womenWeightURL)
if womenWeightPointerResults!='EVENT NOT THROWN':
    print('\nWomen Weight Throw \n------------------------------------------')
    resultsWomenWeight=GetHighestMarksAndThrowNumber(womenWeightPointerResults[1])
    NamesOfWomenPR_Weight=ResultsAndIfPersonalRecord(womenWeightPointerResults[0],resultsWomenWeight[0],'Weight Throw')

womenHammerPointerResults=PointerResults(womenHammerURL)
if womenHammerPointerResults!='EVENT NOT THROWN':
    print('\nWomen Hammer \n------------------------------------------')
    resultsWomenHammer=GetHighestMarksAndThrowNumber(womenHammerPointerResults[1])
    NamesOfWomenPR_Hammer=ResultsAndIfPersonalRecord(womenHammerPointerResults[0],resultsWomenHammer[0],'Hammer')

womenDiscusPointerResults=PointerResults(womenDiscusURL)
if womenDiscusPointerResults!='EVENT NOT THROWN':
    print('\nWomen Discus \n------------------------------------------')
    resultsWomenDiscus=GetHighestMarksAndThrowNumber(womenDiscusPointerResults[1])
    NamesOfWomenPR_Discus=ResultsAndIfPersonalRecord(womenDiscusPointerResults[0],resultsWomenDiscus[0],'Discus')

#This will be formatting for instagram and or info to send to matt for videos for the instagram


if 'NamesOfMenPR_Shotput' in locals():
    print('-----------Mens Shotput----------')
    for eachName in NamesOfMenPR_Shotput[0]:
        print (eachName+ ' throw number' , end =' ')
        for index,eachNameInAllMarks in enumerate(menShotPointerResults[0]):
            if eachNameInAllMarks==eachName:
                print (resultsMenShot[1][index])


if 'NamesOfMenPR_Weight' in locals():
    print('-----------Mens Weight----------')
    for eachName in NamesOfMenPR_Weight[0]:
        print (eachName+ ' throw number' , end =' ')
        for index,eachNameInAllMarks in enumerate(menWeightPointerResults[0]):
            if eachNameInAllMarks==eachName:
                print (resultsMenWeight[1][index])

if 'NamesOfMenPR_Hammer' in locals():
    print('-----------Mens Hammer----------')
    for eachName in NamesOfMenPR_Hammer[0]:
        print (eachName+ ' throw number' , end =' ')
        for index,eachNameInAllMarks in enumerate(menHammerPointerResults[0]):
            if eachNameInAllMarks==eachName:
                print (resultsMenHammer[1][index])

if 'NamesOfMenPR_Discus' in locals():
    print('-----------Mens Discus----------')
    for eachName in NamesOfMenPR_Discus[0]:
        print (eachName+ ' throw number' , end =' ')
        for index,eachNameInAllMarks in enumerate(menDiscusPointerResults[0]):
            if eachNameInAllMarks==eachName:
                print (resultsMenDiscus[1][index])


if 'NamesOfWomenPR_Shotput' in locals():
    print('-----------Womens Shotput----------')
    for eachName in NamesOfWomenPR_Shotput[0]:
        print (eachName+ ' throw number' , end =' ')
        for index,eachNameInAllMarks in enumerate(womenShotPointerResults[0]):
            if eachNameInAllMarks==eachName:
                print (resultsWomenShot[1][index])

if 'NamesOfWomenPR_Weight' in locals():
    print('-----------Womens Weight----------')
    for eachName in NamesOfWomenPR_Weight[0]:
        print (eachName+ ' throw number' , end =' ')
        for index,eachNameInAllMarks in enumerate(womenWeightPointerResults[0]):
            if eachNameInAllMarks==eachName:
                print (resultsWomenWeight[1][index])

if 'NamesOfWomenPR_Hammer' in locals():
    print('-----------Womens Hammer----------')
    for eachName in NamesOfWomenPR_Hammer[0]:
        print (eachName+ ' throw number' , end =' ')
        for index,eachNameInAllMarks in enumerate(womenHammerPointerResults[0]):
            if eachNameInAllMarks==eachName:
                print (resultsWomenHammer[1][index])

if 'NamesOfWomenPR_Discus' in locals():
    print('-----------Womens Discus----------')
    for eachName in NamesOfWomenPR_Discus[0]:
        print (eachName+ ' throw number' , end =' ')
        for index,eachNameInAllMarks in enumerate(womenDiscusPointerResults[0]):
            if eachNameInAllMarks==eachName:
                print (resultsWomenDiscus[1][index])

ShotPutPRNames=[]
ShotPutPRMarks=[]
WeightPRNames=[]
WeightPRMarks=[]
HammerPRNames=[]
HammerPRMarks=[]
DiscusPRNames=[]
DiscusPRMarks=[]
#Doing this this way so if meet only has women or mens prs still prints
if 'NamesOfMenPR_Shotput' in locals():
    ShotPutPRNames=ShotPutPRNames+NamesOfMenPR_Shotput[0]
    ShotPutPRMarks=ShotPutPRMarks+NamesOfMenPR_Shotput[1]

if 'NamesOfMenPR_Weight' in locals():
    WeightPRNames=WeightPRNames+NamesOfMenPR_Weight[0]
    WeightPRMarks=WeightPRMarks+NamesOfMenPR_Weight[1]

if 'NamesOfMenPR_Hammer' in locals():
    HammerPRNames=HammerPRNames+NamesOfMenPR_Hammer[0]
    HammerPRMarks=HammerPRMarks+NamesOfMenPR_Hammer[1]

if 'NamesOfMenPR_Discus' in locals():
    DiscusPRNames=DiscusPRNames+NamesOfMenPR_Discus[0]
    DiscusPRMarks=DiscusPRMarks+NamesOfMenPR_Discus[1]

if 'NamesOfWomenPR_Shotput' in locals():
    ShotPutPRNames=ShotPutPRNames+NamesOfWomenPR_Shotput[0]
    ShotPutPRMarks=ShotPutPRMarks+NamesOfWomenPR_Shotput[1]

if 'NamesOfWomenPR_Weight' in locals():
    WeightPRNames=WeightPRNames+NamesOfWomenPR_Weight[0]
    WeightPRMarks=WeightPRMarks+NamesOfWomenPR_Weight[1]

if 'NamesOfWomenPR_Hammer' in locals():
    HammerPRNames=HammerPRNames+NamesOfWomenPR_Hammer[0]
    HammerPRMarks=HammerPRMarks+NamesOfWomenPR_Hammer[1]

if 'NamesOfWomenPR_Discus' in locals():
    DiscusPRNames=DiscusPRNames+NamesOfWomenPR_Discus[0]
    DiscusPRMarks=DiscusPRMarks+NamesOfWomenPR_Discus[1]

if 'NamesOfMenPR_Shotput' in locals() or 'NamesOfWomenPR_Shotput' in locals():
    print('Shot Put')
    for index,each in enumerate(ShotPutPRNames):
        print(each+' - '+str(ShotPutPRMarks[index]))

if 'NamesOfMenPR_Weight' in locals() or 'NamesOfWomenPR_Weight' in locals():
    print('Weight')
    for index,each in enumerate(WeightPRNames):
        print(each+' - '+str(WeightPRMarks[index]))

if 'NamesOfMenPR_Hammer' in locals() or 'NamesOfWomenPR_Hammer' in locals():
    print('Hammer')
    for index,each in enumerate(HammerPRNames):
        print(each+' - '+str(HammerPRMarks[index]))

if 'NamesOfMenPR_Discus' in locals() or 'NamesOfWomenPR_Discus' in locals():
    print('Discus')
    for index,each in enumerate(DiscusPRNames):
        print(each+' - '+str(DiscusPRMarks[index]))

print('Press enter twice to close!')
input()