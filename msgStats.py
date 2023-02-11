import json
import os


MSG_FOLDER_NAME = 'messeges'

#Reads json file
def readFile(fileName):
    file = open(MSG_FOLDER_NAME +'/'+fileName)
    data = json.load(file)
    file.close()
    return data

#Returns number of files in a folder
def getFilesNum(path):
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path,f))]
    return len(files)

#Returns list of participants in a conversation
def getParticipants(data):
    participantsList = []
    for person in data['participants']:
        participantsList.append(person['name'])
    return participantsList


if __name__ == "__main__":
    data = readFile("message_1.json")
    print(getParticipants(data))