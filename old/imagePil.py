from PIL import Image, ImageFont, ImageDraw, ImageEnhance
from os.path import expanduser
import cv2

baseFolder = "data/"

# crop image based on bounds
# returns cropped image
def cropImage(filename, bounds):
	img = openImage(filename)
	area = (bounds[0], bounds[1], bounds[0] + bounds[2], bounds[1] + bounds[3])
	croppedImg = img.crop(area)
	# croppedImg.show()
	return croppedImg

# saves img as filename
def saveImage(img, newFilename):
	print ("Save new image as " + newFilename)
	img.save(baseFolder + newFilename, "JPEG")

# returns stream of binary data from image
def getImage(filename):
	return open(expanduser('data/' + filename), 'rb')

def openImage(filename):
	return Image.open(baseFolder + filename)

#CV2
def showImage(img):
	# img = openImage(filename)
	# img.show()
    cv2.imshow('Face Detection', img)

# bounds: (x, y, width, height)
def drawRect(img, bounds):
    # source_img = Image.open(baseFolder + filename).convert("RGB")
    # draw = ImageDraw.Draw(source_img)
    # draw.rectangle(((bounds[0], bounds[1]), (bounds[2], bounds[3])), fill="red")
    # # draw.text((20, 70), "something123", font=ImageFont.truetype("font_path123"))
    # source_img.save(baseFolder + filename, "JPEG")
    point1 = (bounds[0], bounds[1])
    point2 = (bounds[0] + bounds[2], bounds[1] + bounds[3])
    cv2.rectangle(img, point1, point2, (0,255,0), 15)

def convertCv2ToPil(cv2_image):
    cv2_image = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(cv2_image)
    return img
