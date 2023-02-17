#Funcionalities:
#Done:
# - Message count
# - Most used words in conversation
# - Reactions recived count
# - Reactions given count
# - Most reacted to message by each person
# - Images sent count
# - Specific word sent count
# - Date of first sent message
# - Account for symbols and emojis
# - Avg message length
# - Directly addressed count (@name) - use count specific word
# - Frequency of given word ocurrence
# - Proportion of reactions recived to messeges sent
# - Allow to chose specific reaction
#To do:
# - Most used words by each participant 
#Other to do things:
# - Allow to give path to folder messeges as an argument
# - Allow to view by month/year
# - Data visualisation
#Optimalisatio ideas:
# - Load all the files at the start [DONE]
# - Convert functions to work on "data" not "file" [DONE]
# - "Fix" all the data before processing [DONE]



import datetime
import json
import os
from ftfy import fix_text

MSG_FOLDER_NAME = 'messeges'

#REACTIONS
THUMBS_UP = '👍'
HEART = '❤'
HAHA = '😆'
WOW = '😮'
THUMBS_DOWN = '👎'
CLOWN = '🤡'



#Reads json file
def readFile(fileName):
    file = open(MSG_FOLDER_NAME +'/'+fileName)
    data = json.load(file)
    file.close()
    return data

#Helper function that returns the number from file name
#Used for sorting
def customSort(file_name):
    prefix, number = file_name.split("_")[0], int(file_name.split("_")[1].split(".")[0])
    return number


#Returns list of sorted files in a folder
def getFiles(path):
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path,f))]
    return sorted(files, key=customSort)

#Function that reads unicodes in data
#Works for emojis and symbols
def fixData(data):
    for i in range(len(data['participants'])):
        data['participants'][i]['name'] = fix_text(data['participants'][i]['name'])
    for i in range(len(data['messages'])):
        data['messages'][i]['sender_name'] = fix_text(data['messages'][i]['sender_name'])
        if 'content' in data['messages'][i]:
            data['messages'][i]['content'] = fix_text(data['messages'][i]['content'])
        if 'reactions' in data['messages'][i]:
            for j in range(len(data['messages'][i]['reactions'])):
                data['messages'][i]['reactions'][j]['reaction'] = fix_text(data['messages'][i]['reactions'][j]['reaction'])
                data['messages'][i]['reactions'][j]['actor'] = fix_text(data['messages'][i]['reactions'][j]['actor'])
    return data


#Returns name of the conversation
def getGroupName(data):
    return data['title']



#Returns list of participants in a conversation
def getParticipants(data,dictForm = False):
    participantslist = []
    for person in data['participants']:
        participantslist.append(person['name'])
    if dictForm:
        return {key:0 for key in participantslist}
    return participantslist


#Retrun a dictionary with ammount of messeges sent by each person
#Takes data form one json file
def countMessages(data):
    dictMsg = getParticipants(data,dictForm=True)
    for message in data['messages']:
        if message['sender_name'] in dictMsg.keys():      #If a person was deleted from a conversation
            dictMsg[message['sender_name']] +=1           #he wont show in participants but there still 
    return dictMsg                                        #will be messeges sent by him

#Counts all messenges sent by each person
def countMessagesAll(dataAll,sort = True):
    dictCountAll = getParticipants(dataAll[0],dictForm=True)
    counts = [countMessages(data) for data in dataAll]
    for count in counts:
        for key in count:
            dictCountAll[key] += count[key]
    if sort:
        return sorted(dictCountAll.items(), key=lambda x: x[1], reverse=True)
    return dictCountAll

#Returns a set of all unique words in a single file
def getWordsUsed(data):
    words = set()
    for message in data['messages']:
        if 'content' in message:                           #Stickers dont have 'content' field
            words.update(word.lower() for word in message['content'].split())
    return words


#Retruns a set of all unique words in all files
def getWordsUsedAll(dataAll):
    allWords = set()
    for data in dataAll:
        allWords = allWords | getWordsUsed(data)
    return allWords

#Retruns a sorted list of words and the amout of times they were used
def countWords(dataAll,sort = True,range = 10):
    dictWords = {key:0 for key in getWordsUsedAll(dataAll)}
    for data in dataAll:
        for message in data['messages']:
            if 'content' in message:
                words = [word.lower() for word in message['content'].split()]
                for word in words:
                    dictWords[word] += 1
    if sort:
        return sorted(dictWords.items(), key=lambda x: x[1], reverse=True)[0:range]
    return dictWords

#Returns a dictionary with sum of reactions recived under all sent messages
def countReactionsRecived(data,whatReaction = 'all'):
    dictReacts = getParticipants(data,dictForm=True)
    for message in data['messages']:
        if 'reactions' in message:                          #Messages without reactions dont have 'reactions' section
            if whatReaction == 'all':
                dictReacts[message['sender_name']] += len(message['reactions'])
            else:
                for reaction in message['reactions']:
                    if reaction['reaction'] == whatReaction:
                        dictReacts[message['sender_name']] += 1

    return dictReacts


