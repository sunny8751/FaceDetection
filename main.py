from faceApi import *
from configuration import *

from pymongo import MongoClient


# format is personId:Person class
directory = {}

def run():
	processVideo('video.mp4', directory, personGroupId)
	# addPerson("obama.jpg", directory, personGroupId)
	# train()
	# checkTrainingStatus()

	# processFrame("small_family.jpg", directory, personGroupId)
	# processFrame("family_photo.jpg", directory, personGroupId)

	# print (directory)
	# deletePersonGroup('good')
	# create person groups: good, neutral, bad


	# personGroupIds = ['good', 'neutral', 'bad']
	# for id in personGroupIds:
	# 	createPersonGroup(id, id + ' people')
	# print ('Person groups created')
	# url = 'https://i.pinimg.com/736x/04/be/aa/04beaa2b9ac077e8f7d69bf53732ac09--corporate-photoshoot-group-corporate-team-photos.jpg'
run()
