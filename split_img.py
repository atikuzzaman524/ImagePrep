from PIL import Image, ImageDraw
import xml.etree.ElementTree as ET
import glob
import numpy as np


def img_center(image_path):
    image_obj = Image.open(image_path)
    img_width, img_height = image_obj.size
    img_width_center = float(img_width)/2
    img_height_center = float(img_height)/2
    center = np.array([img_width_center, img_height_center])
    return center


def crop(image_path, split, counter):
    # image_path: The path to the image to edit
    # coords: A tuple of x/y coordinates (x1, y1, x2, y2)
    # saved_location: Path to save the cropped image
    image_obj = Image.open(image_path)
    cropped_image = image_obj.crop(split)
    cropped_image.save(str(counter) + image_path)


def crop_xml(image_path, split, counter):
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

                    # redefine the bounding box wrt new top left
                    x_min =
                    Top_lef = np.array([x_min, y_min])
                    Top_rig = np.array([x_max, y_min])
                    bot_lef = np.array([x_min, y_max])
                    bot_rig = np.array([x_max, y_max])
                    center = np.array([x_center, y_center])
                    # print(Top_lef)

                    # Now lets express the for corners w.r.t. the center
                    Top_lef = np.subtract(Top_lef, center)
                    Top_rig = np.subtract(Top_rig, center)
                    bot_lef = np.subtract(bot_lef, center)
                    bot_rig = np.subtract(bot_rig, center)
                    # print(Top_lef)
                    # Define rotation matrix
                    c, s = np.cos(np.deg2rad(deg)), np.sin(np.deg2rad(deg))
                    rotate = np.array([[c, -s], [s, c]])

                    # Lets rotate some matrixes
                    Top_lef = np.dot(rotate, np.transpose(Top_lef))
                    Top_rig = np.dot(rotate, np.transpose(Top_rig))
                    bot_lef = np.dot(rotate, np.transpose(bot_lef))
                    bot_rig = np.dot(rotate, np.transpose(bot_rig))

                    # Now we reference our new points back to the top left
                    Top_lef = np.add(Top_lef, center)
                    Top_rig = np.add(Top_rig, center)
                    bot_lef = np.add(bot_lef, center)
                    bot_rig = np.add(bot_rig, center)

                    # Lets set all the x values in an array
                    # Lets set all the y values in an array
                    x_axis = np.array([Top_lef[0], Top_rig[0],
                                       bot_lef[0], bot_rig[0]])
                    y_axis = np.array([Top_lef[1], Top_rig[1],
                                       bot_lef[1], bot_rig[1]])

                    # Now we find the min and max of our X's and Y's
                    max_x = np.amax(x_axis)
                    min_x = np.amin(x_axis)
                    max_y = np.amax(y_axis)
                    min_y = np.amin(y_axis)
                    print(min_x, min_y, max_x, max_y)
                    rot_box = np.array([min_x, min_y, max_x, max_y])
                    return rot_box

                    # xml_filename = str(degree) + '_rotate_' + xml_path
                    # tree.write(xml_filename)


if __name__ == '__main__':

    rotate = 45

    for paths in glob.iglob('*.jpg'):
        x_center, y_center = img_center(paths)
        # rotate_img(paths, rotate)
        # rotate_xml(paths, rotate, x_center, y_center)
        rot_box = rotate_xml(paths, rotate, x_center, y_center)
        rotate_img(paths, rotate, rot_box)

        # print x_center, y_center
