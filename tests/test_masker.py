import os

from videofeed_draw import Freecom
import key_bindings


def test():
	os.chdir(os.getcwd() + '/tests/images')
	images = os.listdir()

	app = Freecom()

	for image in images:
		app.test_run_zoomferous(os.getcwd() + '/' + image)
		key_bindings.listen(app)
