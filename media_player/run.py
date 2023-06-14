import os
import subprocess
import sys

pid = os.fork()

if pid:
   face_detect_ps = subprocess.Popen(args=[sys.executable, "facedetection.py"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
   print(face_detect_ps.communicate())
else:
    player_ps = subprocess.Popen(args=[sys.executable, "updated_happy_detector.py"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    print(player_ps.communicate()) 
