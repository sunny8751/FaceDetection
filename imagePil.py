from PIL import Image
from os.path import expanduser

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
	img.save("data/" + newFilename + ".jpg", "JPEG")

# returns stream of binary data from image
def getImage(filename):
	return open(expanduser('data/' + filename), 'rb')

def openImage(filename):
	return Image.open("data/" + filename)