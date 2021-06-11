import cv2 as cv

import quit

def listen(app):
	if cv.waitKey(1) == ord('q'):
		quit.Key_Q(app)
