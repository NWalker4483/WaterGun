from threading import Thread
import cv2 
import time
import numpy as np

class AidedLargestObjectTracker():
    def __init__(self, detector, max_query_rate = 3):
        self.detector = detector
        self.tracker = cv2.TrackerMOSSE_create()

        self.query = None
        self.query_bbox = (287, 23, 86, 320)
        self.successful = True
        self.initialized = False

        self.max_query_rate = max_query_rate
        self.frames_since = []

    def query_detector(self, frame):
        self.successful = False
        self.frames_since = [frame] 

        # Spawn Thread
        def check_detector(self, image):
            try:
                output = self.detector.update(image)
                print(output)
                self.query_bbox = tuple([int(i) for i in output[0]])
                self.successful = True
            except Exception as e:
                self.successful = False
                #print(e)

        self.query = Thread(target=check_detector, args=(self, frame))
        self.query.start()
    def init_tracker(self):
        return False, None
        self.tracker = cv2.TrackerMOSSE_create()
        print("ddddd")
        self.tracker.init(self.frames_since[0], self.query_bbox)
        print("ccccc")
        print(len(self.frames_since))
        for frame in self.frames_since:
            ok, bbox = self.tracker.update(frame)
        if ok:
            self.initialized = True
            return ok, bbox
        else:
            self.initialized = False
            return False, None
    def update(self, frame):
        if self.query == None:
            self.query_detector(frame)
            return False, None
        else:
            if self.query.is_alive():
                self.frames_since.append(frame)
                if self.initialized:
                    return self.tracker.update(frame)
                else:
                    return False, None
            else:
                self.query = None
                if self.successful:
                    return self.init_tracker()
                else:
                    return False, None

if __name__ == "__main__":
    camera = cv2.VideoCapture(0)
    tracker = AidedLargestObjectTracker()
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