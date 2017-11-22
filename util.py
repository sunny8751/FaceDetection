from configuration import PERSON_GROUP_ID
import cognitive_face_wrapper.person as CF_person
import graphics

class Person:
    def __init__(self, personId, name, userData):
        self.id = personId
        self.name = name
        self.userData = userData
        self.persistedFaceIds = []
        print ("Created new person with id", self.id)

    def setPersistedFaceIds(self, persistedFaceIds):
        self.persistedFaceIds = persistedFaceIds

    def addFaceId(self, faceId):
        # has not reached maximum # of faces per person
        if len(self.persistedFaceIds) < 248:
            # add face id to face id list

            # add persisted face on azure
            img = graphics.openFaceImage(faceId + '.jpg')

            imgBin = graphics.convertToBinary(img)
            addFaceOutput = CF_person.add_face(imgBin, PERSON_GROUP_ID, self.id)
            persistedFaceId = addFaceOutput['persistedFaceId']
            self.persistedFaceIds.append(persistedFaceId)
            graphics.savePersistedFaceImage(persistedFaceId + '.jpg', img)
        else:
            print ("Exceeded limit for # of persisted face ids for %s" % self.id)

    def getImage(self):
        filename = self.persistedFaceIds[0] + '.jpg'
        return graphics.openPersistedFaceImage(filename)

# # person groups {personGroupId: list of Person}
# personGroups = {
#     'bad': [],
#     'neutral': [],
#     'good': [],
#     'test': []
# }

# labels
BAD = 'bad'
NEUTRAL = 'neutral'
GOOD = 'good'
TEST = 'test'

# directory of created Persons {personId: Person}
people = {}

# # list of Person for each label
# badPeople = []
# neutralPeople = []
# goodPeople = []
# testPeople = []
