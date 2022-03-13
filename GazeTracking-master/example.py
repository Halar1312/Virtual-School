import cv2

from gaze_tracking import GazeTracking

class EyeTrack:
    def __init__(self):
        print("Hurrah")
        gaze = GazeTracking()
        webcam = cv2.VideoCapture(0)
        centercount=0
        leftcount=0
        rightcount=0
        totalcount = 0
        while True:
            # We get a new frame from the webcam
            _,frame = webcam.read()

            totalcount=totalcount+1

            # We send this frame to GazeTracking to analyze it
            gaze.refresh(frame)

            frame = gaze.annotated_frame()
            text = ""

            #Values are updated when gaze.refresh function is called.
            if gaze.is_center():
                text = "Center"
                centercount=centercount+1
            elif gaze.is_right():
                text = "Right"
                rightcount=rightcount+1
            elif gaze.is_left():
                text = "Left"
                leftcount= leftcount+1
            elif gaze.is_Up ():
                text = "Up"
            elif gaze.is_blinking():
                text = "Blinking"
            cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (0, 255, 0), 2)
            left_pupil = gaze.pupil_left_coords()
            right_pupil = gaze.pupil_right_coords()
            cv2.putText(frame, "Left pupil:  " + str(left_pupil), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.8, (0, 255, 0), 1)
            cv2.putText(frame, "Right pupil: " + str(right_pupil), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.8, (0, 255, 0), 1)
            cv2.putText(frame, "Center Count: " + str(centercount), (90, 200), cv2.FONT_HERSHEY_DUPLEX, 0.8, (0, 255, 0), 1)
            cv2.putText(frame, "Focused Percentage: " + str((centercount/totalcount)*100)+"%", (90, 235), cv2.FONT_HERSHEY_DUPLEX, 0.8, (0, 255, 0), 1)
            cv2.imshow("Demo", frame)
            if cv2.waitKey(1) == 27:
                break
