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
		self.corner_points_overlay = None
		self.rgb_mask = App()

	def start_cam(self):
		cap = cv.VideoCapture(self.cid)
		if not cap.isOpened():
			print("Cannot open camera")
			exit()

		self.cam_width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
		self.cam_height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))

		self.corner_points_overlay = self.create_blank_overlay(self.cam_height, self.cam_width)

		while True:
			self.read_from_camera(cap)

	def read_from_camera (self, cap):
		ret, frame = cap.read()
		self.frame = frame

		if not ret:
			print("Can't recieve frame..")
			self.stop_camera(cap)

		if len(self.perspective_crop) < 4:
			frame = self.frame
			corner_points_overlay_gray = cv.cvtColor(self.corner_points_overlay, cv.COLOR_BGR2GRAY)
			ret, corner_points_overlay_mask = cv.threshold(corner_points_overlay_gray, 10, 255, cv.THRESH_BINARY)
			inv_corner_points_overlay_mask = cv.bitwise_not(corner_points_overlay_mask)
			frame_for_corner_points_overlay = cv.bitwise_and(frame, frame, mask=inv_corner_points_overlay_mask)
			frame_overlayed_corner_points = cv.add(frame_for_corner_points_overlay, self.corner_points_overlay)

			cv.imshow('feed', frame_overlayed_corner_points)
			
			param = [self.corner_points_overlay]
			cv.setMouseCallback('feed', self.draw_point, param)
		else:
			cv.destroyWindow('feed')

			pts1 = np.float32(self.perspective_crop)
			pts2 = np.float32([[0, 0], [self.cam_width, 0], [0, self.cam_height], [self.cam_width, self.cam_height]])
			transform_frame_matrix = cv.getPerspectiveTransform(pts1, pts2)
			transform_frame = cv.warpPerspective(frame, transform_frame_matrix, (self.cam_width, self.cam_height))
			cv.imshow('transformed', transform_frame)

			mask, color_masked = self.rgb_mask.show_masked_frame(transform_frame)
			cv.imshow('mask', mask)
			param = [transform_frame]
			cv.setMouseCallback('transformed', self.rgb_mask.get_color_from_click, param)

		if cv.waitKey(1) == ord('q'):
			if len(self.perspective_crop) == 4:
				cv.destroyWindow('transformed')
				cv.destroyWindow('mask')
				self.perspective_crop = []
				self.corner_points_overlay = self.create_blank_overlay(self.cam_height, self.cam_width)
			else:
				self.stop_camera(cap)

	def stop_camera(self, cap):
		cap.release()
		cv.destroyAllWindows()
		exit()

	def create_blank_overlay(self, height, width):
		return np.zeros((height, width, 3), np.uint8)

	def draw_point(self, event, x, y, flags, param):
		if event == cv.EVENT_LBUTTONDOWN:
			print(f'drawing point at {x},{y}')
			self.perspective_crop.append([x, y])
			cv.circle(param[0], (x, y), 10, (0, 0, 255), 3)
