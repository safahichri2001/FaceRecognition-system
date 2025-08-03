'''import os
import datetime
import tkinter as tk
import cv2
from PIL import Image, ImageTk
import numpy as np
import face_recognition
import pickle
import tkinter.messagebox


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

        # Vérification de l'identité
        unknown_image = face_recognition.load_image_file(unknown_img_path)
        unknown_encoding = face_recognition.face_encodings(unknown_image)

        if len(unknown_encoding) == 0:
            self.msg_box('Ups...', 'No face detected. Please try again.')
            os.remove(unknown_img_path)
            return

        unknown_encoding = unknown_encoding[0]
        matches = face_recognition.compare_faces(self.known_face_encodings, unknown_encoding)
        name = "Unknown"

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
        name = "Unknown"

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

    def add_img_to_label(self, label):
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        label.imgtk = imgtk
        label.configure(image=imgtk)
        self.register_new_user_capture = self.most_recent_capture_arr.copy()

    def start(self):
        self.main_window.mainloop()

    def msg_box(self, title, description):
        tkinter.messagebox.showinfo(title, description)

    def load_data(self):
        # Chargement des encodages et des noms des visages enregistrés
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

    def save_data(self):
        # Sauvegarde des encodages et des noms des visages enregistrés
        data = {'encodings': self.known_face_encodings, 'names': self.known_face_names}
        with open(os.path.join(self.db_dir, 'face_encodings.pkl'), 'wb') as f:
            pickle.dump(data, f)

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

    @staticmethod
    def get_text_label(window, text):
        label = tk.Label(window, text=text)
        label.config(font=("sans-serif", 21), justify="left")
        return label

    @staticmethod
    def get_entry_text(window):
        inputtxt = tk.Text(window, height=2, width=15, font=("Arial", 32))
        return inputtxt

    def get_user_access_history_path(self, name):
        return f'{name}.txt'


if __name__ == "__main__":
    app = App()
    app.start()'''
import datetime
import tkinter as tk
import cv2
from PIL import Image, ImageTk
import numpy as np
import face_recognition
import pickle
import tkinter.messagebox
from gradio_client import Client, file


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

        self.gradio_client = Client("https://faceonlive-face-liveness-detection-sdk.hf.space/")

    def spoof_window(self):
        spoof_window = tk.Toplevel(self.main_window)
        spoof_window.geometry("200x100+600+300")
        spoof_label = tk.Label(spoof_window, text="Spoof")
        spoof_label.pack(pady=20)

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
    
    # Vérification de la liveness du visage
     result = self.gradio_client.predict(frame=file(unknown_img_path), api_name="/face_liveness")
     if 'data' in result:
        liveness_score = result['data']['liveness_score']
        print(f"Liveness Score: {liveness_score:.2f}")

        if liveness_score == 0.0:
            self.msg_box('No Face Detected', 'No face detected . Please try again.')
            os.remove(unknown_img_path)
            return
        elif liveness_score < 0.5:  # Seuil de liveness pour déterminer si c'est un spoof
            self.msg_box('Spoof detected', 'User is likely a spoof. Access denied.')
            os.remove(unknown_img_path)
            return
        else:
            # Liveness confirmé, procéder à la vérification de l'identité
            unknown_image = face_recognition.load_image_file(unknown_img_path)
            unknown_encoding = face_recognition.face_encodings(unknown_image)

            if len(unknown_encoding) == 0:
                self.msg_box('Ups...', 'No face detected. Please try again.')
                os.remove(unknown_img_path)
                return

            unknown_encoding = unknown_encoding[0]
            matches = face_recognition.compare_faces(self.known_face_encodings, unknown_encoding)
            name = "Unknown"

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
        name = "Unknown"

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

    def add_img_to_label(self, label):
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        label.imgtk = imgtk
        label.configure(image=imgtk)
        self.register_new_user_capture = self.most_recent_capture_arr.copy()

    def start(self):
        self.main_window.mainloop()

    def msg_box(self, title, description):
        tkinter.messagebox.showinfo(title, description)

    def load_data(self):
        # Chargement des encodages et des noms des visages enregistrés
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

    def save_data(self):
        # Sauvegarde des encodages et des noms des visages enregistrés
        data = {'encodings': self.known_face_encodings, 'names': self.known_face_names}
        with open(os.path.join(self.db_dir, 'face_encodings.pkl'), 'wb') as f:
            pickle.dump(data, f)

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

    @staticmethod
    def get_text_label(window, text):
        label = tk.Label(window, text=text)
        label.config(font=("sans-serif", 21), justify="left")
        return label

    @staticmethod
    def get_entry_text(window):
        inputtxt = tk.Text(window, height=2, width=15, font=("Arial", 32))
        return inputtxt

    def get_user_access_history_path(self, name):
        return f'{name}.txt'

    def predict_face_liveness(self, user_img_path):
        result = self.gradio_client.predict(frame=file(user_img_path), api_name="/face_liveness")
        print("Result:", result)
        if 'data' in result:
            liveness_score = result['data']['liveness_score']
            print("Liveness Score:", liveness_score)
            if liveness_score < 0.5:  # Adapté en fonction du seuil désiré
                print("User is likely a spoof")
                self.spoof_window()
            else:
                print("User is likely not a spoof")
        else:
            print("No liveness information found in result")


if __name__ == "__main__":
    app = App()
    app.start()
