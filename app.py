from flask import Flask, render_template, Response
from cam import VideoCamera


app = Flask(__name__)


@app.route('/')
@app.route('//<name>')
def index(name=None):
    # rendering webpage
    return render_template('index.html',name='Belit')

def generate_cam(camera):
    while True:
        #Get kamera
        frame = camera.get_frame()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')\

@app.route('/video')
def video():
    return Response(generate_cam(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
if __name__ =='__main__':
    # server definition
    app.run(host='0.0.0.0')