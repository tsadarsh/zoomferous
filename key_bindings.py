import cv2 as cv

import quit

def listen(app):
	key = cv.waitKey(1)
	if key == ord('q'):
		quit.Key_Q(app)

	elif key == ord('s'):
		app.save_frame()

	elif key == ord('r'):
		app.change_ink_color('r')

	elif key == ord('b'):
		app.change_ink_color('b')

	elif key == ord('g'):
		app.change_ink_color('g')
