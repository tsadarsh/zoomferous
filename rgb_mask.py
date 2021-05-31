import numpy as np
import cv2 as cv


class App:
	def __init__(self):
		self.cid = 0

	def start_camera(self):
		cap = cv.VideoCapture(self.cid)
		if not cap.isOpened():
			print("Cannot open camera")
			exit()

		while True:
			frame = self.read_from_camera(cap)
			cv.imshow('frame', frame)
			self.show_green_only(frame)

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
		lower_blue = np.array([110,50,50])
		upper_blue = np.array([130,255,255])


		lower_limit = np.array([0, 0, 0])
		upper_limit = np.array([50, 255, 50])

		mask = cv.inRange(hsv, lower_blue, upper_blue)
		masked_frame = cv.bitwise_and(frame, frame, mask=mask)
		cv.imshow('mask', mask)
		cv.imshow('green_masked_frame', masked_frame)


app = App()
app.start_camera()