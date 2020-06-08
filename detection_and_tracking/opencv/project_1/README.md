## Simple detection and tracking using foreground and background extraction techniques

### Steps
1. Apply cv2.GaussianBlur to smooth image/ reduce noise.
2. Get the pixel difference between first frame and current frame using cv2.absdiff.
3. Apply cv2.threshold to convert binary image.
4. Appy cv2.erode that Erodes away the boundaries of foreground object
5. Find a contours and draw rectange using contours points