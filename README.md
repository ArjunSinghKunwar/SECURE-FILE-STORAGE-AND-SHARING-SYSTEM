# Secure File Storage and Sharing System

A secure file storage and sharing system developed using Python. It allows users to register, authenticate, upload and download encrypted files, share them using keys, and revoke access when needed. This system is designed for privacy, integrity, and controlled sharing.

---

## Features

- End-to-end file encryption
- User registration and login
- Secure file upload and download
- Key-based file sharing
- Access revocation mechanism
- Simple and modular codebase

---

## Technologies Used

- Python 3
- SQLite (for lightweight database)
- Cryptographic libraries (e.g., hashlib, os, base64, etc.)
- CLI or basic GUI (Tkinter/Flask if implemented)

---

## Project Structure

Secure-File-Storage-System/
├── encryption/ # Logic for encryption and decryption
├── users/ # User authentication and management
├── storage/ # File upload/download logic
├── revoke/ # File sharing revocation logic
├── db/ # SQLite database operations
├── main.py # Main entry point of the project
├── README.md # Project documentation
└── requirements.txt # Required Python packages (if applicable)

---

## How to Run

1. Clone the repository:

git clone https://github.com/ArjunSinghKunwar/SECURE-FILE-STORAGE-AND-SHARING-SYSTEM.git
cd SECURE-FILE-STORAGE-AND-SHARING-SYSTEM

2. Install the required packages:

pip install -r requirements.txt
(If requirements.txt is not present, manually install required packages like cryptography or hashlib.)

3. Run the application:

python main.py
Security Notes
Files are encrypted before being stored locally or in the database.

Only authenticated users can access or share files.

Shared files require a valid key to open.

Revoked access disables further downloads by the recipient.

Future Improvements
Web-based frontend using Flask or Django

Role-based access control

Integration with cloud storage providers

Time-based or OTP-based access sharing

Email notifications for shared/revoked files

License
This project is developed for educational purposes. 

Author
Arjun Singh Kunwar
Cybersecurity and ISP enthusiast
GitHub: ArjunSinghKunwar

