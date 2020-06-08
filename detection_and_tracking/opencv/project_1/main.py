from argparse import ArgumentParser
import logging as log
import sys
import cv2
import imutils
import numpy as np
from skvideo.io import vwrite
from skvideo.io import FFmpegWriter

def build_argparser():
    parser = ArgumentParser()
    parser.add_argument("-i", "--input", required=True, type=str,
                        help="Path to the video file")
    parser.add_argument("-min", "--min_area", required=False, type=int,
                        default=500, help="Min area size")
    return parser

def main():
    w = 400
    h = 400
    args = build_argparser().parse_args()
    log.basicConfig(format="[ %(levelname)s ] %(asctime)-15s %(message)s",
                    level=log.INFO, stream=sys.stdout)
    
    try:
        cap = cv2.VideoCapture(args.input)
        if not cap.isOpened():
            raise NameError('Just a Dummy Exception, write your own')
    except cv2.error as e:
        print("cv2.error:", e)
    
    out = FFmpegWriter('final.avi')
    
    firstFrame = None

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        
        if frame is None:
            break

        key_pressed = cv2.waitKey(20)
        
        gray = cv2.resize(frame, (w, h))
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        smooth = cv2.GaussianBlur(gray, (21, 21), 0)
        
        if firstFrame is None:
            firstFrame = gray
            continue
        
        frameDelta = cv2.absdiff(firstFrame, smooth)
        thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

        # Erosion
        kernel = np.ones((3,3),np.uint8)
        erode = cv2.erode(thresh, kernel, iterations=2)
        
        # Dilation
        dilate = cv2.dilate(thresh, None, iterations=2)
        
        contours, hierarchy = cv2.findContours(erode.copy(), cv2.RETR_EXTERNAL,
		        cv2.CHAIN_APPROX_SIMPLE)

        for c in contours:
            # if the contour is too small, ignore it
            if cv2.contourArea(c) < args.min_area:
                 continue

            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Display the resulting frame
        cv2.imshow('frame', frame)

        out.writeFrame(frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
if __name__ == "__main__":  
    main()