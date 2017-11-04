import http.client, urllib.request, urllib.parse, urllib.error, base64, requests, json

from imagePil import *

from configuration import *

import time
import cv3

def processVideo(filename, directory, personGroupId):
	cap = cv2.VideoCapture("data/" + filename)
	while not cap.isOpened():
	    cap = cv2.VideoCapture("data/" + filename)
	    cv2.waitKey(1000)
	    print ("Wait for the header")

	pos_frame = cap.get(cv2.cv.CV_CAP_PROP_POS_FRAMES)
	while True:
	    flag, frame = cap.read()
	    if flag:
	        # The frame is ready and already captured
	        cv2.imshow('video', frame)
	        pos_frame = cap.get(cv2.cv.CV_CAP_PROP_POS_FRAMES)
	        print (str(pos_frame)+" frames")
	    else:
	        # The next frame is not ready, so we try to read it again
	        cap.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, pos_frame-1)
	        print ("frame is not ready")
	        # It is better to wait for a while for the next frame to be ready
	        cv2.waitKey(1000)

	    if cv2.waitKey(10) == 27:
	        break
	    if cap.get(cv2.cv.CV_CAP_PROP_POS_FRAMES) == cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT):
	        # If the number of captured frames is equal to the total number of frames,
	        # we stop
	        break

	# img = openImage(filename)
	# # To iterate through the entire gif
	# try:
	# 	count = 0
	# 	while 1:
	# 		# only process every third frame
	# 		if count % 3 == 0:
	# 			img.seek(img.tell()+1)
	# 			saveImage(img, 'tmp')
	# 			processFrame('tmp', directory, personGroupId)
	# 		count += 1
	# except EOFError:
	# 	pass # end of sequence
	# print ("Finished processing video")

def waitForTraining():
	while checkTrainingStatus() == False:
		# still training
		time.sleep(.2)

def checkJson(parsed):
	if len(parsed) == 0 or 'error' in parsed:
		# no faces detected or error
		print("Sorry. Something went wrong. Please try again.")
		return None
	return parsed

def detect(img):
	# Request headers.
	headers = {
		# 'Content-Type': 'application/json',
		'Content-Type': 'application/octet-stream',
		'Ocp-Apim-Subscription-Key': subscription_key,
	}

	# Request parameters.
	params = {
		'returnFaceId': 'true',
		'returnFaceLandmarks': 'false',
		# 'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
	}

	# Body. The URL of a JPEG image to analyze.
	# body = {'url': url}

	try:
		# Execute the REST API call and get the response.
		response = requests.request('POST', 'https://' + subscription_base + '/face/v1.0/detect', data=img, headers=headers, params=params)

		# print ('Response:')
		parsed = json.loads(response.text)
		# print (json.dumps(parsed, sort_keys=True, indent=2))

		return checkJson(parsed)

	except Exception as e:
		print('Error:')
		print(e)

def checkTrainingStatus():
	headers = {
		# Request headers
		'Ocp-Apim-Subscription-Key': subscription_key,
	}

	params = urllib.parse.urlencode({
	})

	ans = False
	try:
		conn = http.client.HTTPSConnection(subscription_base)
		conn.request("GET", "/face/v1.0/persongroups/" + personGroupId + "/training?%s" % params, "", headers)
		response = conn.getresponse()
		data = response.read()
		print(data)
		parsed = checkJson(json.loads(data.decode('utf8')))
		if parsed != None and parsed['status'] == 'succeeded':
			ans = True
		conn.close()
	except Exception as e:
		print("[Errno {0}] {1}".format(e.errno, e.strerror))
	return ans

def train():
	headers = {
		# Request headers
		'Ocp-Apim-Subscription-Key': subscription_key,
	}

	params = urllib.parse.urlencode({
	})

	try:
		conn = http.client.HTTPSConnection(subscription_base)
		conn.request("POST", "/face/v1.0/persongroups/" + personGroupId + "/train?%s" % params, "", headers)
		response = conn.getresponse()
		data = response.read()
		print(data)
		conn.close()
	except Exception as e:
		print("[Errno {0}] {1}".format(e.errno, e.strerror))

