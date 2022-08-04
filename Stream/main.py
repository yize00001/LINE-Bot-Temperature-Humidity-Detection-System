from flask import Flask, render_template, Response
import cv2
import numpy as np

app = Flask(__name__)

camera = cv2.VideoCapture(-1)  # use 0 for web camera
camera.set(3,565)
camera.set(4,350)

def gen_frames():  # generate frame by frame from camera
    while True:
        # Capture frame-by-frame
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            tmp = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + tmp + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


# @app.route('/')
# def index():
#     """Video streaming home page."""
#     return render_template('main.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8000)
