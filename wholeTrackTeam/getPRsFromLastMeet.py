#This file will ask user if they want the most recent track meet results or if they want to enter in a meet manualy
#in the event a meet took place and this file was not executed
response=input('Do you want PR\'s from the most recent track meet? (y/n): ')
#n
Y              # FOR TESTING IN CMD comment out for running the file to work
correctResponse=False
validResponses=['y','n','Y','N']
while not correctResponse:
    for eachValidResponse in validResponses:
        if response==eachValidResponse:
            correctResponse=True
    if not correctResponse:
        response=input ('please enter valid answer y or n: ')

response=response.lower()
if response =='y':
    url = 'https://www.tfrrs.org/teams/WI_college_m_Wis_Stevens_Point.html'

if response =='n':
    url = input('Please go to the meet you would like to get the PR\'s from and paste the URL here ')
    goodURL=False
    while not goodURL:
        if 'https://www.tfrrs.org' not in url:
            url = input('Please paste a valid TFRRS link -> ')
        else:
            goodURL=True

print ('Getting PR\'s from most recent results')
print (url)





input('Press Enter to Close')