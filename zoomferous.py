from sys import exit
import numpy as np
import cv2 as cv
from skimage.filters import threshold_sauvola
from skimage.filters.rank import core_cy_3d
from time import asctime as current_time

import quadrilateral_sort


class Core:
	def __init__(self):
		self.cap = None
		self.frame = None
		self.transformed_frame = None
		self.current_frame_in_window = None
		self.cam_height = None
		self.cam_width = None
		self.color_frame = None
		self.corner_points_cords = []
		self.corner_points = None
		self.masker = Mask_from_skimage()

	def VideoCapture(self, cid=0):
		"""Returns a videoCapture object.

		Video capture object is used to obtain frames form the video
		camera. Provide camera-id to choose different camera (default is
		primary webcam of device).
		"""
		cap = cv.VideoCapture(cid)
		if not cap.isOpened():
			print("Cannot open camera")
			exit()

		self.__update_parameters(cap)

		return cap

	def __update_parameters(self, cap):
		self.cap = cap
		self.cam_height = self.get_camera_height(cap)
		self.cam_width = self.get_camera_width(cap)
		self.color_frame = self.create_blank_overlay(
			self.cam_height, self.cam_width)
		self.color_frame[:] = [255, 255, 255]
		self.corner_points = self.create_blank_overlay(
			self.cam_height, self.cam_width)

	def get_camera_height(self, cap):
		return int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))

	def get_camera_width(self, cap):
		return int(cap.get(cv.CAP_PROP_FRAME_WIDTH))

	def run_zoomferous(self, cap):
		"""Starting point for Zoomferous operations

		After creating a videoCapture object call this method inside a
		`while True` block. This method first checks if the four corner
		points are selected. If number of corner points are less than 4
		the method for overlaying the selected points as red-rings on
		top of the frame is called. If 4 corner points are selected, the
		method for obtainig the transformed frame is called. This method
		returns a greyscale image. The next method adds color to this
		frame.
		"""
		self.frame = self.get_camera_frame(cap)

		if len(self.corner_points_cords) < 4:
			self.selecting_corner_points()
		else:
			transformed_frame = self.make_transformed_frame(
				self.frame, self.corner_points_cords,
				self.cam_height, self.cam_width)
			masked_frame = self.masker.show_masked_frame(transformed_frame)
			colored_frame = self.add_color_to_frame(
				masked_frame, self.color_frame)
			self.show_frame(colored_frame)

	def test_run_zoomferous(self, image_source):
		"""Tests use this method instead for `run_zoomferous`.

		Instead of using the videoCapture object the tests are run on
		images saved in tests/images. During tests use `q` to run next
		test.
		"""
		self.frame = cv.imread(image_source)

		cv.imshow('feed', self.frame)
		mask, color_masked = self.masker.show_masked_frame(self.frame)
		cv.imshow('result', mask)

		wait = cv.waitKey(0)

	def get_camera_frame(self, cap):
		"""Returns frame from provided VideoCapture object"""
		ret, frame = cap.read()

		if not ret:
			print("Can't recieve frame..")

		return frame

	def create_blank_overlay(self, height, width):
		"""Returns a black frame of specified height and width."""
		return np.zeros((height, width, 3), np.uint8)

	def selecting_corner_points(self):
		"""This method is called when the selected number of corner
		points is less than 4. Mouse binding for selecting the points
		is also set here.
		"""
		frame_with_corner_points = self.make_frame_with_selected_corner_points(
			self.frame, self.corner_points)
		self.show_frame(frame_with_corner_points)
		cv.setMouseCallback('Zoomferous', self.draw_corner_points)

	def draw_corner_points(self, event, x, y, flags, param):
		"""On mouse click event the co-ordinates of the mouse pointer
		is stored. A red-ring is drawn on a blank frame at the same
		co-ordinates.
		"""
		if event == cv.EVENT_LBUTTONDOWN:
			print(f'drawing point at {x},{y}')
			self.corner_points_cords.append([x, y])
			cv.circle(self.corner_points, (x, y), 10, (0, 0, 255), 3)

	def make_frame_with_selected_corner_points(self, frame, corner_points):
		"""The frame with selected corner points as red-rings is
		overlayed on top of the frame and returned.
		"""
		corner_points_mask = cv.inRange(corner_points, np.array([0,0,254]), np.array([0,0,256]))
		inv_corner_points_mask = cv.bitwise_not(corner_points_mask)
		frame_without_corner_points = cv.bitwise_and(frame, frame, mask=inv_corner_points_mask)
		frame_with_corner_points = cv.add(frame_without_corner_points, corner_points)

		return frame_with_corner_points

	def make_transformed_frame(self, frame, corner_points_cords, height, width):
		"""Returns frame after perspectve wraping.

		The given frame with the corner points is transformed to get the
		view when the camera is facing directly above the workspace.
		"""
		sorted_corner_points_cords = quadrilateral_sort.tl_tr_bl_br(corner_points_cords)
		pts1 = np.float32(sorted_corner_points_cords)
		pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
		transform_frame_matrix = cv.getPerspectiveTransform(pts1, pts2)
		transformed_frame = cv.warpPerspective(frame, transform_frame_matrix, (width, height))

		return transformed_frame

	def add_color_to_frame(self, frame, color_frame):
		"""Returns colored frame from greyscale image

		The input image is is bitwise added with a blank frame with a
		single solid color.
		"""
		mask_bgr = cv.cvtColor(frame, cv.COLOR_GRAY2BGR)
		colored_frame = cv.bitwise_and(mask_bgr, color_frame, mask=frame)

		return colored_frame

	def show_frame(self, frame, name="Zoomferous"):
		cv.imshow(name, frame)
		self.current_frame_in_window = frame

	def change_ink_color(self, color):
		"""Sets the blank frame with a single solid color"""
		if color == 'w':
			self.color_frame[:] = [255, 255, 255]
		elif color == 'r':
			self.color_frame[:] = [0, 0, 255]
		elif color == 'b':
			self.color_frame[:] = [255, 0, 0] 
		elif color == 'g':
			self.color_frame[:] = [0, 255, 0]

	def save_frame(self, name=None):
		"""Saves frame in working directory.

		Default file name is ascii Date-time. Optional to provide file
		name and file format.
		"""
		if name is None:
			name = current_time() + '.png'
		print(f"Saving frame as {name}")
		cv.imwrite(name, self.current_frame_in_window)

class Mask:
	"""This class holds the structure for masking. Inherit this class
	and provide the logic in `show_masked_frame` method.
	"""
	def __init__(self):
		self.frame = None
		self.ink_color = None

	def get_color_from_click(self, event, x, y, flags, param):
		frame_as_list = param[0][y, x].tolist()
		frame_in_hsv = cv.cvtColor(np.uint8([[frame_as_list]]), cv.COLOR_BGR2HSV)
		self.ink_color = frame_in_hsv.tolist()[0][0]


class Mask_from_ink_color(Mask):
	"""Mask using IN-RANGE technique

	The content from frame is masked by choosing pixels only which lie
	in the provided range.
	"""
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

		return mask

class Mask_from_skimage(Mask):
	"""Mask using SAUVOLA_THRESHOLD technique

	The provided frame is fed to the scikit image library's sauvola
	algorithm"""
	def show_masked_frame(self, frame):
		warped = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

		T = threshold_sauvola(warped, window_size=35, k=0.2)
		warped = (warped > T).astype("uint8") * 255
		warped = cv.bitwise_not(warped)

		return warped
