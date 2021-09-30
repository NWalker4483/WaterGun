import numpy as np
import cv2
from imutils.video import VideoStream
from watergun import WaterGun
#a = WaterGun()
#a.start()
#a.center()
#a.stop()
camera = VideoStream()
camera.start()

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((6*7,3), np.float32)
objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)
# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.
chesspoints = []
try:
    while True:
        img = camera.read()
        img = cv2.flip(img,0)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Find the chess board corners
        ret, corners = cv2.findChessboardCorners(gray, (7,6), None)
        # If found, add object points, image points (after refining them)
        if ret == True:
            time.sleep(.25)
            objpoints.append(objp)
            corners2 = cv2.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)
            imgpoints.append(corners)
            # Draw and display the corners
            chesspoints.append(corners2)
        for corners_ in chesspoints:
            cv2.drawChessboardCorners(img, (7,6), corners_, True)
        cv2.imshow('img', img)
        cv2.waitKey(1)
except Exception as e:
    raise(e)
finally:
    
    print("Started Calibration")
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
    np.save("camera_matrix.npy", mtx)
    np.save("dist_coefficients.npy", dist)
    print(ret, mtx, dist, rvecs, tvecs)
    #camera.release()
    cv2.destroyAllWindows()