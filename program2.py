import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QSize
import face_recognition
import cv2
import numpy as np
import sys
import tkinter as tk
from tkinter import filedialog
def LoadImage(ImagePath):
    image = face_recognition.load_image_file(ImagePath)
    face_encoding = face_recognition.face_encodings(image)[0]
    return face_encoding    

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.setMinimumSize(QSize(500, 200))    
        self.setWindowTitle("Face Recognition Program") 

        self.nameLabel = QLabel(self)
        self.nameLabel.setText("""Name of the person to be recognized:""")
        self.line = QLineEdit(self)

        self.UiComponents() 

        self.line.move(200, 20)
        self.line.resize(200, 32)
        self.nameLabel.move(10, 20)
        self.nameLabel.resize(180, 15)

        pybutton = QPushButton('OK', self)
        pybutton.clicked.connect(self.clickMethod)
        pybutton.resize(200,32)
        pybutton.move(200, 60)        

    def UiComponents(self): 
  
        # creating label 
        label1 = QLabel("For exit from video press c", self) 
  
        # setting geometry to the label 
        label1.setGeometry(200, 100, 150, 50) 
  
    def clickMethod(self):
        name =   self.line.text()
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename()
        video_capture = cv2.VideoCapture(0)
        LoadImage(file_path)

        face_encoding = LoadImage(file_path)
        familiar_face_encodings = [
            face_encoding

        ]
        familiar_face_names = [
            name
        ]
        face_locations = []
        face_encodings = []
        face_names = []
        process_this_frame = True
        
        while True:
            ret, frame = video_capture.read()

            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

            rgb_small_frame = small_frame[:, :, ::-1]

            if process_this_frame:
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

                face_names = []
                for face_encoding in face_encodings:
                    matches = face_recognition.compare_faces(familiar_face_encodings, face_encoding)
                    name = "Unknown"

                    face_distances = face_recognition.face_distance(familiar_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = familiar_face_names[best_match_index]

                    face_names.append(name)

            process_this_frame = not process_this_frame


            for (top, right, bottom, left), name in zip(face_locations, face_names):
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            cv2.imshow('Video', frame)

            if cv2.waitKey(1) & 0xFF == ord('c'):
                break
        
        video_capture.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit( app.exec_() )