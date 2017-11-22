import http.client, urllib.request, urllib.parse, urllib.error, base64, requests, json

from configuration import *
from imagePil import *
import math
import time

lastCall = 0
def apiCall(method, url, body, headers):
    global lastCall
    # make sure maximum rate isn't exceeded
    currentTime = time.time()
    delay = lastCall + 3.1 - currentTime
    if delay > 0:
        time.sleep(delay)
    lastCall = currentTime

    headers ['Ocp-Apim-Subscription-Key'] = subscription_key
    try:
        conn = http.client.HTTPSConnection(subscription_base)
        conn.request(method, url, body, headers)
        response = conn.getresponse()
        data = response.read()
        return data
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

def listPersons(personGroupId):
    params = urllib.parse.urlencode({
        # Request parameters
        # 'start': '{string}',
        # 'top': '1000',
    })
    data = apiCall("GET", "/face/v1.0/persongroups/" + personGroupId + "/persons?%s" % params, "{body}", {})
    return json.loads(data.decode('utf8'))

def listPersonGroups():
    params = urllib.parse.urlencode({
        # Request parameters
        # 'start': '{string}',
        # 'top': '1000',
    })
    data = apiCall("GET", "/face/v1.0/persongroups?%s" % params, "{body}", {})
    return json.loads(data.decode('utf8'))

def checkJson(parsed):
    print (parsed)
    if len(parsed) == 0 or 'error' in parsed:
        # no faces detected or error
        print("Sorry. Something went wrong. Please try again.")
        return None
    return parsed

def detect(img):
    headers = {
        'Content-Type': 'application/octet-stream',
    }
    params = urllib.parse.urlencode({
        'returnFaceId': 'true',
        'returnFaceLandmarks': 'false',
        # 'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
    })
    # Execute the REST API call and get the response.
    data = apiCall('POST', "/face/v1.0/detect?%s" % params, img, headers)
    return checkJson(json.loads(data.decode('utf8')))

def checkTrainingStatus():
    params = urllib.parse.urlencode({
    })
    ans = False
    data = apiCall("GET", "/face/v1.0/persongroups/" + personGroupId + "/training?%s" % params, "", {})
    parsed = checkJson(json.loads(data.decode('utf8')))
    if parsed != None and parsed['status'] == 'succeeded':
        ans = True
    return ans

def waitForTraining():
    while checkTrainingStatus() == False:
        # still training
        time.sleep(.2)

def train():
    params = urllib.parse.urlencode({
    })
    data = apiCall("POST", "/face/v1.0/persongroups/" + personGroupId + "/train?%s" % params, "", {})
    return data

def identify(faceIds, personGroupId):
    waitForTraining();
    headers = {
        'Content-Type': 'application/json',
    }
    params = urllib.parse.urlencode({
    })
    body = json.dumps({
        'faceIds': faceIds,
        'personGroupId': personGroupId,
        # 'maxNumOfCandidatesReturned': 1,
        'confidenceThreshold': 0,
    })
    data = apiCall("POST", "/face/v1.0/identify?%s" % params, body, headers)
    ans = checkJson(json.loads(data.decode('utf8')))
    return ans

def createPersonGroup(id, name):
    headers = {
        'Content-Type': 'application/json',
    }
    body = json.dumps({'name': name})
    data = apiCall("PUT", "/face/v1.0/persongroups/" + id, "", headers)
    return data

def deletePersonGroup(id):
    data = apiCall("DELETE", "/face/v1.0/persongroups/" + id, "", headers)
    print(data)

def addFace(filename, bounds, personId, personGroupId):
    headers = {
        'Content-Type': 'application/octet-stream',
    }
    params = urllib.parse.urlencode({
        # Request parameters
        # 'userData': '{string}',
        'targetFace': "%d,%d,%d,%d" % (bounds[0], bounds[1], bounds[2], bounds[3]),
    })
    img = getImage(filename)
    data = apiCall("POST", "/face/v1.0/persongroups/" + personGroupId +"/persons/" + personId + "/persistedFaces?%s" % params, img, headers)
    print(data)

def createPerson(personGroupId, name):
    headers = {
        'Content-Type': 'application/json',
    }
    params = urllib.parse.urlencode({
    })
    data = json.dumps({'name': name})
    ans = None
    data = apiCall("POST", "/face/v1.0/persongroups/" + personGroupId + "/persons?%s" % params, data, headers)
    ans = checkJson(json.loads(data.decode('utf8')))
    if ans != None:
        ans = ans['personId']
    return ans

def deletePerson(personGroupId, personId):
    params = urllib.parse.urlencode({
    })
    data = apiCall("DELETE", "/face/v1.0/persongroups/" + personGroupId + "/persons/" + personId + "?%s" % params, "", {})
