# import the necessary packages
import numpy as np
import imutils
import cv2

class NCS2_Wrapper():
    # initialize the list of class labels MobileNet SSD was trained to
    # detect, then generate a set of bounding box colors for each class
    CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
        "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
        "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
        "sofa", "train", "tvmonitor"]
    COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))
    model = "Sample_MobileNetSSD_model/MobileNetSSD_deploy.caffemodel"
    prototxt = "Sample_MobileNetSSD_model/MobileNetSSD_deploy.prototxt"
    def __init__(self, min_confidence = .5, filter_for = None):
        if filter_for == None:
            self.filter_for = set(NCS2_Wrapper.CLASSES)
        else:
            self.filter_for = filter_for
        """
        ap.add_argument("-p", "--prototxt", required=True,
            help="path to Caffe 'deploy' prototxt file")
            help="path to Caffe pre-trained model")
            """
        # load our serialized model from disk
        print("[INFO] loading model...")
        net = cv2.dnn.readNetFromCaffe(NCS2_Wrapper.prototxt, NCS2_Wrapper.model)
        # specify the target device as the Myriad processor on the NCS
        net.setPreferableTarget(cv2.dnn.DNN_TARGET_MYRIAD)
        self.net = net

    def update(self, frame):
        frame = imutils.resize(frame, width=400)
        # grab the frame dimensions and convert it to a blob
        (h, w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(frame, 0.007843, (300, 300), 127.5)    
        # pass the blob through the network and obtain the detections and
        # predictions
        self.net.setInput(blob)
        detections = self.net.forward()
        good_detections = []
        # loop over the detections
        for i in np.arange(0, detections.shape[2]):
            # extract the confidence (i.e., probability) associated with
            # the prediction
            confidence = detections[0, 0, i, 2]
            # filter out weak detections by ensuring the `confidence` is
            # greater than the minimum confidence
            if confidence > self.min_confidence:
                # extract the index of the class label from the
                # `detections`, then compute the (x, y)-coordinates of
                # the bounding box for the object
                idx = int(detections[0, 0, i, 1])
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                if self.CLASSES[idx] in self.filter_for:
                    good_detections.append(box.astype("int"))
        return good_detections
        
if __name__ == "__main__":
        
    (startX, startY, endX, endY) = box.astype("int")
    # draw the prediction on the frame
    label = "{}: {:.2f}%".format(CLASSES[idx],
        confidence * 100)
    cv2.rectangle(frame, (startX, startY), (endX, endY),
        COLORS[idx], 2)
    y = startY - 15 if startY - 15 > 15 else startY + 15
    cv2.putText(frame, label, (startX, y),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)