#Returns sorted list of participants and numbers of reactions under their messages
def countReactionsRecivedAll(dataAll,whatReaction = 'all',sort = True):
    dictReacts = countReactionsRecived(dataAll[0],whatReaction)
    for data in dataAll:
        tempDict = countReactionsRecived(data,whatReaction)
        for key in dictReacts:
            dictReacts[key] += tempDict[key]
    if sort:
        return sorted(dictReacts.items(), key=lambda x: x[1], reverse=True)
    return dictReacts


#Returns a dictionary with sum of reactions given all sent messages
def countReactionsGiven(data,whatReaction = 'all'):
    dictReacts = getParticipants(data,dictForm=True)
    for message in data['messages']:
        if 'reactions' in message:
            if whatReaction == 'all':                    #Messages without reactions dont have 'reactions' section
                for reaction in message['reactions']:
                    dictReacts[reaction['actor']] += 1
            else:
                for reaction in message['reactions']:
                    if reaction['reaction'] == whatReaction:
                        dictReacts[reaction['actor']] += 1
    return dictReacts
    
#Returns sorted list of participants and numbers of reactions left under messages
def countReactionsGivenAll(dataAll,whatReaction='all',sort = True):
    dictReacts = getParticipants(dataAll[0],dictForm=True)

    for data in dataAll:
        tempDict = countReactionsGiven(data,whatReaction)
        for key in dictReacts:
            dictReacts[key] += tempDict[key]
    if sort:
        return sorted(dictReacts.items(), key=lambda x: x[1], reverse=True)
    return dictReacts

#Returns sorted list of participants, reactions recived, and the messege that recived the most reactions
def mostReactedToMessage(dataAll,whatReaction ='all',sort = True):
    dictReacts = {key:[0,''] for key in getParticipants(dataAll[0])}
    for data in dataAll:
        for message in data['messages']:
            if 'reactions' in message:
                if whatReaction == 'all':
                    reactionCount = len(message['reactions'])
                else:
                    reactionCount = 0
                    for reaction in  message['reactions']:
                        if reaction['reaction'] == whatReaction:
                            reactionCount+=1
                if reactionCount > dictReacts[message['sender_name']][0]:
                        dictReacts[message['sender_name']][0] = reactionCount
                        if 'content' in message:
                            dictReacts[message['sender_name']][1] = message['content']
                        elif 'videos' in message:
                            dictReacts[message['sender_name']][1] = message['videos'][0]['uri']
                        elif 'photos' in message:
                            dictReacts[message['sender_name']][1] = message['photos'][0]['uri']
                        else:
                            dictReacts[message['sender_name']][1] = 'unrecognised'
    if sort:
        return sorted(dictReacts.items(), key=lambda x: x[1][0], reverse=True)
    return dictReacts


#Retrun a dictionary with ammount of images and videos sent by each person
#Takes data form one json file
def countMedia(data):
    dictMedia = getParticipants(data,dictForm=True)
    for message in data['messages']:
        if message['sender_name'] in dictMedia.keys():
            if 'videos' in message or 'photos' in message:   
                dictMedia[message['sender_name']] +=1          
    return dictMedia                                    

#Counts all images and videos sent by each person
def countMediaAll(dataAll,sort=True):
    dictCountAll = getParticipants(dataAll[0],dictForm=True)
    counts = [countMedia(data) for data in dataAll]
    for count in counts:
        for key in count:
            dictCountAll[key] += count[key]
    if sort:
        return sorted(dictCountAll.items(), key=lambda x: x[1], reverse=True)
    return dictCountAll

#Counts all the times word given as an argument was written by each participant
#Takes data form one json file
def countGivenWord(data,word):
    dictWord = getParticipants(data,dictForm=True)
    for message in data['messages']:
        if message['sender_name'] in dictWord.keys() and 'content' in message: 
            if word in message['content'].lower():
                dictWord[message['sender_name']] +=1
    return dictWord       

#Counts all the times word given as an argument was written by each participant in whole conversation
def countGivenWordAll(dataAll,word,sort = True):
    dictCountAll = getParticipants(dataAll[0],dictForm=True)
    counts = [countGivenWord(data,word) for data in dataAll]
    for count in counts:
        for key in count:
            dictCountAll[key] += count[key]
    if sort:
        return sorted(dictCountAll.items(), key=lambda x: x[1], reverse=True)
    return dictCountAll

#Counts summaric length of every message send by each participant
#Takes data form one json file
def countMessageLen(data):
    dictLen = getParticipants(data,dictForm=True)
    for message in data['messages']:
        if message['sender_name'] in dictLen.keys() and 'content' in message: 
            dictLen[message['sender_name']] += len(message['content'])
    return dictLen       

#Counts summaric length of every message each participant in whole conversation
def countMessageLenAll(dataAll,sort = True):
    dictLenAll = getParticipants(dataAll[0],dictForm=True)
    counts = [countMessageLen(data) for data in dataAll]
    for count in counts:
        for key in count:
            dictLenAll[key] += count[key]
    if sort:
        return sorted(dictLenAll.items(), key=lambda x: x[1], reverse=True)
    return dictLenAll

