import requests
import json
import sys
import getopt
import pprint




iiSHost = 'http://prod.localhost/JAMS/api'
headers = {'content-type': 'application/json', 'Accept': 'application/json' }

class Job:
    def __init__(self, jobName, parentFolderName, methodName):
        self.jobName = jobName
        self.parentFolderName = parentFolderName
        self.methodName = methodName
        self.elements = []

    def updateElements(self, element):
        self.elements.append(element)

class Element:
    def __init__(self, elementKind, elementTypeName, elementState):
        self.elementKind = elementKind
        self.elementTypeName = elementTypeName
        self.elementState = elementState
        self.properties = []
    
    def updateProperties(self,property):
        self.properties.append(property)

class ElementProperty:
    def __init__(self, categoryName, propertyName, currentValue):
        self.categoryName = categoryName
        self.propertyName = propertyName
        self.currentValue = currentValue




def jobDefinition(jobName, folder, method):
    return {
        'jobName' : jobName,
        'parentFolderName': folder,
        'methodName': method,
        'elements': '[]'
    }

def scheduleDateDefinition(scheduledDate):
    return {
        'elementTypeName': 'ScheduleTrigger',
        'properties': "[ { 'currentValue': {" + scheduledDate + "} }]"
    }

def getSchedule():
    url = '{}/element/properties/ScheduleTrigger'.format(iiSHost)
    response = requests.get(url, headers=headers)
    return json.loads(response.text)

def getAJob(jobName):
    url = '{}/job?name={}'.format(iiSHost, jobName)
    response = requests.get(url, headers=headers)
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(response.json())

def putJob(job):
    url = '{}/job'.format(iiSHost)
    return requests.post(url, data=json.dumps(job), headers=headers)

def login(username, password):
    url = '{}/authentication/login'.format(iiSHost)
    payload = {
              "username": '{}'.format(username),
              "password": '{}'.format(password)
             }

    response = requests.post(url, data=json.dumps(payload), headers=headers)
    if response == None or response.status_code != 200:
        print('Failed to login')
        sys.exit(2)
    mydict = response.json()
    return mydict.get("access_token")

def main(argv):

    username = ''
    password = ''
    try:
        opts, args = getopt.getopt(argv, "hu:p:", ["username=","password="])
    except getopt.GetoptError:
        print( 'auth.py -u <username> -p <password>')
        sys.exit(2)

    for opt,arg in opts:
        if opt in ("-u", "--username"):
            username = arg
        elif opt in ("-p", "--password"):
            password = arg

    access_token = login(username, password)
    headers.update({'Authorization': 'Bearer {}'.format(access_token)})

    sampleJob = jobDefinition("NewJob", "\\Demonstrations","SSH")
    schedDate = scheduleDateDefinition('1st workday of month')
    sampleJob['elements'] = '[{}]'.format(schedDate)

    print(sampleJob)

    response = putJob(sampleJob)
    if response.status_code != 201:
        print('Failed to create job. Error is: {}/{}'.format(response.status_code, response.text)) 
        sys.exit(1)
    else:
        print('Successfully created job')



if __name__ == "__main__":
    main(sys.argv[1:])

