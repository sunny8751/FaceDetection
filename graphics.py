from configuration import DATA_FOLDER, FACE_FOLDER, PERSISTED_FACE_FOLDER

import cv2

# bounds: (x, y, width, height)
def drawRect(img, bounds):
    point1 = (bounds[0], bounds[1])
    point2 = (bounds[0] + bounds[2], bounds[1] + bounds[3])
    cv2.rectangle(img, point1, point2, (0,255,0), 2)

def showImage(img):
    cv2.imshow('Face Detection', img)

def openFaceImage(filename):
    return cv2.imread(FACE_FOLDER + filename)

def openPersistedFaceImage(filename):
    return cv2.imread(PERSISTED_FACE_FOLDER + filename)

def openImage(filename):
    return cv2.imread(DATA_FOLDER + filename)

def saveFaceImage(filename, img):
    cv2.imwrite(FACE_FOLDER + filename, img);

def savePersistedFaceImage(filename, img):
    cv2.imwrite(PERSISTED_FACE_FOLDER + filename, img);

# bounds: (x, y, width, height)
def cropImage(img, bounds):
    return img[bounds[1]:bounds[1] + bounds[3], bounds[0]:bounds[0] + bounds[2]]

def convertToBinary(img):
    # save img to temp file
    tmpFilename = DATA_FOLDER + "tmp.jpg"
    cv2.imwrite(tmpFilename, img);
    return open(tmpFilename, 'rb')

def processVideo(filename, processFunction):
    cap = cv2.VideoCapture(DATA_FOLDER + filename)
    while not cap.isOpened():
        cap = cv2.VideoCapture(DATA_FOLDER + filename)
        cv2.waitKey(1000)
        print ("Wait for the header")

    frameRate = cap.get(5)

    pos_frame = cap.get(cv2.CAP_PROP_POS_FRAMES)
    while True:
        flag, frame = cap.read()
        if flag:
            # The frame is ready and already captured
            pos_frame = cap.get(cv2.CAP_PROP_POS_FRAMES)

            # if pos_frame % (secondsPerFrame * math.floor(frameRate)) == 0:
                # process the frame every second
                # cv2.imshow('video', frame)
                # print (str(pos_frame)+" frames")

                # save frame to tmp file
                # cv2.imwrite('data/tmp.jpg', frame)
                # processFrame('tmp.jpg', directory, personGroupId)
                # identifyFrame('tmp.jpg')
            processFunction(frame, pos_frame, frameRate)
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
