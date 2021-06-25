import zoomferous
import key_bindings


app = zoomferous.Core()

while True:
	app.run_zoomferous()
	key_bindings.listen(app)
