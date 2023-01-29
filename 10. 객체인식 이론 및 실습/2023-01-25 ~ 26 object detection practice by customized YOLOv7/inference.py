from hubconf import custom
import torch, os, glob, cv2

"""디바이스 설정"""
DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

"""모델을 호출하자"""
model = custom(path_or_model='./runs/train/exp/weights/best.pt')
# print(model)
model.conf = 0.6 # NMS confidence threshold
model.iou = 0.45 # NMS IoU threshold
model.to(DEVICE)

"""image path list"""
image_path_list = glob.glob(os.path.join("./dataset/test/images", "*.jpg"))
# print(image_path_list)


for i in image_path_list :
    image_path = i

    """cv2로 이미지 읽기"""
    image = cv2.imread(image_path)

    """model input"""
    output = model(image, size=640) # 모델에 이미지 넣은 결과
    # print(output.print())
    bbox_info = output.xyxy[0]
    # print(bbox_info)
    for bbox in bbox_info :
        # print(bbox)
        x1 = int(bbox[0].item()) # bbox에 대한 좌표값을 정수형으로 변환
        y1 = int(bbox[1].item())
        x2 = int(bbox[2].item())
        y2 = int(bbox[3].item())

        score = round(bbox[4].item(), 4) # bbox에 찍힌 점수 반올림한 값
        label_number = int(bbox[5].item()) # bbox의 label 번호값
        # print(x1, y1, x2, y2, score, label_number)
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
    cv2.imshow("test", image)
    cv2.waitKey(1)