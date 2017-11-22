from faceApi import *
from imagePil import *
from database import *

import cv2


def printPeople():
    personGroups = listPersonGroups()
    for personGroup in personGroups:
        personGroupId = personGroup['personGroupId']
        people = listPersons(personGroupId)
        print (personGroupId.upper())
        for person in people:
            print ("name: " + person['name'])
            print ("personId: " + person['personId'])
            print ("faceIds: " + str(person['persistedFaceIds']))
            print()

def deleteAllPeople():
    personGroups = listPersonGroups()
    for personGroup in personGroups:
        personGroupId = personGroup['personGroupId']
        people = listPersons(personGroupId)
        for person in people:
            deletePerson(personGroupId, person['personId'])
    print("All people are deleted")

def processVideo(filename, directory, personGroupId):
    cap = cv2.VideoCapture("data/" + filename)
    while not cap.isOpened():
        cap = cv2.VideoCapture("data/" + filename)
        cv2.waitKey(1000)
        print ("Wait for the header")

    frameRate = cap.get(5)

    pos_frame = cap.get(cv2.CAP_PROP_POS_FRAMES)
    while True:
        flag, frame = cap.read()
        if flag:
            # The frame is ready and already captured
            pos_frame = cap.get(cv2.CAP_PROP_POS_FRAMES)

            if pos_frame % (math.floor(frameRate)) == 0:
                # process the frame every second
                # cv2.imshow('video', frame)
                # print (str(pos_frame)+" frames")

                # save frame to tmp file
                # cv2.imwrite('data/tmp.jpg', frame)
                # processFrame('tmp.jpg', directory, personGroupId)
                # identifyFrame('tmp.jpg')
                identifyFrame(frame)
        else:
            # The next frame is not ready, so we try to read it again
            cap.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, pos_frame-1)
            print ("frame is not ready")
            # It is better to wait for a while for the next frame to be ready
            cv2.waitKey(1000)

        if cv2.waitKey(10) == 27:
            break
        if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
            # If the number of captured frames is equal to the total number of frames,
            # we stop
            break

    # img = openImage(filename)
    # # To iterate through the entire gif
    # try:
    #     count = 0
    #     while 1:
    #         # only process every third frame
    #         if count % 3 == 0:
    #             img.seek(img.tell()+1)
    #             saveImage(img, 'tmp')
    #             processFrame('tmp', directory, personGroupId)
    #         count += 1
    # except EOFError:
    #     pass # end of sequence
    # print ("Finished processing video")

def identifyFrame(frame):
    # load the image to analyze
    # img = convertCv2ToPil(frame)
    img = getImage("tmp.jpg")
    print(img)
    # detect the faces in the image
    detectOutput = detect(img)
    if detectOutput == None:
        showImage(frame)
        return

    for faceInfo in detectOutput:
        rect = faceInfo['faceRectangle']
        bounds = (int(rect['left']), int(rect['top']), int(rect['width']), int(rect['height']))
        drawRect(frame, bounds)
    showImage(frame)

def processFrame(filename, directory, personGroupId):
    # load the image to analyze
    img = getImage(filename)
    # detect the faces in the image
    detectOutput = detect(img)
    if detectOutput == None:
        return

    # format is faceId:image bounds
    faces = {}

    # add each detected face to faces dict
    for faceInfo in detectOutput:
        rect = faceInfo['faceRectangle']
        bounds = (int(rect['left']), int(rect['top']), int(rect['width']), int(rect['height']))
        faces[faceInfo['faceId']] = bounds

    # identify each face and add new ones to the imageDirectory
    faceIds = list(faces.keys())
    for i in range(len(faceIds) // 10 + 1):
        # a batch of at most 10 face ids
        # returns (personId, confidence)
        faceBatch = faceIds[10*i:10*i+10]
        # candidate people that these faces could belong to
        # None if new face
        candidates = identify(faceBatch, personGroupId)
        print(candidates)
        if candidates == None:
            # error happened during identify
            return

        for candidate in candidates:
            confidence = candidate['candidates'][0]['confidence']
            personId = candidate['candidates'][0]['personId']
            faceId = candidate['faceId']
            bounds = faces[faceId]
            # reasonably confident this is the right person
            if confidence > threshold:
                # candidate already exists
                # add the new face
                directory[personId].addFace(filename, bounds)
            else:
                # new face
                # add candidate
                person = Person(faceId, personGroupId)
                if person.id != None:
                    # person is created
                    person.setImage(cropImage(filename, bounds))
                    person.addFace(filename, faces[faceId])
                    directory[person.id] = person
                    # add to MongoDB
                    addMongoPerson(person)
    train()

def addPerson(filename, directory, personGroupId):
    # load the image to analyze
    img = getImage(filename)
    # detect the faces in the image
    detectOutput = detect(img)
    if detectOutput == None:
        return

    # add each detected face to faces dict
    faceInfo = detectOutput[0]
    rect = faceInfo['faceRectangle']
    bounds = (int(rect['left']), int(rect['top']), int(rect['width']), int(rect['height']))
    faceId = faceInfo['faceId']

    # identify each face and add new ones to the imageDirectory
    faceImg = cropImage(filename, bounds)
    # new face
    # add candidate
    person = Person(faceId, personGroupId)
    person.setImage(faceImg)
    person.addFace(filename, bounds)
    directory[person.id] = person

class Person:
    counter = 0
    def __init__(self, faceId, personGroupId):
        self.personGroupId = personGroupId
        self.numFaces = 1
        self.name = 'Person' + str(Person.counter)
        self.id = createPerson(personGroupId, self.name)
        if self.id != None:
            Person.counter += 1
            print ("Created new person with id", self.id)
        else:
            print ("Failed to create new person")

    def addFace(self, filename, bounds):
        # has not reached maximum # of faces per person
        if self.numFaces < 248:
            print ("Adding a new face for ", self.id)
            addFace(filename, bounds, self.id, self.personGroupId)

    def setImage(self, img):
        saveImage(img, self.id)
