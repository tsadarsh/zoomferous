import numpy as np
import cv2 as cv
from skimage.filters import threshold_sauvola,threshold_local

class Freecom:
	def __init__(self, cid=0):
		self.cid = cid
		self.frame = None
		self.ink_color = []
		self.lower_color = [110,50,50]
		self.upper_color = [130,255,255]
		self.cap = self.create_videocapture_object()
		self.cam_height = self.get_camera_height()
		self.cam_width = self.get_camera_width()
		self.corner_points_cords = []
		self.corner_points = self.create_blank_overlay(self.cam_height, self.cam_width)
		self.masker = Mask_from_ink_color()


	def create_videocapture_object(self):
		cap = cv.VideoCapture(self.cid)
		if not cap.isOpened():
			print("Cannot open camera")
			exit()

		return cap

	def get_camera_height(self):
		return int(self.cap.get(cv.CAP_PROP_FRAME_HEIGHT))

	def get_camera_width(self):
		return int(self.cap.get(cv.CAP_PROP_FRAME_WIDTH))

	def run_zoomferous(self):
		self.frame = self.get_camera_frame()

		if len(self.corner_points_cords) < 4:
			self.selecting_corner_points()
		else:
			self.show_transformed_frame()

	def get_camera_frame(self):
		ret, frame = self.cap.read()

		if not ret:
			print("Can't recieve frame..")

		return frame

	def create_blank_overlay(self, height, width):
		return np.zeros((height, width, 3), np.uint8)

	def selecting_corner_points(self):
		self.show_frame_with_selected_corner_points()
		cv.setMouseCallback('Zoomferous', self.draw_corner_points)

	def draw_corner_points(self, event, x, y, flags, param):
		if event == cv.EVENT_LBUTTONDOWN:
			print(f'drawing point at {x},{y}')
			self.corner_points_cords.append([x, y])
			cv.circle(self.corner_points, (x, y), 10, (0, 0, 255), 3)

	def show_frame_with_selected_corner_points(self):
		corner_points_mask = cv.inRange(self.corner_points, np.array([0,0,254]), np.array([0,0,256]))
		inv_corner_points_mask = cv.bitwise_not(corner_points_mask)
		frame_without_corner_points = cv.bitwise_and(self.frame, self.frame, mask=inv_corner_points_mask)
		frame_with_corner_points = cv.add(frame_without_corner_points, self.corner_points)

		cv.imshow('Zoomferous', frame_with_corner_points)

	def show_transformed_frame(self):
		pts1 = np.float32(self.corner_points_cords)
		pts2 = np.float32([[0, 0], [self.cam_width, 0], [0, self.cam_height], [self.cam_width, self.cam_height]])
		transform_frame_matrix = cv.getPerspectiveTransform(pts1, pts2)
		transform_frame = cv.warpPerspective(self.frame, transform_frame_matrix, (self.cam_width, self.cam_height))
		cv.imshow('Zoomferous', transform_frame)

		mask, color_masked = self.masker.show_masked_frame(transform_frame)
		cv.imshow('mask', mask)
		param = [transform_frame]
		cv.setMouseCallback('Zoomferous', self.masker.get_color_from_click, param)


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
		self.k=1.0

	def get_color_from_click(self, event, x, y, flags, param):
		if event == cv.EVENT_LBUTTONDBLCLK:
			super().get_color_from_click(event, x, y, flags, param)

			self.lower_color[0] = (self.ink_color[0]-10) % 180
			self.upper_color[0] = (self.ink_color[0]+10) % 180
			print("picking", self.lower_color, "to", self.upper_color, f"from {x}, {y}")

	def show_masked_frame(self, frame):
		gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
		warped = cv.GaussianBlur(gray, (3, 3), 0)
		T=threshold_local(warped,5,offset=self.k/100,method='gaussian')
		# T = threshold_sauvola(warped,3,k=self.k/1000,r=None)
		warped = (warped > T).astype("uint8") * 255
		warped=cv.bitwise_not(warped)

		hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

		mask1 = cv.inRange(hsv, np.array(self.lower_color), np.array(self.upper_color))
		masked_frame = cv.bitwise_and(frame, frame, mask=mask1)
		return warped, masked_frame
	def nothing(self,x):
		self.k=x

		
	