import picoweb
import csvwriter
import uasyncio as asyncio
import PlateDetection
import _thread


app = picoweb.WebApp(__name__)



@app.route('/')
def index(req, resp):
    headers = {"Location": "/detection_history"}
    yield from picoweb.start_response(resp, status="302", headers=headers)



@app.route('/detection_history')
def history(req, resp):
    yield from picoweb.start_response(resp)
    yield from app.render_template(resp, "index.html", (csvwriter.readPlatesFromDetection(),))
    


@app.route('/allowed_plates')
def allowed_plates(req, resp):
    yield from picoweb.start_response(resp)
    yield from app.render_template(resp, "allowedPlates.html", (csvwriter.getPlatesFromMemory(),))
    


@app.route('/allowed_plates/add', methods=['POST'])
def allowed_plates_add(req, resp):
    if req.method == "POST":
        yield from req.read_form_data()
    else:  # GET, apparently
        # Note: parse_qs() is not a coroutine, but a normal function.
        # But you can call it using yield from too.
        req.parse_qs()
    csvwriter.addAuthPlate(req.form['plate'])
    headers = {"Location": "/allowed_plates"}
    yield from picoweb.start_response(resp, status="302", headers=headers)


@app.route('/allowed_plates/remove', methods=['POST'])
def allowed_plates_remove(req, resp):
    if req.method == "POST":
        yield from req.read_form_data()
    else:  # GET, apparently
        # Note: parse_qs() is not a coroutine, but a normal function.
        # But you can call it using yield from too.
        req.parse_qs()
    csvwriter.removePlate(req.form['plate'])
    headers = {"Location": "/allowed_plates"}
    yield from picoweb.start_response(resp, status="302", headers=headers)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(PlateDetection.main())
    app.run(host='0.0.0.0', port=5010, debug=True)
    