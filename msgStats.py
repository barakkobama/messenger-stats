#Funcionalities:
#Done:
# - Message count
# - Most used words in conversation
# - Reactions recived count
# - Reactions given count
# - Most reacted to message by each person
# - Images sent count
# - 'XD' sent count
#To do:
# - Directly addressed count (@name)
# - Most used words by each participant 
# - Avg message length
#Other to do things:
# - Allow to give path to folder messeges as an argument
# - Data visualisations
# - Ignore punctuation marks
# - Parse Polish symbols
# - Show info like time of creation
# - Allow to view by month/year
# - Allow to filter reactions
# - Maybe optimize so files are read once at the launch



import json
import os


MSG_FOLDER_NAME = 'messeges/'



#Reads json file
def readFile(fileName):
    file = open(MSG_FOLDER_NAME +'/'+fileName)
    data = json.load(file)
    file.close()
    return data

#Returns list of files in a folder
def getFiles(path):
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path,f))]
    return files


#Returns list of participants in a conversation
def getParticipants(data):
    participantslist = []
    for person in data['participants']:
        participantslist.append(person['name'])
    return participantslist


#Retrun a dictionary with ammount of messeges sent by each person
#Takes data form one json file
def countMessages(file):
    data = readFile(file)
    dictMsg = {key:0 for key in getParticipants(data)}
    for message in data['messages']:
        if message['sender_name'] in dictMsg.keys():      #If a person was deleted from a conversation
            dictMsg[message['sender_name']] +=1           #he wont show in participants but there still 
    return dictMsg                                        #will be messeges sent by him

#Counts all messenges sent by each person
def countMessagesAll(files):
    dictCountAll = countMessages(files.pop(0))
    counts = [countMessages(file) for file in files]
    for count in counts:
        for key in count:
            dictCountAll[key] += count[key]
    return sorted(dictCountAll.items(), key=lambda x: x[1], reverse=True)

#Returns a set of all unique words in a single file
def getWordsUsed(file):
    data = readFile(file)
    words = set()
    for message in data['messages']:
        if 'content' in message:                           #Stickers dont have 'content' field
            words.update(word.lower() for word in message['content'].split())
    return words


#Retruns a set of all unique words in all files
def getWordsUsedAll(files):
    allWords = getWordsUsed(files.pop(0))
    for file in files:
        allWords = allWords | getWordsUsed(file)
    return allWords

#Retruns a sorted list of words and the amout of times they were used
def countWords(files):
    dictWords = {key:0 for key in getWordsUsedAll(files)}
    for file in files:
        for message in readFile(file)['messages']:
            if 'content' in message:
                words = [word.lower() for word in message['content'].split()]
                for word in words:
                    dictWords[word] += 1
    return sorted(dictWords.items(), key=lambda x: x[1], reverse=True)

#Returns a dictionary with sum of reactions recived under all sent messages
def countReactionsRecived(file):
    data = readFile(file)
    dictReacts = {key:0 for key in getParticipants(data)}
    for message in data['messages']:
        if 'reactions' in message:                          #Messages without reactions dont have 'reactions' section
            dictReacts[message['sender_name']] += len(message['reactions'])
    return dictReacts


#Returns sorted list of participants and numbers of reactions under their messages
def countReactionsRecivedAll(files):
    dictReacts = countReactionsRecived(files.pop(0))
    for file in files:
        tempDict = countReactionsRecived(file)
        for key in dictReacts:
            dictReacts[key] += tempDict[key]
    return sorted(dictReacts.items(), key=lambda x: x[1], reverse=True)


#Returns a dictionary with sum of reactions given all sent messages
def countReactionsGiven(file):
    data = readFile(file)
    dictReacts = {key:0 for key in getParticipants(data)}
    for message in data['messages']:
        if 'reactions' in message:                          #Messages without reactions dont have 'reactions' section
            for reaction in message['reactions']:
                dictReacts[reaction['actor']] += 1
    return dictReacts
    
