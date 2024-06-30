import cv2
import pandas as pd
import numpy as np
from ultralytics import YOLO
import time
import torch
import pathlib
import requests
import os


pathlib.PosixPath = pathlib.WindowsPath


#cap = cv2.VideoCapture(1)
cap = cv2.VideoCapture('parking1.mp4')

#model_name = 'C:\\Users\\bccf\\Desktop\\park\\yolov5-master\\best_1.pt'
model_name=""
if model_name:
    current_directory = os.getcwd()
    file_path = os.path.join(current_directory)
    model = torch.hub.load(file_path, 'custom', source='local', path=model_name)
    #print('model loaded(senin agirlik modeli)')
else:
    current_directory = os.getcwd()
    file_path = os.path.join(current_directory)
    model = torch.hub.load(file_path, 'yolov5s',
                           source='local', pretrained=True,
                           force_reload=True)  # model_name yoksa yolov5s yuklenir


#model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
#model = torch.hub.load('ultralytics/yolov5', 'custom', path='best_1.pt')


def RGB(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE:
        colorsBGR = [x, y]
        print(colorsBGR)


cv2.namedWindow('RGB')
cv2.setMouseCallback('RGB', RGB)



#with open("coco.txt", "r") as my_file:
#    class_list = my_file.read().split("\n")


areas = [
    [(52, 364), (30, 417), (73, 412), (88, 369)],
    [(105, 353), (86, 428), (137, 427), (146, 358)],
    [(159, 354), (150, 427), (204, 425), (203, 353)],
    [(217, 352), (219, 422), (273, 418), (261, 347)],
    [(274, 345), (286, 417), (338, 415), (321, 345)],
    [(336, 343), (357, 410), (409, 408), (382, 340)],
    [(396, 338), (426, 404), (479, 399), (439, 334)],
    [(458, 333), (494, 397), (543, 390), (495, 330)],
    [(511, 327), (557, 388), (603, 383), (549, 324)],
    [(564, 323), (615, 381), (654, 372), (596, 315)],
    [(616, 316), (666, 369), (703, 363), (642, 312)],
    [(674, 311), (730, 360), (764, 355), (707, 308)]
]

free_spaces_list = []
previous_free_spaces_list = []
difference_list = []
plate_name = "IKU 1991"
difference = []

while True:
    start_time = time.time()
    ret, frame = cap.read()
    if not ret:
        break
    time.sleep(1) #videoda olduğunda bunu yapmamız gerekiyor
    frame = cv2.resize(frame, (1020, 500))


    results = model(frame)
    df = results.pandas().xyxy[0]

    #Her alandaki arabaları saymak için listeleri başlatın
    occupancy = [0] * 12
    free_spaces = []
    free_spaces_name=[]

    for index, row in df.iterrows():
        x1, y1, x2, y2 = int(row['xmin']), int(row['ymin']), int(row['xmax']), int(row['ymax'])
        class_id = row['class']
        confidence = row['confidence']
        class_name=row['name']
        c = class_name
        #print(c)

        #cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        #cv2.putText(frame, str(class_name), (x1, y1), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
        #cv2.putText(frame, str(confidence), (x1, y2), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)

        if 'car' in c:
            # Araba koordinatlarını hesaplayın
            cx = (x1 + x2) // 2
            cy = (y1 + y2) // 2

            # Aracın tanımlanan alanlardan herhangi birinde olup olmadığını kontrol edin
            for i, area in enumerate(areas):

                result = cv2.pointPolygonTest(np.array(area, np.int32), (cx, cy), False)
                if result >= 0:
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.circle(frame, (cx, cy), 3, (0, 0, 255), -1)
                    occupancy[i] += 1
                    cv2.putText(frame, str(c), (x1, y1), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)


    total_spaces = 12
    occupied_spaces = sum(occupancy)
    free_spaces = total_spaces - occupied_spaces
    print(free_spaces)


    current_free_spaces_list = []
    for i, count in enumerate(occupancy):
        if count == 0:
            current_free_spaces_list.append(f"Park - {i + 1}")


    previous_free_spaces = previous_free_spaces_list[-1] if previous_free_spaces_list else []


    for item in previous_free_spaces:
        if item not in current_free_spaces_list:
            difference.append(item)

    # Güncel listeyi kaydet
    previous_free_spaces_list.append(current_free_spaces_list)

    # Ekrana yazdır
    #print("Önceki boş park yerleri:", previous_free_spaces)
    #print("Sonraki boş park yerleri:", current_free_spaces_list)
    #print("Fark:", difference_list)

    #print(f"{plate_name} = {difference}")
    if difference:
        difference=difference[0]

    is_free=None
    if current_free_spaces_list==[]:
        is_free=False
    else:
        is_free=True


    print("s: ",is_free)

    data_to_send = {
        "free_spaces": free_spaces,
        "free_spaces_list": current_free_spaces_list,
        "difference": difference,
        "plate_name": plate_name,
        "is_free": is_free

    }
    print("diffrence: ",difference)

    try:
        response = requests.post('http://192.168.162.250:5000/update_spaces', json=data_to_send)

        if response.status_code == 200:
            print("Data sent successfully!")
        else:
            print("Failed to send data.")
    except requests.exceptions.RequestException as e:
        print(f"Error sending data: {e}")


    # Park alanlarını ve çerçeveyi işaretleyind
    for i, area in enumerate(areas):
        if occupancy[i] == 1 :
             color = (0, 0, 255)
        else:
            color = (0, 255, 0)
        cv2.polylines(frame, [np.array(area, np.int32)], True, color, 2)
        cv2.putText(frame, str(i+1), (area[0][0], area[0][1] + 20), cv2.FONT_HERSHEY_COMPLEX, 0.5, color, 1)

    cv2.putText(frame, str(free_spaces), (23, 30), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)


    end_time = time.time()
    fps = 1 / (end_time - start_time)
    cv2.putText(frame, f'FPS: {fps:.2f}', (23, 60), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)


    cv2.imshow("RGB", frame)

    difference=[]
    if cv2.waitKey(1) & 0xFF == 27:
        break


cap.release()
cv2.destroyAllWindows()
