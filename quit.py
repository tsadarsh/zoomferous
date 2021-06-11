import cv2 as cv


class Key_Q:
	def __init__(self, app):
		self.app = app

		if len(app.perspective_crop) == 4:
			self.back_to_select_corner_points()
		else:
			self.quit_zoomferous()

	def back_to_select_corner_points(self):
		cv.destroyWindow('transformed')
		cv.destroyWindow('mask')
		self.app.perspective_crop = []
		self.app.corner_points_overlay = self.app.create_blank_overlay(self.app.cam_height, self.app.cam_width)

	def quit_zoomferous(self):
		self.app.cap.release()
		cv.destroyAllWindows()
		exit()