import numpy as np
import cv2 as cv


class App:
	def __init__(self):
		self.cid = 0
		self.frame = None
		self.ink_color = []
		self.lower_color = [110,50,50]
		self.upper_color = [130,255,255]

	def start_camera(self):
		cap = cv.VideoCapture(self.cid)
		if not cap.isOpened():
			print("Cannot open camera")
			exit()

		while True:
			self.frame = self.read_from_camera(cap)
			cv.imshow('frame', self.frame)
			self.show_green_only(self.frame)
			self.set_mouse_event()

	def stop_camera(self, cap):
		cap.release()
		cv.destroyAllWindows()
		exit()

	def read_from_camera (self, cap):
		ret, frame = cap.read()

		if not ret:
			print("Can't recieve frame..")
			self.stop_camera(cap)

		if cv.waitKey(1) == ord('q'):
			self.stop_camera(cap)

		return frame

	def show_green_only(self, frame):
		hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

		mask = cv.inRange(hsv, np.array(self.lower_color), np.array(self.upper_color))
		masked_frame = cv.bitwise_and(frame, frame, mask=mask)
		cv.imshow('mask', mask)
		cv.imshow('color_masked_frame', masked_frame)

	def set_mouse_event(self):
		cv.setMouseCallback('frame', self.get_color_from_click)

	def get_color_from_click(self, event, x, y, flags, param):
		if event == cv.EVENT_LBUTTONDBLCLK:
			frame_as_list = self.frame[y, x].tolist()
			frame_in_hsv = cv.cvtColor(np.uint8([[frame_as_list]]), cv.COLOR_BGR2HSV)
			self.ink_color = frame_in_hsv.tolist()[0][0]

			self.lower_color[0] = (self.ink_color[0]-10) % 180
			self.upper_color[0] = (self.ink_color[0]+10) % 180
			print("setting", self.lower_color, "to", self.upper_color)

app = App()
app.start_camera()
