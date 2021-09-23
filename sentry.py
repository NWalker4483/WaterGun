from watergun import WaterGun
from TFLite_Wrapper import TFLite_Wrapper
from aspt import AidedLargestObjectTracker
from simple_pid import PID
from imutils.video import VideoStream
import cv2

#create instance of MobileNet, SORT, and Water Gun
model = TFLite_Wrapper("Sample_TFLite_model")
tracker = AidedLargestObjectTracker(model)

camera = VideoStream()
camera.start()
water_gun = WaterGun()
water_gun.start()
water_gun.tilt = 50
water_gun.pan = 50
x, y = PID(1,0,1), PID(1,0,1)
frame = camera.read()
frame_center = (0, 0)
pan_pid = PID(1,0,.25)
tilt_pid = PID(1,0,.25)
while True:
    frame = camera.read()
    ok, bbox = tracker.update(frame)
    # track_bbs_ids is a np array where each row contains a valid bounding box and track_id (last column#print(track_bbs_ids)
    if ok:
        cv2.rectangle(frame, (int(bbox[0]),int(bbox[1])), (int(bbox[2]),int(bbox[3])), (10, 255, 0), 2)
    
    cv2.imshow("Frame", frame)
    cv2.waitKey(1)
    
    
