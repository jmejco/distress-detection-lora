#Import time module for sleep functions
import time
#Import imutils for image processing
import imutils
#Import picamera functions for camera capture
from picamera.array import PiRGBArray
from picamera import PiCamera
#Import configurations
from config import *
#Import classification and alarm functions
from functions import *

#Initialize threshold counter and initial frame
COUNTER = 0
first_frame = None

#Open camera object
with PiCamera() as camera:
    #Capture as RGB array
    with PiRGBArray(camera) as stream:
        #Set camera resolution from configurations
        camera.resolution = RESOLUTION
        #Allow camera to warm up
        time.sleep(CAMERA_WARMUP_TIME)

        #Start looping over each continuous frame
        for f in camera.capture_continuous(stream, format="bgr"):

            #Clear the previous strean for caorture
            stream.truncate()
            stream.seek(0)
            #Set the current frame array
            current_frame = f.array

            #Resize, convert to grayscale and apply blur to create the background mask
            current_frame = imutils.resize(current_frame, width=500)
            mask = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
            mask = cv2.GaussianBlur(mask, BLUR_SIZE, 0)

            #Perform initial background modelling
            if first_frame is None:
                first_frame = mask
                continue

            #Compute difference between background and current image
            frame_diff = cv2.absdiff(first_frame, mask)

            #Reset the counter if the difference is negligible
            if np.mean(frame_diff) < MIN_DIFF:
                COUNTER = 0
            
            #Detect the contours in the image
            frame_threshold = cv2.threshold(frame_diff, 25, 255, cv2.THRESH_BINARY)[1]
            frame_threshold = cv2.dilate(frame_threshold, None, iterations=2)
            contours = cv2.findContours(frame_threshold.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            contours = imutils.grab_contours(contours)

            #Loop through the detected contours
            for contour in contours:
                #Ignore if the contour area is small
                if cv2.contourArea(contour) < MIN_AREA:
                    continue

                #Sleep for 1 second to allow time thresholding
                time.sleep(1.0)
                
                #Increment counter for every frame which is occupied
                COUNTER += 1
                
                if COUNTER >= TIME_THRESHOLD:

                    #Reset the counter if the threshold is exceeded
                    COUNTER = 0

                    #Run the object classification module on the last frame
                    detected = classify(current_frame)

                    
                    if detected is not None:
                        #Run the LoRa alarm module if a person is detected
                        send_lora(detected)

                        #Allow the system to cool off
                        time.sleep(TIME_BETWEEN_SIGNALS)

                        #Reset the frame
                        first_frame = None
            #Clear the stream
            stream.truncate(0)
