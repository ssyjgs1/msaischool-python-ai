# json xml to yolo
import os
import glob
import copy
import json
import cv2
import pandas as pd

label_dict = {"garbage_bag" : 0, "street_vendor": 1, "food_truck": 2, "banner": 3, "tent": 4,"flame": 5, "pet": 6, "bench": 7, 
                "park_pot": 8, "trash_can": 9, "rest_area": 10, "toilet": 11, "street_lamp": 12, "park_info": 13, 
                # "smoke": 14, # "fence": 15, # "sit_board"   : 16, # "park_headstone": 17
}

def main():
    xlsx_path1 = f'D:/train.xlsx'
    xlsx_path2 = f'D:/valid.xlsx'

    remove_list1 = remove_image_list(xlsx_path1)
    remove_list2 = remove_image_list(xlsx_path2)
    remove_list = remove_list1 + remove_list2

    for use in ['train', 'val']:
    # for use in ['train', 'val']:
        ori_json_path = f"D:/dataset/{use}/labels"
        new_images_path = f"D:/datasets/{use}/images"
        new_labels_path = f"D:/datasets/{use}/labels"
        os.makedirs(new_images_path, exist_ok= True)
        os.makedirs(new_labels_path, exist_ok= True)

        json_paths = glob.glob(os.path.join(ori_json_path, "*", "*.json"))
        # print(json_paths)
        # print(len(json_paths))
        # exit()

        for index, json_path in enumerate(json_paths) :
            # 본 데이터셋에서 학습에 필요한 정보만 읽어 반환
            try:
                # json 읽기
                with open(json_path, 'r', encoding='utf8') as f:
                    # json load
                    json_file = json.load(f)

                annotations = json_file['annotations']
                image_info  = json_file['images']
                image_path = json_path.replace('labels', 'images')
                image_path = image_path.replace('.json', '.jpg')
                # ./dataset/train/images\11.street_vendor\11_erip_su_11-10_13-30-48_aft_DF4.jpg

                # text file name
                img_name = image_info['ori_file_name']
                # 11_erip_su_11-10_13-30-48_aft_DF4.jpg

                # 이미지 이름이 remove_list에 없다면
                if img_name not in remove_list:
                    print(index,'\t', img_name)
                    
                    # 이미지 리사이즈 
                    image = resize(image_path, (1366, 786))

                    # # save resized image
                    cv2.imwrite(os.path.join(new_images_path, img_name), image)
                    
                    # text file name
                    txt_name = img_name.replace('.jpg', ".text")
                    # 11_erip_su_11-10_13-30-48_aft_DF4.text

                    # yolo width heigth image size getting
                    img_width  = image_info['width']
                    img_height = image_info['height']

                    for annotation in annotations:
                        label_name = annotation['object_class']
                        if label_name not in label_dict:
                            continue  # 비석, 울타리, 연기, 좌판 제외
                        bbox = annotation['bbox']
                        x1, y1, x2, y2 = bbox[0][0], bbox[0][1], bbox[1][0], bbox[1][1]

                        # voc -> yolo 좌표 얻기
                        yolo_x = (x1 + x2) / 2 / img_width
                        yolo_y = (y1 + y2) / 2 / img_height
                        yolo_w = (x2 - x1) / img_width
                        yolo_h = (y2 - y1) / img_height

                        # 라벨 number 
                        label_num = label_dict[label_name]
                        # print(index, yolo_x, yolo_y, yolo_w, yolo_h, label_num)

                        # yolo 좌표와 라벨을 텍스트 파일로 쓰기
                        with open(f"{new_labels_path}/{txt_name}", 'a') as f:
                            f.write(f"{label_num} {yolo_x} {yolo_y} {yolo_w} {yolo_h} \n")
                else:
                    print(f'{img_name} is in remove list')
            except Exception as e:
                print(e)

def remove_image_list(xlsx_path):
    # pip install openpyxl
    df = pd.read_excel(xlsx_path, engine='openpyxl')
    remove_list = list(df['filename'].dropna())
    return remove_list

def resize(image_path, size):
    # size: (new_width, new_height)
    # size 크기로 맞춰 이미지 resize 및 bbox 정보 수정
    image = cv2.imread(image_path)
    image = cv2.resize(image, (size[0], size[1]))

    return image

if __name__ == '__main__':
    main()