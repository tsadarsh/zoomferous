import numpy as np
import cv2 as cv


class Freecom:
	def __init__(self, cid=0):
		self.cid = cid
		self.cam_width = None
		self.cam_height = None
		self.perspective_crop = []
		self.mask_color_lower = [0, 0, 0]
		self.mask_color_upper = [255, 255, 255]
		self.mask_color_width = 10

	def start_cam(self):
		cap = cv.VideoCapture(self.cid)
		if not cap.isOpened():
			print("Cannot open camera")
			exit()

		# Get camera's width and height
		self.cam_width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
		self.cam_height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))

		# Black background from points
		blank_img = np.zeros((self.cam_height, self.cam_width, 3), np.uint8)

		#create trackbar
		cv.namedWindow('mask_settings')
		cv.createTrackbar('H', 'mask_settings', 0, 360, self.update_hue_mask_value)
		cv.createTrackbar('S', 'mask_settings', 0, 100, self.update_sat_mask_value)
		cv.createTrackbar('V', 'mask_settings', 0, 100, self.update_val_mask_value)
		cv.createTrackbar('W', 'mask_settings', 0, 50, self.update_hsv_mask_width)

		while True:
			ret, frame = cap.read()

			if not ret:
				print("Cant receive frame..")
				break

			if len(self.perspective_crop) < 4:
				cv.imshow('feed', frame)
				cv.imshow('bg', blank_img)
				param = [blank_img]
				cv.setMouseCallback('feed', self.draw_point, param)
			else:
				pts1 = np.float32(self.perspective_crop)
				pts2 = np.float32([[0, 0], [self.cam_width, 0], [0, self.cam_height], [self.cam_width, self.cam_height]])
				transform_frame_matrix = cv.getPerspectiveTransform(pts1, pts2)
				transform_frame = cv.warpPerspective(frame, transform_frame_matrix, (self.cam_width, self.cam_height))
				cv.imshow('new', transform_frame)
				mask_frame = self.show_masked(transform_frame)
				cv.imshow('masked', mask_frame)
			if cv.waitKey(1) == ord('q'):
				self.stop_cam(cap)
				break

	def stop_cam(self, cap):
		cap.release()
		cv.destroyAllWindows()

	def draw_point(self, event, x, y, flags, param):
		if event == cv.EVENT_LBUTTONDBLCLK:
			print(f'event triggered at {x},{y}')
			self.perspective_crop.append([x, y])
			cv.circle(param[0], (x, y), 10, (255, 0, 0), -1)

	def update_hsv_mask_width(self, val):
		self.mask_color_width = val

	def update_hue_mask_value(self, val):
		self.mask_color_lower[0] = val-self.mask_color_width
		self.mask_color_upper[0] = val+self.mask_color_width

	def update_sat_mask_value(self, val):
		self.mask_color_lower[1] = val-self.mask_color_width
		self.mask_color_upper[1] = val+self.mask_color_width

	def update_val_mask_value(self, val):
		self.mask_color_lower[2] = val-self.mask_color_width
		self.mask_color_upper[2] = val+self.mask_color_width

	def show_masked(self, frame):
		#frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
		lower_black = np.array(self.mask_color_lower)
		upper_black = np.array(self.mask_color_upper)
		mask = cv.inRange(frame, lower_black, upper_black)
		res = cv.bitwise_and(frame, frame, mask=mask)
		return mask


app = Freecom()
app.start_cam()
