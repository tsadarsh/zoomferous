import numpy as np
import cv2 as cv

from rgb_mask import App


class Freecom:
	def __init__(self, cid=0):
		self.cid = cid
		self.cap = None
		self.cam_width = None
		self.cam_height = None
		self.frame = None
		self.ink_color = []
		self.lower_color = [110,50,50]
		self.upper_color = [130,255,255]
		self.perspective_crop = []
		self.corner_points_overlay = None
		self.rgb_mask = Mask_from_ink_color()

	def create_videocapture_object(self):
		self.cap = cv.VideoCapture(self.cid)
		if not self.cap.isOpened():
			print("Cannot open camera")
			exit()

		self.cam_height = self.get_camera_height(self.cap)
		self.cam_width = self.get_camera_width(self.cap)

		self.corner_points_overlay = self.create_blank_overlay(self.cam_height, self.cam_width)

		return self.cap

	def get_camera_height(self, cap):
		return int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))

	def get_camera_width(self, cap):
		return int(cap.get(cv.CAP_PROP_FRAME_WIDTH))

	def run_zoomferous(self, cap):
		self.frame = self.get_camera_frame(cap)

		if len(self.perspective_crop) < 4:
			self.selecting_corner_points()
		else:
			self.show_transformed_frame()

	def get_camera_frame(self, cap):
		ret, frame = cap.read()

		if not ret:
			print("Can't recieve frame..")
			self.stop_camera(cap)

		return frame

	def selecting_corner_points(self):
		corner_points_overlay_gray = cv.cvtColor(self.corner_points_overlay, cv.COLOR_BGR2GRAY)
		ret, corner_points_overlay_mask = cv.threshold(corner_points_overlay_gray, 10, 255, cv.THRESH_BINARY)
		inv_corner_points_overlay_mask = cv.bitwise_not(corner_points_overlay_mask)
		frame_for_corner_points_overlay = cv.bitwise_and(self.frame, self.frame, mask=inv_corner_points_overlay_mask)
		frame_overlayed_corner_points = cv.add(frame_for_corner_points_overlay, self.corner_points_overlay)

		cv.imshow('Zoomferous', frame_overlayed_corner_points)

		param = [self.corner_points_overlay]
		cv.setMouseCallback('Zoomferous', self.draw_corner_points, param)

	def show_transformed_frame(self):
		pts1 = np.float32(self.perspective_crop)
		pts2 = np.float32([[0, 0], [self.cam_width, 0], [0, self.cam_height], [self.cam_width, self.cam_height]])
		transform_frame_matrix = cv.getPerspectiveTransform(pts1, pts2)
		transform_frame = cv.warpPerspective(self.frame, transform_frame_matrix, (self.cam_width, self.cam_height))
		cv.imshow('Zoomferous', transform_frame)

		mask, color_masked = self.rgb_mask.show_masked_frame(transform_frame)
		cv.imshow('mask', mask)
		param = [transform_frame]
		cv.setMouseCallback('Zoomferous', self.rgb_mask.get_color_from_click, param)

	def create_blank_overlay(self, height, width):
		return np.zeros((height, width, 3), np.uint8)

	def draw_corner_points(self, event, x, y, flags, param):
		if event == cv.EVENT_LBUTTONDOWN:
			print(f'drawing point at {x},{y}')
			self.perspective_crop.append([x, y])
			cv.circle(param[0], (x, y), 10, (0, 0, 255), 3)


class Mask:
	def __init__(self):
		self.frame = None
		self.ink_color = None

	def get_color_from_click(self, event, x, y, flags, param):
		frame_as_list = param[0][y, x].tolist()
		frame_in_hsv = cv.cvtColor(np.uint8([[frame_as_list]]), cv.COLOR_BGR2HSV)
		self.ink_color = frame_in_hsv.tolist()[0][0]


class Mask_from_ink_color(Mask):
	def __init__(self):
		self.lower_color = [110,50,50]
		self.upper_color = [130,255,255]

	def get_color_from_click(self, event, x, y, flags, param):
		if event == cv.EVENT_LBUTTONDBLCLK:
			super().get_color_from_click(event, x, y, flags, param)

			self.lower_color[0] = (self.ink_color[0]-10) % 180
			self.upper_color[0] = (self.ink_color[0]+10) % 180
			print("picking", self.lower_color, "to", self.upper_color, f"from {x}, {y}")

	def show_masked_frame(self, frame):
		hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

		mask = cv.inRange(hsv, np.array(self.lower_color), np.array(self.upper_color))
		masked_frame = cv.bitwise_and(frame, frame, mask=mask)

		return mask, masked_frame
