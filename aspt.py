from detector import Detector
from threading import Thread
import cv2 
import time
import numpy as np

class AidedSinglePersonTracker():
    def __init__(self, max_query_rate = 3):
        self.detector = Detector()
        self.tracker = cv2.legacy.TrackerMOSSE_create()

        self.query = None
        self.query_bbox = (287, 23, 86, 320)
        self.successful = True

        self.track_maintained = False
        self.max_query_rate = max_query_rate
        self.frames_since = [] 

    def query_detector(self, frame):
        self.successful = False
        self.frames_since = [frame] 

        # Spawn Thread
        def check_detector(self, image):
            try:
                output = self.detector.prediction(image)
                df = self.detector.filter_prediction(output, image)
                df = df.loc[df['class_name'] == "person"]
                biggest = df.iloc[0]
                print(biggest)
                self.query_bbox = (biggest["x1"], biggest["y1"], biggest["x2"], biggest["y2"])
                self.successful = True
            except:
                self.successful = False

        self.query = Thread(target=check_detector, args=(self, frame))
        self.query.start()

    def update(self, frame):
        self.ok, self.bbox = self.tracker.update(frame)
        if self.ok:
            return True, self.bbox
        else:
            if self.query != None:
                if self.query.is_alive():
                    self.frames_since.append(frame)
                    return False, None
                else:
                    if self.successful:
                        self.query = None
                        self.tracker = cv2.legacy.TrackerMOSSE_create()
                        self.tracker.init(self.frames_since[0], self.query_bbox)
                        for frame in self.frames_since:
                            ok, bbox = self.tracker.update(frame)
                        if ok:
                            return ok, bbox
            self.query_detector(frame)
        return False, None

if __name__ == "__main__":
    camera = cv2.VideoCapture(0)
    tracker = AidedSinglePersonTracker()
    while True:
        ret, frame = camera.read()

        ok, bbox = tracker.update(frame)

        # Start timer
        timer = cv2.getTickCount()

        # Update tracker
        ok, bbox = tracker.update(frame)

        # Calculate Frames per second (FPS)
        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)

        # Draw bounding box
        if ok:
            # Tracking success
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)
        else :
            # Tracking failure
            cv2.putText(frame, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)

        # Display tracker type on frame
        cv2.putText(frame, "MOOSE" + " Tracker", (100,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2);
    
        # Display FPS on frame
        cv2.putText(frame, "FPS : " + str(int(fps)), (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2);

        # Display result
        cv2.imshow("Tracking", frame)

        # Exit if ESC pressed
        k = cv2.waitKey(1) & 0xff
        if k == 27 : break