#Returns sorted list of participants and numbers of reactions left under messages
def countReactionsGivenAll(files):
    dictReacts = countReactionsGiven(files.pop(0))

    for file in files:
        tempDict = countReactionsGiven(file)
        for key in dictReacts:
            dictReacts[key] += tempDict[key]
    return sorted(dictReacts.items(), key=lambda x: x[1], reverse=True)

#Returns sorted list of participants, reactions recived, and the messege that recived the most reactions
def mostReactedToMessage(files):
    data = [readFile(file) for file in files]
    dictReacts = {key:[0,''] for key in getParticipants(data[0])}
    for file in data:
        for message in file['messages']:
            if 'reactions' in message:
                if len(message['reactions']) > dictReacts[message['sender_name']][0]:
                    dictReacts[message['sender_name']][0] = len(message['reactions'])
                    if 'content' in message:
                        dictReacts[message['sender_name']][1] = message['content']
                    elif 'videos' in message:
                        dictReacts[message['sender_name']][1] = message['videos'][0]['uri']
                    elif 'photos' in message:
                        dictReacts[message['sender_name']][1] = message['photos'][0]['uri']
                    else:
                        dictReacts[message['sender_name']][1] = 'unrecognised'
    return sorted(dictReacts.items(), key=lambda x: x[1][0], reverse=True)


#Retrun a dictionary with ammount of images and videos sent by each person
#Takes data form one json file
def mediaCount(file):
    data = readFile(file)
    dictMedia = {key:0 for key in getParticipants(data)}
    for message in data['messages']:
        if message['sender_name'] in dictMedia.keys():
            if 'videos' in message or 'photos' in message:   
                dictMedia[message['sender_name']] +=1          
    return dictMedia                                    

#Counts all images and videos sent by each person
def mediaCountAll(files):
    dictCountAll = mediaCount(files.pop(0))
    counts = [mediaCount(file) for file in files]
    for count in counts:
        for key in count:
            dictCountAll[key] += count[key]
    return sorted(dictCountAll.items(), key=lambda x: x[1], reverse=True)

#Counts all the times 'XD' was written by each participant
#Takes data form one json file
def XDCount(file):
    data = readFile(file)
    dictXD = {key:0 for key in getParticipants(data)}
    for message in data['messages']:
        if message['sender_name'] in dictXD.keys() and 'content' in message: 
            if 'xd' in message['content'].lower():
                dictXD[message['sender_name']] +=1
    return dictXD        

#Counts all the times 'XD' was written by each participant in whole conversation
def XDCountAll(files):
    dictCountAll = XDCount(files.pop(0))
    counts = [XDCount(file) for file in files]
    for count in counts:
        for key in count:
            dictCountAll[key] += count[key]
    return sorted(dictCountAll.items(), key=lambda x: x[1], reverse=True)

#Counts summaric length of every message send by each participant
#Takes data form one json file
def messageLen(file):
    data = readFile(file)
    dictLen = {key:0 for key in getParticipants(data)}
    for message in data['messages']:
        if message['sender_name'] in dictLen.keys() and 'content' in message: 
            dictLen[message['sender_name']] += len(message['constent'])
    return dictLen       

#Counts summaric length of every message each participant in whole conversation
def messageLenAll(files):
    dictLenAll = messageLen(files.pop(0))
    counts = [messageLen(file) for file in files]
    for count in counts:
        for key in count:
            dictLenAll[key] += count[key]
    return sorted(dictLenAll.items(), key=lambda x: x[1], reverse=True)

def main():
    files = getFiles(MSG_FOLDER_NAME)
    participants = getParticipants(readFile(files[0]))
    msgCount = countMessagesAll(files)
    wordsUsed = countWords(files)
    reactionsRecived = []
    reactionsGiven = []
    mostReactedToMessage = []
    mediaSent = []
    xdCount = []
    msgLen = []
    print(msgCount)
    print(wordsUsed[0:10])










if __name__ == "__main__":
    main()