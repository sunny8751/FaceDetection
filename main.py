from configuration import SUBSCRIPTION_KEY, SUBSCRIPTION_BASE, FRAME_PROCESS_RATE, THRESHOLD, PERSON_GROUP_ID
import cognitive_face_wrapper.face as CF_face
import cognitive_face_wrapper.face_list as CF_face_list
import cognitive_face_wrapper.person as CF_person
import cognitive_face_wrapper.person_group as CF_person_group
import graphics
import util
from util import Person
from util import people as peopleDirectory

import math

def associateFacesToNewPeople(faceIds):
    print ("Unidentified people:", len(faceIds))
    # use each face id to create new Person
    for faceId in faceIds:
        name = 'Person' + str(len(peopleDirectory)) # not necessarily unique
        userData = ''
        personId = CF_person.create(PERSON_GROUP_ID, name, user_data=userData)['personId']
        newPerson = Person(personId, name, userData)
        newPerson.addFaceId(faceId)

        peopleDirectory[personId] = newPerson

    # train the model
    CF_person_group.train(PERSON_GROUP_ID)

# TODO make failure propogate upwards
def waitForTraining():
    statusOutput = CF_person_group.get_status(PERSON_GROUP_ID)
    status = statusOutput['status']
    while status != 'succeeded':
        if status == 'failed':
            print (statusOutput['message'])
            return
        # still training
        time.sleep(.2)

# param faceIds to identify
# return unidentified faceIds
def identifyFacesToExistingPeople(faceIds):
    # no people to identify to
    if len(peopleDirectory) == 0:
        return faceIds

    # wait for training to be done
    waitForTraining()

    unidentified = []

    numIdentified = 0
    # partition the list of face ids into 10 bc that's the max for the API call
    while numIdentified < len(faceIds):
        # subset of 10 face ids
        subset = faceIds[numIdentified:numIdentified + 10]

        # identify the faces
        identifyOutput = CF_face.identify(subset, PERSON_GROUP_ID)
        for faceInfo in identifyOutput:
            faceId = faceInfo['faceId']
            if len(faceInfo['candidates']) == 0:
                # no candidates found
                unidentified.append(faceId)
                continue
            candidateId = faceInfo['candidates'][0]['personId']
            confidence = faceInfo['candidates'][0]['confidence']
            if confidence >= THRESHOLD:
                # this face belongs to the candidate!
                candidate = peopleDirectory[candidateId]
                candidate.addFaceId(faceId)
            else:
                unidentified.append(faceId)

        numIdentified += 10

    return unidentified

# detects faces in the frame and returns them.
# draws rectangles around detected faces
# param frame image to detect
# return faceIds that were detected
def drawAndDetectFaces(frame):
    # convert from cv2 image to python file object
    frameBin = graphics.convertToBinary(frame)
    # detect the faces in the frame
    detectOutput = CF_face.detect(frameBin)

    faceIds = []
    # go through each detected face and draw rect around face
    for faceInfo in detectOutput:
        faceId = faceInfo['faceId']
        # add the face id
        faceIds.append(faceId)
        # get the face's bounds
        rect = faceInfo['faceRectangle']
        bounds = (rect['left'], rect['top'], rect['width'], rect['height'])
        graphics.saveFaceImage(faceId + '.jpg', graphics.cropImage(frame, bounds))
        # draw rectangle around the face
        graphics.drawRect(frame, bounds)
    return faceIds

def processFrame(frame, frameCount, frameRate):
    # offset frame count by 1 to process the first frame
    frameCount -= 1
    # only process one frame/second
    if frameCount % (math.floor(frameRate)) != 0:
        return
    numSecs = (frameCount // math.floor(frameRate))
    if  numSecs % FRAME_PROCESS_RATE != 0:
        # just show the frame but don't process it
        graphics.showImage(frame)
        return

    faceIds = drawAndDetectFaces(frame)
    graphics.showImage(frame)

    unidentified = identifyFacesToExistingPeople(faceIds)
    associateFacesToNewPeople(unidentified)

# load information into local memory from azure
def load():
    # load people in person group
    peopleListOutput = CF_person.lists(PERSON_GROUP_ID)
    for personInfo in peopleListOutput:
        personId = personInfo['personId']
        name = personInfo['name']
        userData = personInfo['userData']
        persistedFaceIds = personInfo['persistedFaceIds']
        # add a new Person to the directory
        newPerson = Person(personId, name, userData)
        newPerson.setPersistedFaceIds(persistedFaceIds)
        peopleDirectory[personId] = newPerson
    print ("Loaded %d people into directory" % len(peopleDirectory))

def deleteAllPeople():
    # get list of people
    peopleListOutput = CF_person.lists(PERSON_GROUP_ID)
    # delete each person
    for personInfo in peopleListOutput:
        personId = personInfo['personId']
        CF_person.delete(PERSON_GROUP_ID, personId)
    print ('Deleted all people from azure database')

    # delete saved images
    import os
    from configuration import FACE_FOLDER, PERSISTED_FACE_FOLDER
    for filename in os.listdir(FACE_FOLDER):
        os.remove(FACE_FOLDER + filename)
    for filename in os.listdir(PERSISTED_FACE_FOLDER):
        os.remove(PERSISTED_FACE_FOLDER + filename)
    print ('Deleted all saved images of faces and persisted faces')

if __name__ == "__main__":
    import cognitive_face as CF
    CF.Key.set(SUBSCRIPTION_KEY)
    CF.BaseUrl.set(SUBSCRIPTION_BASE)

    # deleteAllPeople();

    load()
    CF_person_group.train(PERSON_GROUP_ID)
    graphics.processVideo("video.mp4", processFrame)