#Returns the date of the first send message
def getFirstMsgDate(dataAll):
    data = dataAll[len(dataAll)-1]
    firstMsgMs = data['messages'][len(data['messages'])-1]['timestamp_ms']
    firstMsgUnixUDT = int(firstMsgMs/1000)
    return datetime.datetime.fromtimestamp(firstMsgUnixUDT).strftime('%d-%m-%Y %H:%M:%S')

#Returns the avrage message length for each participant
def countAvgMessageLen(dataAll,sort = True):
    msgLen = countMessageLenAll(dataAll,False)
    msgAmmount = countMessagesAll(dataAll,False)
    dictAvgLen = getParticipants(dataAll[0],dictForm=True)
    i = 0
    for key in dictAvgLen.keys():
        dictAvgLen[key] = round(msgLen[key]/msgAmmount[key],3)
        i+=1
    if sort:
        return sorted(dictAvgLen.items(), key=lambda x: x[1], reverse=True)
    return dictAvgLen

#Retruns the procentage of how many messeges contain a given word
def countWordFreq(dataAll,word,sort=True):
    wordCount = countGivenWordAll(dataAll,word,False)
    msgAmmount = countMessagesAll(dataAll,False)
    dictWordFreq = getParticipants(dataAll[0],dictForm=True)
    i = 0
    for key in dictWordFreq.keys():
        dictWordFreq[key] = round(wordCount[key]/msgAmmount[key],4)*100
        i+=1
    if sort:
        return sorted(dictWordFreq.items(), key=lambda x: x[1], reverse=True)
    return dictWordFreq

#Returns proportions of reactions recived/messeges sent
def countReactionProp(dataAll,whatReaction = 'all',sort=True):
    msgAmmount = countMessagesAll(dataAll,False)
    reactAmmount = countReactionsRecivedAll(dataAll,whatReaction,sort = False)
    dictReactProp =  getParticipants(dataAll[0],dictForm=True)
    i = 0
    for key in dictReactProp.keys():
        dictReactProp[key] = round(reactAmmount[key]/msgAmmount[key],4)*100
        i+=1
    if sort:
        return sorted(dictReactProp.items(), key=lambda x: x[1], reverse=True)
    return dictReactProp





#def main():
  #  ...
    #files = getFiles(MSG_FOLDER_NAME)
    #dataAll = [fixData(readFile(file)) for file in files]  #takes a long time to finish



    #dataAll = [readFile(file) for file in files]

    #Testing
    #print("------------Message Count------------")
    #msgCount = countMessagesAll(dataAll,False)
    #vis.plot_pie_chart(msgCount,"Messages sent")
    #vis.plot_bar_chart(msgCount,"Messages sent")
    #print(msgCount)

    #print("------------Most used words------------")
    #wordsUsed = countWords(dataAll)
    #for i in range (100):
    #    print(str(i)+"."+str(wordsUsed[i]))

    #print("------------First message date------------")
    #creationDate = getFirstMsgDate(dataAll)
    #print(creationDate)

    #print("------------Reactions recived------------")
    #reactionsRecived = countReactionsRecivedAll(dataAll)
    #print(reactionsRecived)

    #print("------------Reactions given------------")
    #reactionsGiven = countReactionsGivenAll(dataAll)    
    #print(reactionsGiven)

    #print("------------Most reacted to message------------")
    #mostReactedTo = mostReactedToMessage(dataAll)
    #print(mostReactedTo)

    #print("------------Media sent------------")
    #mediaSent = countMediaAll(dataAll)
    #print(mediaSent)

    #print("------------Word Conut - 'xd' ------------")
    #wordCount = countGivenWordAll(dataAll,'xd')
    #print(wordCount)


    #print("----------Sumaric length of all messages--------")
    #msgLen = countMessageLenAll(dataAll)
    #print(msgLen)

    #print("----------Avrage message length----------------")
    #avgLen = countAvgMessageLen(dataAll)
    #print(avgLen)

    #print("------Word ocurrence frequency- Kurwa--------------")
    #wordFreq = countWordFreq(dataAll,'kurw')
    #print(wordFreq)

   # print("-------Reaction recived to messeges sent proporction--------")
    #reactProp = countReactionProp(dataAll)
    #print(reactProp)

    #print("-----------Reaction count: HAHA-----------------------")
    #reactCount = countReactionsRecivedAll(dataAll,HAHA)
    #print(reactCount)

    #print("-----------Reaction count: HAHA-----------------------")
    #reactCount = countReactionsRecivedAll(dataAll,HAHA)
    #print(reactCount)

    
    #print("-------Reaction HAHA recived to messeges sent proporction--------")
    #reactProp = countReactionProp(dataAll,HAHA)
    #print(reactProp)


    #print("-------Reaction HEART recived to messeges sent proporction--------")
    #reactProp = countReactionProp(dataAll,HEART)
    #print(reactProp)

    #print("-----------Reaction count: WOW-----------------------")
    #reactCount = countReactionsRecivedAll(dataAll,WOW)
    #print(reactCount)

    #print("-------Most HAHA reacts message----------------")
    #mostHAHAto = mostReactedToMessage(dataAll,whatReaction=HAHA)
    #print(mostHAHAto)