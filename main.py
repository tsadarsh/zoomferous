import zoomferous
import key_bindings


app = zoomferous.Core()
cap = app.VideoCapture(0)

while True:
	app.run_zoomferous(cap)
	key_bindings.listen(app)