def identify(faceIds, personGroupId):
	waitForTraining();
	headers = {
		# Request headers
		'Content-Type': 'application/json',
		'Ocp-Apim-Subscription-Key': subscription_key,
	}

	params = urllib.parse.urlencode({
	})

	body = json.dumps({
		'faceIds': faceIds,
		'personGroupId': personGroupId,
		# 'maxNumOfCandidatesReturned': 1,
		'confidenceThreshold': 0,
		})

	ans = None

	try:
		conn = http.client.HTTPSConnection(subscription_base)
		conn.request("POST", "/face/v1.0/identify?%s" % params, body, headers)
		response = conn.getresponse()
		data = response.read()
		print(data)
		ans = checkJson(json.loads(data.decode('utf8')))
		conn.close()
	except Exception as e:
		print("[Errno {0}] {1}".format(e.errno, e.strerror))
	return ans

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
				person.setImage(cropImage(filename, bounds))
				person.addFace(filename, faces[faceId])
				directory[person.id] = person
	train()

def createPersonGroup(id, name):
	# Request headers.
	headers = {
		'Content-Type': 'application/json',
		'Ocp-Apim-Subscription-Key': subscription_key,
	}

	body = json.dumps({'name': name})

	try:
		conn = http.client.HTTPSConnection(subscription_base)
		conn.request("PUT", "/face/v1.0/persongroups/" + id, body, headers)
		response = conn.getresponse()
		data = response.read()
		print(data)
		print(response)
		conn.close()
	except Exception as e:
		print("[Errno {0}] {1}".format(e.errno, e.strerror))

def deletePersonGroup(id):
	headers = {
		# Request headers
		'Ocp-Apim-Subscription-Key': subscription_key,
	}

	try:
		conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
		conn.request("DELETE", "/face/v1.0/persongroups/" + id, "", headers)
		response = conn.getresponse()
		data = response.read()
		print(data)
		conn.close()
	except Exception as e:
		print("[Errno {0}] {1}".format(e.errno, e.strerror))

def addFace(filename, bounds, personId, personGroupId):
	headers = {
		# Request headers
		'Content-Type': 'application/octet-stream',
		'Ocp-Apim-Subscription-Key': subscription_key,
	}

	params = urllib.parse.urlencode({
		# Request parameters
		# 'userData': '{string}',
		'targetFace': "%d,%d,%d,%d" % (bounds[0], bounds[1], bounds[2], bounds[3]),
	})

	img = getImage(filename)

	try:
		conn = http.client.HTTPSConnection('eastus2.api.cognitive.microsoft.com')
		conn.request("POST", "/face/v1.0/persongroups/" + personGroupId +"/persons/" + personId + "/persistedFaces?%s" % params, img, headers)
		response = conn.getresponse()
		data = response.read()
		print(data)
		conn.close()
	except Exception as e:
		print("[Errno {0}] {1}".format(e.errno, e.strerror))

def createPerson(personGroupId, name):
	headers = {
		# Request headers
		'Content-Type': 'application/json',
		'Ocp-Apim-Subscription-Key': subscription_key,
	}

	params = urllib.parse.urlencode({
		
	})

	data = json.dumps({'name': name})

	ans = None

	try:
		conn = http.client.HTTPSConnection(subscription_base)
		conn.request("POST", "/face/v1.0/persongroups/" + personGroupId + "/persons?%s" % params, data, headers)
		response = conn.getresponse()
		data = response.read()
		print(data)
		ans = checkJson(json.loads(data.decode('utf8')))
		if ans != None:
			ans = ans['personId']
		conn.close()
	except Exception as e:
		print("[Errno {0}] {1}".format(e.errno, e.strerror))
	return ans

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
		Person.counter += 1
		self.id = createPerson(personGroupId, self.name)
		print ("Created new person with id", self.id)

	def addFace(self, filename, bounds):
		# has not reached maximum # of faces per person
		if self.numFaces < 248:
			print ("Adding a new face for ", self.id)
			addFace(filename, bounds, self.id, self.personGroupId)

	def setImage(self, img):
		saveImage(img, self.id)
