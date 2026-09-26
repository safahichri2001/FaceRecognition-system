import os
import datetime
import pickle
import tkinter as tk
import tkinter.messagebox

import cv2
import numpy as np
import face_recognition
from PIL import Image, ImageTk
from gradio_client import Client, file

# Hosted liveness-detection model (Hugging Face Space)
LIVENESS_SPACE = "https://faceonlive-face-liveness-detection-sdk.hf.space/"
# Below this score, the capture is treated as a spoof (photo, screen...)
LIVENESS_THRESHOLD = 0.5


class App:
    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.geometry("1200x520+350+100")

        self.login_button_main_window = self.get_button(self.main_window, 'login', 'green', self.login)
        self.login_button_main_window.place(x=750, y=200)

        self.logout_button_main_window = self.get_button(self.main_window, 'logout', 'red', self.logout)
        self.logout_button_main_window.place(x=750, y=300)

        self.webcam_label = self.get_img_label(self.main_window)
        self.webcam_label.place(x=10, y=0, width=700, height=500)

        self.add_webcam(self.webcam_label)

        self.db_dir = './db'
        if not os.path.exists(self.db_dir):
            os.mkdir(self.db_dir)
        self.access_history_dir = './access_history'
        if not os.path.exists(self.access_history_dir):
            os.makedirs(self.access_history_dir)

        self.known_face_encodings = []
        self.known_face_names = []
        self.load_data()

        self.gradio_client = Client(LIVENESS_SPACE)

    def add_webcam(self, label):
        if 'cap' not in self.__dict__:
            self.cap = cv2.VideoCapture(0)
        self._label = label
        self.process_webcam()

    def process_webcam(self):
        ret, frame = self.cap.read()
        self.most_recent_capture_arr = frame

        img_ = cv2.cvtColor(self.most_recent_capture_arr, cv2.COLOR_BGR2RGB)
        self.most_recent_capture_pil = Image.fromarray(img_)
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        self._label.imgtk = imgtk
        self._label.configure(image=imgtk)
        self._label.after(20, self.process_webcam)

    def login(self):
        unknown_img_path = './.tmp.jpg'
        cv2.imwrite(unknown_img_path, self.most_recent_capture_arr)

        # Liveness check first: reject photos and screens before identifying anyone
        result = self.gradio_client.predict(frame=file(unknown_img_path), api_name="/face_liveness")
        if 'data' not in result:
            self.msg_box('Ups...', 'Liveness check unavailable. Please try again.')
            os.remove(unknown_img_path)
            return

        liveness_score = result['data']['liveness_score']
        print(f"Liveness Score: {liveness_score:.2f}")

        if liveness_score == 0.0:
            self.msg_box('No Face Detected', 'No face detected. Please try again.')
            os.remove(unknown_img_path)
            return
        if liveness_score < LIVENESS_THRESHOLD:
            self.msg_box('Spoof detected', 'User is likely a spoof. Access denied.')
            os.remove(unknown_img_path)
            return

        # Live face confirmed: identify the user
        unknown_image = face_recognition.load_image_file(unknown_img_path)
        unknown_encoding = face_recognition.face_encodings(unknown_image)

        if len(unknown_encoding) == 0:
            self.msg_box('Ups...', 'No face detected. Please try again.')
            os.remove(unknown_img_path)
            return

        unknown_encoding = unknown_encoding[0]
        matches = face_recognition.compare_faces(self.known_face_encodings, unknown_encoding)

        if True in matches:
            first_match_index = matches.index(True)
            name = self.known_face_names[first_match_index]
            self.msg_box('Welcome back !', f'Welcome, {name}.')
            user_history_path = os.path.join(self.access_history_dir, f'{name}.txt')

            with open(user_history_path, 'a') as f:
                f.write('Login: {}\n'.format(datetime.datetime.now()))
        else:
            self.msg_box('Ups...', 'Unknown user. Please register new user or try again.')

        os.remove(unknown_img_path)

    def logout(self):
        unknown_img_path = './.tmp.jpg'
        cv2.imwrite(unknown_img_path, self.most_recent_capture_arr)
        unknown_image = face_recognition.load_image_file(unknown_img_path)
        unknown_encoding = face_recognition.face_encodings(unknown_image)

        if len(unknown_encoding) == 0:
            self.msg_box('Ups...', 'No face detected. Please try again.')
            os.remove(unknown_img_path)
            return

        unknown_encoding = unknown_encoding[0]
        matches = face_recognition.compare_faces(self.known_face_encodings, unknown_encoding)

        if True in matches:
            first_match_index = matches.index(True)
            name = self.known_face_names[first_match_index]

            user_history_path = os.path.join(self.access_history_dir, f'{name}.txt')
            with open(user_history_path, 'a') as f:
                f.write('Logout: {}\n'.format(datetime.datetime.now()))

            self.msg_box('Goodbye !', f'Goodbye, {name}.')
        else:
            self.msg_box('Ups...', 'Unknown user. Please register new user or try again.')

        os.remove(unknown_img_path)

    def start(self):
        self.main_window.mainloop()

    def msg_box(self, title, description):
        tkinter.messagebox.showinfo(title, description)

    def load_data(self):
        # Load the face encodings registered through the API (register.py)
        for filename in os.listdir(self.db_dir):
            if filename.endswith('_encoding.pkl'):
                with open(os.path.join(self.db_dir, filename), 'rb') as f:
                    encoding = pickle.load(f)
                    name = filename.split('_encoding.pkl')[0]
                    self.known_face_encodings.append(encoding)
                    self.known_face_names.append(name)
            elif filename.endswith('_encoding.npy'):
                encoding = np.load(os.path.join(self.db_dir, filename))
                name = filename.split('_encoding.npy')[0]
                self.known_face_encodings.append(encoding)
                self.known_face_names.append(name)

    @staticmethod
    def get_button(window, text, color, command, fg='white'):
        button = tk.Button(window, text=text, activebackground="black", activeforeground="white", fg=fg, bg=color,
                           command=command, height=2, width=20, font=('Helvetica bold', 20))
        return button

    @staticmethod
    def get_img_label(window):
        label = tk.Label(window)
        label.grid(row=0, column=0)
        return label


if __name__ == "__main__":
    app = App()
    app.start()
