from videofeed_draw import Freecom
import key_bindings


app = Freecom()

while True:
	app.run_zoomferous()
	key_bindings.listen(app)
