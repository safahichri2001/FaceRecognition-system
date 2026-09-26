# Face Recognition Access Control

Real-time facial recognition access control with **liveness detection**, deployed in a
live coworking space and connected to the space's mobile reservation app.

*Bachelor's final year project (2023 – 2024) — Future Vision Association.
Built by Safa Hichri and Lamiss Khalfallah.*

| | |
|---|---|
| **Recognition accuracy** | 92% |
| **Detection time** | under 1 second |
| **Anti-spoofing** | printed photos and screens are rejected |

---

## How it works

The system has two parts:

```
                  ┌──────────────────────────────┐
  Webcam ───────► │  Desk app (main.py, Tkinter) │ ──► access_history/<user>.txt
                  │  1. liveness check           │
                  │  2. face identification      │
                  └──────────────────────────────┘
                                 ▲ face encodings (db/)
                  ┌──────────────┴───────────────┐
  Mobile app ───► │  REST API (FastAPI)          │
                  │  register · update · delete  │
                  │  access history              │
                  └──────────────────────────────┘
```

**Login flow**

1. The desk app captures the current webcam frame.
2. **Liveness check** — the frame is scored by a face liveness-detection model hosted on
   Hugging Face. A score below `0.5` is treated as a spoof (printed photo, screen) and
   access is denied *before* any identification happens.
3. **Identification** — the live face is encoded with `face_recognition` and compared to
   the registered encodings.
4. The login (or logout) time is appended to the user's access history.

## Components

| File | Role |
|---|---|
| [`main.py`](main.py) | Desk application: live webcam feed, login / logout, liveness check |
| [`register.py`](register.py) | `POST /register` — registers a user from a photo, rejects faces already registered |
| [`update.py`](update.py) | `POST /update_photo` — replaces a user's photo |
| [`delete.py`](delete.py) | `DELETE /delete_user` — removes a user's photo and face encoding |
| [`history.py`](history.py) | `GET /access_history` — returns the access history to the mobile app |

## Getting started

```bash
pip install -r requirements.txt

# Desk application (needs a webcam)
python main.py

# API used by the mobile app — one service per file, e.g.
uvicorn register:app --port 8000
```

> `face_recognition` depends on `dlib`, which needs CMake and a C++ compiler to install.

## Privacy

Faces and access logs are personal data. They are **stored locally only**
(`db/` and `access_history/`) and are **excluded from version control** by `.gitignore`.

Note that the liveness check sends the captured frame to a third-party service hosted on
Hugging Face — in a production deployment, this should be replaced by a model running
on-premise.

## Known limitations

This is a student project; the following would need to be addressed before any
production use:

- **No authentication on the API** — anyone on the network can register, delete users or
  read the access history.
- **Unvalidated usernames** — the username is used directly in file paths, which allows
  path traversal.
- **Photo updates don't refresh the encoding** — `update_photo` replaces the image but the
  desk app keeps recognizing the previous face encoding.
- **Logout skips the liveness check** — only login is protected against spoofing.
- **Encodings are stored with `pickle`**, which must never be loaded from untrusted files.
