import face_recognition
import cv2
from PIL import ImageDraw, Image
import numpy
import json
from FaceSaveScp import create_connection, saveDb, findDb

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        frame_count = 0
        ret, frame = self.video.read()
        fr_resized = cv2.resize(frame, (640,480))
        encodingBox=[]
        while True:
            frame_count+=1
            if frame_count % 20 == 0:
                #change encoding from bgr to rgb for face_rec lib
                colorM = cv2.cvtColor(fr_resized, cv2.COLOR_BGR2RGB)

                #getting face locations and encodings
                face_locations = face_recognition.face_locations(colorM,model="hog")
                encodings = face_recognition.face_encodings(colorM, face_locations)
                face_landmarks_list = face_recognition.face_landmarks(colorM)
                #arr2 = encodings.tolist()


                #db operations
                #saveDb("belit",encodings)
                print(findDb(encodings))


                # face_rects = face_cascade.detectMultiScale(gray, 1.3, 5)
                # if len(face_rects)!=0:
                #     print(type(face_rects))
                # else:
                #     print("No Face")
                #print(encodings)


                #drawing on image part
                for (x, y, w, h) in face_locations:
                    cv2.rectangle(fr_resized, (h,x), (y,w), (0, 255, 255), 2)
                    break
                pil_image = Image.fromarray(fr_resized)
                d = ImageDraw.Draw(pil_image)
                for face_landmarks in face_landmarks_list:
                    for facial_feature in face_landmarks.keys():
                        d.line(face_landmarks[facial_feature], width=5)
                fr_resized = numpy.array(pil_image)
                ret, jpeg = cv2.imencode('.jpg', fr_resized,[0,64])
                return jpeg.tobytes()

