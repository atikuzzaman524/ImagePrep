from PIL import Image
import xml.etree.ElementTree as ET
import glob
import numpy as np

# enter how many sub-devisions you want in the x and the y direction
# We will figure out the rest
x_split = 1
y_split = 4


def split_setup(image_path, x_split, y_split):
    image_obj = Image.open(image_path)
    img_width, img_height = image_obj.size
    split_width = img_width/x_split
    split_height = img_height/y_split
    return split_width, split_height


def crop(image_path, i, j, split_width, split_height):
    # image_path: The path to the image to edit
    # coords: A tuple of x/y coordinates (x1, y1, x2, y2)
    # saved_location: Path to save the cropped image
    image_obj = Image.open(image_path)
    split = np.array([0, 0, 0, 0])
    split[0] = i * split_width
    split[1] = j * split_height
    split[2] = (i+1) * split_width
    split[3] = (j+1) * split_height
    cropped_image = image_obj.crop(split)
    cropped_image.save('/Users/harrisonknoll/code/DarknetPrepScripts/test/' +
                       str(i) + str(j) + "_" + image_path)
    image_obj.close()
    return split


def crop_xml(image_path, split, i, j):
    xml_path = image_path.replace('.jpg', '.xml')
    tree = ET.parse(xml_path)
    root = tree.getroot()
    for child in root.findall('object'):
        for subchild in child.findall('bndbox'):
            x_min = float(subchild.find('xmin').text)
            y_min = float(subchild.find('ymin').text)
            x_max = float(subchild.find('xmax').text)
            y_max = float(subchild.find('ymax').text)

            if x_min < split[0]:
                x_min = split[0]
            if y_min < split[1]:
                y_min = split[1]
            if x_max > split[2]:
                x_max = split[2]
            if y_max > split[3]:
                y_max = split[3]

            # if its out of bounds then get rid of it
            if x_max < split[0] or \
               y_max < split[1] or \
               x_min > split[2] or \
               y_min > split[3]:
                root.remove(child)
            else:
                # Shift the coordinates to be with respect to zero zero
                x_min = x_min - split[0]
                y_min = y_min - split[1]
                x_max = x_max - split[0]
                y_max = y_max - split[1]
                print(split)

                subchild.find('xmin').text = str(x_min)
                subchild.find('ymin').text = str(y_min)
                subchild.find('xmax').text = str(x_max)
                subchild.find('ymax').text = str(y_max)






    xml_filename = str(i) + str(j) + '_' + xml_path
    tree.write('/Users/harrisonknoll/code/DarknetPrepScripts/test/' +
               xml_filename)


if __name__ == '__main__':

    for paths in glob.iglob('*.jpg'):
        split_width, split_height = split_setup(paths, x_split, y_split)
        i = 0
        while i < x_split:
            j = 0
            while j < y_split:
                split = crop(paths, i, j, split_width, split_height)
                crop_xml(paths, split, i, j)
                j += 1
            i += 1
