from PIL import Image
import xml.etree.ElementTree as ET
import glob
import numpy as np

def img_center(image_path):

    image_obj = Image.open(image_path)
    img_width, img_height = image_obj.size
    img_width_center = float(img_width)/2
    img_height_center = float(img_height)/2
    return img_width_center, img_height_center

def rotate_img(image_path, degree):
    image_obj = Image.open(image_path)
    rotate_img = image_obj.rotate(degree, resample=Image.BICUBIC)
    rotate_img.show()
    rotate_img.save(str(degree) + '_rotate_' + image_path)
    s =  rotate_img.size
    print (s[0], s[1])

def rotate_xml(image_path, degree, x_center, y_center):
    xml_path = image_path.replace('.jpg', '.xml')
    tree = ET.parse(xml_path)
    root = tree.getroot()
    for child in root:
        if child.tag == "object":
            for subchild in child:
                if subchild.tag == "bndbox":
                    x_min = float(subchild.find('xmin').text)
                    y_min = float(subchild.find('ymin').text)
                    x_max = float(subchild.find('xmax').text)
                    y_max = float(subchild.find('ymax').text)

                    #rotation: 
                    #First lets define the four corners
                    Top_left    = (x_min, y_min, 0.0, 0.0)
                    Top_right   = (x_max, y_min, 0.0, 0.0)
                    bottom_left = (x_min, y_max, 0.0, 0.0)
                    bottom_right= (x_max, y_max, 0.0, 0.0)

                    #Now lets define the vector from the center of image to the corner
                    Top_left[2] = 

                    

                
    # xml_filename = str(degree) + '_rotate_' + xml_path
    # tree.write(xml_filename)




if __name__ == '__main__':

    rotate = 90

    for paths in glob.iglob('*.jpg'):
        x_center, y_center = img_center(paths)
        # rotate_img(paths,rotate)
        # rotate_xml(paths, rotate, x_center, y_center)
        rotate_xml(paths, rotate, x_center, y_center)
        
        #print x_center, y_center