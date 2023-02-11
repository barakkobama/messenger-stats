#Funcionalities:
#Done:
# - Message count
#To do:
# - Most used words in conversation
# - Most used words by each participants 
# - Reactions given count
# - Reactions recived count
# - Images sent count
# - 'XD' sent count
# - Directly addressed count (@name)
# - Avg message length
#Other to do things:
# - Allow to give path to folder messeges as an argument
# - Data visualisations
# - Ignore punctuation marks


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
    participantsList = []
    for person in data['participants']:
        participantsList.append(person['name'])
    return participantsList


#Retrun a dictionary with ammount of messeges sent by each person
#Takes data form one json file
def messagesCount(file):
    data = readFile(file)
    dictMsg = {key:0 for key in getParticipants(data)}
    for message in data['messages']:
        if message['sender_name'] in dictMsg.keys():      #If a person was deleted from a conversation
            dictMsg[message['sender_name']] +=1           #he wont show in participants but there still 
    return dictMsg                                        #will be messeges sent by him

#Counts all messenges sent by each person
def messagesCountAll():
    files = getFiles(MSG_FOLDER_NAME)
    dictCountAll = messagesCount(files.pop(0))
    counts = [messagesCount(file) for file in files]
    for count in counts:
        for key in count:
            dictCountAll[key] += count[key]
    return dictCountAll

#Returns a set of all unique words in a single file
def getWordsUsed(file):
    data = readFile(file)
    words = set()
    for message in data['messages']:
        if 'content' in message:                           #Stickers dont have 'content' field
            words.update(word.lower() for word in message['content'].split())
    return words


#Retruns a set of all unique words in all files
def getWordsUsedAll():
    files = getFiles(MSG_FOLDER_NAME)
    allWords = getWordsUsed(files.pop(0))
    for file in files:
        allWords = allWords | getWordsUsed(file)
    return allWords

#Retruns a list of 
def countWords():
    dictWords = {key:0 for key in getWordsUsedAll()}
    files = getFiles(MSG_FOLDER_NAME)
    for file in files:
        for message in readFile(file)['messages']:
            if 'content' in message:
                words = [word.lower() for word in message['content'].split()]
                for word in words:
                    dictWords[word] += 1
    return sorted(dictWords.items(), key=lambda x: x[1], reverse=True)






if __name__ == "__main__":
    count = countWords()
    for i in range (100):
        print(str(i) +"." + str(count[i]))