import cv2
import pandas as pd
import numpy as np
from ultralytics import YOLO
import torch
import time

model=torch.hub.load('ultralytics/yolov5', 'yolov5s')


def RGB(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE :  
        colorsBGR = [x, y]
        print(colorsBGR)
        

cv2.namedWindow('RGB')
cv2.setMouseCallback('RGB', RGB)

cap=cv2.VideoCapture('parking1.mp4')

   




area9=[(511,327),(557,388),(603,383),(549,324)]




while True:    
    ret,frame = cap.read()
    if not ret:
        break
    
    frame=cv2.resize(frame,(1020,500))

    results = model(frame)
 #   print(results)
    df=results.pandas().xyxy[0]

#    print(px)
   
    list9=[]
   
    
    for index,row in df.iterrows():
#        print(row)
        #print("asdasdas ",df.iterrows)
        x1, y1, x2, y2 = int(row['xmin']), int(row['ymin']), int(row['xmax']), int(row['ymax'])

        c=row['name']
        if 'car' in c:
            cx=int(x1+x2)//2
            cy=int(y1+y2)//2

       
      
            results9=cv2.pointPolygonTest(np.array(area9,np.int32),((cx,cy)),False)
            if results9>=0:
               cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)
               cv2.circle(frame,(cx,cy),3,(0,0,255),-1)
               list9.append(c)  
        
              
            
    
    a9=(len(list9))
  
  
    if a9==1:
        cv2.polylines(frame,[np.array(area9,np.int32)],True,(0,0,255),2)
        cv2.putText(frame,str('9'),(591,398),cv2.FONT_HERSHEY_COMPLEX,0.5,(0,0,255),1)
    else:
        cv2.polylines(frame,[np.array(area9,np.int32)],True,(0,255,0),2)
        cv2.putText(frame,str('9'),(591,398),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),1)
   
    
    

    cv2.imshow("RGB", frame)

    if cv2.waitKey(1)&0xFF==27:
        break
cap.release()
cv2.destroyAllWindows()
#stream.stop()


