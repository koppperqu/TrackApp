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
    if(eventName=='Weight Throw'):
        for index,eachHighestMark in enumerate(highestMarks):
            if(eachHighestMark>float(WeightPRS[prRow[index]])):
                print ('PR!! OLD MARK '+ WeightPRS[prRow[index]]+' new mark ' + str(eachHighestMark) + ' for ' + namesInput[index])
                WeightPRS[prRow[index]]=eachHighestMark
    if(eventName=='Hammer'):
        for index,eachHighestMark in enumerate(highestMarks):
            if(eachHighestMark>float(HammerPRS[prRow[index]])):
                print ('PR!! OLD MARK '+ HammerPRS[prRow[index]]+' new mark ' + str(eachHighestMark) + ' for ' + namesInput[index])
                HammerPRS[prRow[index]]=eachHighestMark
    if(eventName=='Discus'):
        for index,eachHighestMark in enumerate(highestMarks):
            if(eachHighestMark>float(DiscusPRS[prRow[index]])):
                print ('PR!! OLD MARK '+ DiscusPRS[prRow[index]]+' new mark ' + str(eachHighestMark) + ' for ' + namesInput[index])
                DiscusPRS[prRow[index]]=eachHighestMark
    for index,eachName in enumerate(Names):
        pr.write('\n'+Names[index]+','+str(WeightPRS[index])+','+str(ShotPRS[index])+','+str(HammerPRS[index])+','+str(DiscusPRS[index]))
    pr.close()

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

# pointerResults=PointerResults(womenShotURL)
# results=GetHighestMarksAndThrowNumber(pointerResults[1])
# ResultsAndIfPersonalRecord(pointerResults[0],results[0],'Weight Throw')
# pointerResults=PointerResults(menShotURL)
# results=GetHighestMarksAndThrowNumber(pointerResults[1])
# ResultsAndIfPersonalRecord(pointerResults[0],results[0],'Shot Put')



print('\nMen Shot Put \n------------------------------------------')
pointerResults=PointerResults(menShotURL)
results=GetHighestMarksAndThrowNumber(pointerResults[1])
ResultsAndIfPersonalRecord(pointerResults[0],results[0],'Shot Put')
print('\nMen Weight Throw \n------------------------------------------')
pointerResults=PointerResults(menWeightURL)
results=GetHighestMarksAndThrowNumber(pointerResults[1])
ResultsAndIfPersonalRecord(pointerResults[0],results[0],'Weight Throw')
print('\nMen Hammer \n------------------------------------------')
print(PointerResults(menDiscusURL))
print('\nMen Discus \n------------------------------------------')
print(PointerResults(menHammerURL))

print('\nWomen Shot Put \n------------------------------------------')
pointerResults=PointerResults(womenShotURL)
results=GetHighestMarksAndThrowNumber(pointerResults[1])
ResultsAndIfPersonalRecord(pointerResults[0],results[0],'Shot Put')
print('\nWomen Weight Throw \n------------------------------------------')
pointerResults=PointerResults(womenWeightURL)
results=GetHighestMarksAndThrowNumber(pointerResults[1])
ResultsAndIfPersonalRecord(pointerResults[0],results[0],'Weight Throw')
print('\nWomen Hammer \n------------------------------------------')
print(PointerResults(womenDiscusURL))
print('\nWomen Discus \n------------------------------------------')
print(PointerResults(womenHammerURL))

       #find round might be uselfule later if not delete
       #round = eachNameRow.find(class_=True).attrs['class'][0]
       #it was usefull good job me :)

#Prints who threw what mark on what throw (for testing)
# a=0
# for i in names:
    # print(names[a], " threw ", highestmarks[a], " on throw ", thrownumbers[a])
    # a=a+1

# import csv
# with open (r"C:\Users\akopp\TrackApp\track\pr.txt", 'r') as f:
    # prs = [row[0] for row in csv.reader(f,delimiter='\t')]
    # prs= (prs[1:])#Gets rid of first row without name or someones pr's
# #Goes through prs to first find person whoes highest mark is getting analyzed(search by last name with contains)
# #Puts the correct index (right name) from prs into a new temp array of marks that go WEIGHT,SHOT,HAMMER,DISCUS
# #Depending on what event is being analyzed for to index 0-3 to check if that number is smaller than the higest mark at the meet
# #If it is it will print a symbol(*) next to the number in the results page to symbolize a pr
# #if not just print number normally (might change to only do pr's)
# #Print event name (ie mens weight) then under Name and distance thrown do for all events put in results file.
# for eachName in names:
    # print(eachName)
    # for eachPr in prs:
input()