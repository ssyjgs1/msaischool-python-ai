import os
import glob
import cv2
from xml.etree.ElementTree import parse

total_image_path = './total_images'
total_label_path = './total_labels'

image = glob.glob(os.path.join(total_image_path, '*', '*.png'))
label = glob.glob(os.path.join(total_label_path, '*.txt'))

print("이미지 갯수 >>>", len(image), "라벨 갯수 >>>", len(label))

no_label_image = []
image_name_list = []
label_name_list = []



for i in image :
    image_name = os.path.basename(i)
    image_name = image_name.split('.')[0]
    image_name_list.append(image_name)
# print(image_name_list)

for i in label :
    label_name = os.path.basename(i)
    label_name = label_name.split('.')[0]
    label_name_list.append(label_name)
# print(label_name_list)

print(set(image_name_list) - set(label_name_list))
print(set(label_name_list) - set(image_name_list))