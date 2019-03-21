#!/usr/bin/python3
import os
import time
import argparse
import shutil

import numpy as np
import cv2 as cv


face_cascade = cv.CascadeClassifier('/usr/share/OpenCV/haarcascades/haarcascade_frontalface_default.xml')
eye_cascade = cv.CascadeClassifier('/usr/share/OpenCV/haarcascades/haarcascade_eye.xml')

def _putText(frame, text, pos_x, pos_y):
    for i, line in enumerate(text.split('\n')):
        y = pos_y + (i-1)*20
        cv.putText(frame, line, (pos_x, y), cv.FONT_HERSHEY_SIMPLEX, 0.8, 255)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--label", default="test", help="name of image to be labeled")
    parser.add_argument("-d", "--dir", default="./person", help="root dir to save labeled image")
    parser.add_argument("-t", "--time", default=10.0, help="Record time (second)")
    parser.add_argument("-s", "--save", help="Save avi video", action="store_true")

    args = parser.parse_args()

    cv.namedWindow('Video',cv.WINDOW_NORMAL)
    cv.resizeWindow('Video', 1024, 768)
    cv.moveWindow('Video', 0, 0)

    camera = cv.VideoCapture(0)
    dirname = os.path.join(args.dir, args.label)
    if os.path.exists(dirname):
        shutil.rmtree(dirname)
    os.makedirs(dirname)


    if args.save:
        frame_width = int(camera.get(3))
        frame_height = int(camera.get(4))
        # Define the codec and create VideoWriter object
        fourcc = cv.VideoWriter_fourcc(*'XVID')
        avi_name = "%s/%s.avi" % (dirname, args.label)
        # Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
        out = cv.VideoWriter(avi_name, cv.VideoWriter_fourcc('M','J','P','G'),
                             15, (frame_width,frame_height))

    i = 0
    image = ""
    start_time = time.time()
    while True:
        now = time.time()
        if (cv.waitKey(1) & 0xFF == ord('q')) or (start_time + float(args.time) < now):
            print("In %d seconds, record %s %d images to %s" %
                   (int(args.time), args.label, i, dirname))
            break

        rv, frame = camera.read()
        if rv:
            gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(frame, 1.3, 5)
            for (x,y,w,h) in faces:
                if (x > 50 and y > 50):
                    image = "%s/face_%d.jpg" % (dirname, i)
                    cv.imwrite(image, frame[y-50:y+h+50, x:x+w])
                    cv.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)

                    text = "Recording %s" % args.label
                    _putText(frame, text, x-50, y-50)
                    i += 1
                # Record first recognize face
                continue
            if args.save:
                out.write(frame)
            cv.imshow('Video', frame)

    # When everything done, release the capture
    camera.release()
    if args.save:
        out.release()
    cv.destroyAllWindows()