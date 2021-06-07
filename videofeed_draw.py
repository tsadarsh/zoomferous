import numpy as np
import cv2 as cv

from rgb_mask import App


class Freecom:
	def __init__(self, cid=0):
		self.cid = cid
		self.cam_width = None
		self.cam_height = None
		self.frame = None
		self.ink_color = []
		self.lower_color = [110,50,50]
		self.upper_color = [130,255,255]
		self.perspective_crop = []
		self.blank_img = None
		self.rgb_mask = App()

	def start_cam(self):
		cap = cv.VideoCapture(self.cid)
		if not cap.isOpened():
			print("Cannot open camera")
			exit()

		self.cam_width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
		self.cam_height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))

		self.blank_img = np.zeros((self.cam_height, self.cam_width, 3), np.uint8)

		while True:
			self.frame = self.read_from_camera(cap)

	def read_from_camera (self, cap):
		ret, frame = cap.read()

		if not ret:
			print("Can't recieve frame..")
			self.stop_camera(cap)

		if len(self.perspective_crop) < 4:
			cv.imshow('feed', frame)
			cv.imshow('bg', self.blank_img)
			param = [self.blank_img]
			cv.setMouseCallback('feed', self.draw_point, param)
		else:
			cv.destroyWindow('feed')
			cv.destroyWindow('bg')

			pts1 = np.float32(self.perspective_crop)
			pts2 = np.float32([[0, 0], [self.cam_width, 0], [0, self.cam_height], [self.cam_width, self.cam_height]])
			transform_frame_matrix = cv.getPerspectiveTransform(pts1, pts2)
			transform_frame = cv.warpPerspective(frame, transform_frame_matrix, (self.cam_width, self.cam_height))
			cv.imshow('new', transform_frame)

			mask, color_masked = self.rgb_mask.show_masked_frame(transform_frame)
			cv.imshow('mask', mask)
			param = [transform_frame]
			cv.setMouseCallback('new', self.rgb_mask.get_color_from_click, param)

		if cv.waitKey(1) == ord('q'):
			if len(self.perspective_crop) == 4:
				cv.destroyWindow('new')
				cv.destroyWindow('mask')
				self.perspective_crop = []
			else:
				self.stop_camera(cap)

		return frame

	def stop_camera(self, cap):
		cap.release()
		cv.destroyAllWindows()
		exit()

	def draw_point(self, event, x, y, flags, param):
		if event == cv.EVENT_LBUTTONDOWN:
			print(f'drawing point at {x},{y}')
			self.perspective_crop.append([x, y])
			cv.circle(param[0], (x, y), 10, (255, 0, 0), -1)
