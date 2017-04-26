from code.pycode.load import getImage

def extractImageArea(path, cp1, cp2, savepath):
	im = getImage(path)
	width = im.size[0]
	height = im.size[1]

	pixeldata = im.load()
	for i in range(height):
		for j in range(width):
			if j not in range(cp1[0],cp2[0]) or i not in range(cp1[1],cp2[1]):
				pixeldata[j,i] = 0

	im.save(savepath)

def cropImage(path, cp1,cp2, savepath=None):
	if not savepath:
		savepath = path

	im = getImage(path)
	width = im.size[0]
	height = im.size[1]

	pixeldata = im.load()
	for i in range(height):
		for j in range(width):
			if j in range(cp1[0],cp2[0]) and i in range(cp1[1],cp2[1]):
				pixeldata[j,i] = 0

	im.save(savepath)