<h1 align="center">🧠 FaceRecognition-System</h1>
<p align="center">
  🔐 An AI-powered facial recognition system with <strong>live spoof detection</strong>, 
  integrated with a mobile app to manage coworking space access and reservations.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.7%2B-blue?logo=python">
  <img src="https://img.shields.io/badge/OpenCV-4.x-red?logo=opencv">
  <img src="https://img.shields.io/badge/face_recognition-Yes-brightgreen">
  <img src="https://img.shields.io/badge/Mobile%20App-Integrated-orange?logo=android">
  <img src="https://img.shields.io/badge/License-MIT-lightgrey?logo=license">
</p>

---
<ul>
  <li>🔐 <strong>User Registration:</strong> Register new users with facial data</li>
  <li>📷 <strong>Real-Time Recognition:</strong> Detect and recognize faces via webcam</li>
  <li>📅 <strong>Access Logging:</strong> Log access and leave times automatically</li>
  <li>📱 <strong>Mobile App Integration:</strong> Connect with mobile app for managing reservations</li>
  <li>📝 <strong>History Management:</strong> View and manage access history via text files</li>
</ul>
## 🔐 Liveness Detection

We use a spoof detection model via <a href="https://huggingface.co/" target="_blank">Hugging Face</a> to ensure that access is granted only to real, live users.  
If a printed photo or screen is detected, access is denied immediately.

---

## 🖥️ GUI Demo

The system includes a simple graphical interface built with <strong>Tkinter</strong>:

- 📷 Live webcam feed  
- 🔓 "Login" and 🔒 "Logout" buttons  
- 🛑 Detection of spoof attempts  
- ✅ Display of success or ❌ error messages  

---

## 📱 Mobile Integration

This system is integrated with a mobile app to:

- 🏢 Manage coworking space reservations  
- ⏱️ Track access and exit times  
- 🔄 Sync logs to a mobile dashboard  

💡 <em>The mobile app handles authentication and scheduling while the face recognition system ensures secure physical access.</em>

---

## 📦 Dependencies

- Python 3.7+  
- OpenCV  
- face_recognition  
- Pillow  

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you’d like to modify or improve.

---

## 🛡️ License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

---

## 📬 Contact

Made with ❤️ by <strong>Safa Hichri and Lamiss khalfallah </strong><br>


