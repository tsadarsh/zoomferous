import cv2 as cv
from sys import exit

class Key_Q:
	def __init__(self, app):
		self.app = app

		if len(app.corner_points_cords) == 4:
			self.back_to_select_corner_points()
		else:
			self.quit_zoomferous()

	def back_to_select_corner_points(self):
		cv.destroyWindow('transformed')
		cv.destroyWindow('mask')
		self.app.corner_points_cords = []
		self.app.corner_points = self.app.create_blank_overlay(self.app.cam_height, self.app.cam_width)

	def quit_zoomferous(self):
		self.app.cap.release()
		cv.destroyAllWindows()
		exit()
