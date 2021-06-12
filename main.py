from videofeed_draw import Freecom, Mask_from_ink_color
import key_bindings
import cv2 as cv
import os
app = Freecom()
a=Mask_from_ink_color()
cv.namedWindow('mask')
cv.createTrackbar('k','mask',0,500,app.masker.nothing)

while True:
	app.run_zoomferous()
	key_bindings.listen(app)
