from PIL import Image
import xml.etree.ElementTree as ET
import glob
 
def crop(image_path, coords, saved_location):
	"""
	@param image_path: The path to the image to edit
	@param coords: A tuple of x/y coordinates (x1, y1, x2, y2)
	@param saved_location: Path to save the cropped image
	"""
	image_obj = Image.open(image_path)
	#w, h = image_obj.size
	#print w, h
	cropped_image = image_obj.crop(coords)
	cropped_image.save(saved_location)
	#cropped_image.show()
	w, h = cropped_image.size
	#print w, h

def size(image_path, crop_size):

	image_obj = Image.open(image_path)
	w, h = image_obj.size
	x_min = w/2-int(crop_size)/2
	x_max = w/2+int(crop_size)/2
	y_min = h/2-int(crop_size)/2
	y_max = h/2+int(crop_size)/2
	coords = (x_min, y_min, x_max, y_max)
	return coords, w, h

def evensize(image_path, even_size):
	image_obj = Image.open(image_path)
	old_size = image_obj.size
	#print old_size[1], image_path

	if old_size[1] < even_size[1]:
		new_size = even_size
		new_image = Image.new("RGB", new_size)
		new_image.paste(image_obj,  ((new_size[0]-old_size[0])/2, 
										 (new_size[1]-old_size[1])/2))
		new_image.save(image_path)
		buffer_shift = (new_size[1]-old_size[1])/2

	else:
		buffer_shift = 0

	#print old_size, image_path
	return buffer_shift


def resize(image_path, final_size, saved_file):

	image_obj = Image.open(image_path)
	resized_image = image_obj.resize(final_size)
	#resized_image.show()
	resized_image.save('/home/ameren/DarknetPrepScripts/edited/' + saved_file)

def resize_xml(xml_path, cordnts, final_size, buffer_shift):
	tree = ET.parse(xml_path)
	root = tree.getroot()
	filename = xml_path.replace('.xml', '.txt')
	f = open('/home/ameren/DarknetPrepScripts/edited/' + filename, "w+")

	for child in root:
		if child.tag == "object":
			for subchild in child:
				if subchild.tag == "name":
					object_class = subchild.text
					#print object_class

					if object_class == "insulator":
						objectnumber = 0
					if object_class == "flashover":
						objectnumber = 1
					if object_class == "broken":
						objectnumber = 2

					#print objectid
				if subchild.tag == "bndbox":
					for subsubchild in subchild:
						if subsubchild.tag == "xmin":
							x_min = float(subsubchild.text)
						if subsubchild.tag == "ymin":
							y_min = float(subsubchild.text)
						if subsubchild.tag == "xmax":
							x_max = float(subsubchild.text)
						if subsubchild.tag == "ymax":
							y_max = float(subsubchild.text)
					#print buffer_shift
					#print x_min, y_min, x_max, y_max
					y_min = y_min + buffer_shift
					y_max = y_max + buffer_shift
					#print x_min, y_min, x_max, y_max
					#print cordnts
					#cropping resize of boundingbox
					if x_min < cordnts[0]:
						x_min = 0.0
					else:
						x_min = x_min - cordnts[0]
					
					if y_min < cordnts[1]:
						y_min = 0.0
					else:
						y_min = y_min - cordnts[1]
					if x_max > cordnts[2]:
						x_max = 3744.0
					else:
						x_max = x_max - cordnts[0]
					if y_max > cordnts[3]:
						y_max = 3744.0
					else:
						y_max = y_max - cordnts[1]

					if x_min > cordnts[2]:
						x_min = 3744.0
					if y_min > cordnts[3]:
						y_min = 3744.0
					if x_max < cordnts[0]:
						x_max = 0.0
					if y_max < cordnts[1]:
						y_max = 0.0
					#print x_min, y_min, x_max, y_max



					# #scale resize of bounding box
					# x_min = x_min/9
					# y_min = y_min/9
					# x_max = x_max/9
					# y_max = y_max/9

					#Define width and height
					width = x_max - x_min
					height = y_max - y_min
					x_center = x_min + width/2
					y_center = y_min + height/2

					#calculate percentage in photocoordinates
					x_min_percent = x_center/3744
					y_min_percent = y_center/3744
					width_percent = width/3744
					heigh_percent = height/3744
					#print x_min_percent, y_min_percent


					
					line = str(objectnumber) + ' ' + str(x_min_percent) + ' ' + str(y_min_percent) + ' ' + str(width_percent) + ' ' + str(heigh_percent)
					

					if width_percent and heigh_percent != 0:
						f.write(line + "\n")
						print xml_path
						print x_min_percent, y_min_percent, width_percent, heigh_percent
						#print cordnts
						#print x_min, y_min, x_max, y_max 
						#print x_center, y_center

 
 
if __name__ == '__main__':

	for paths in glob.iglob('*.jpg'):

		buffershift = evensize(paths, (5280, 3956))
		#print paths
		cordnts, orig_width, orig_height = size(paths, 3744)
		crop(paths, cordnts, 'cropped.jpg')
		resize('cropped.jpg', (416, 416), paths)
		annotation = paths.replace('.jpg', '.xml')
		resize_xml(annotation, cordnts, 416, buffershift)