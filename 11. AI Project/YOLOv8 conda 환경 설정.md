1. Anaconda Prompt 관리자 권한 실행  
```conda create --name [가상환경이름] python=3.8```

2. conda activate yolov8  
   vs code Ultralytics-main 폴더로 접속한 이후 아래 cmd 창에서 진행

3. pip install -r requirements.txt  
   pip list

4. pip uninstall torch

5. pip uninstall torchvision

6. ```pip install torch==1.12.1+cu116 torchvision==0.13.1+cu116 torchaudio==0.12.1 --extra-index-url https://download.pytorch.org/whl/cu116```(하드웨어 따라 다름 - PyTorch 공식 사이트 참조 필요)
 
7. pip install albumentations