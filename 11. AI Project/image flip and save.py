"""이미지 좌우 반전 시켜 새로이 생성하는 스크립트"""
# 일부 이미지에 대해 생성 오류가 있었음

import cv2, glob, os
import matplotlib.pyplot as plt

route = './'
image_path = glob.glob(os.path.join(route, 'military uav from video', '*.png'))

os.makedirs('./fliptest', exist_ok=True)

for images in image_path :
    filename = os.path.basename(images)
    # print(filename)
    
    image = cv2.imread(images)
    # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.flip(image, 1) # 1은 좌우 반전, 0은 상하 반전이다.
    # cv2.imwrite(f'./fliptest/{filename}', image)
    cv2.imwrite(os.path.join(route, f'/fliptest/{filename}'), image)