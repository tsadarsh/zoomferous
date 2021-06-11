from videofeed_draw import Freecom
import key_bindings


app = Freecom()
cap = app.create_videocapture_object()
while True:
	app.run_zoomferous(cap)
	key_bindings.listen(app)