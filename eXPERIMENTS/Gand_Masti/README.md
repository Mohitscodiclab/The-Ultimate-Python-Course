# 🔐 UI Vault – Secure Encrypted Folder Locker

A GUI-based secure vault system built with Python that protects sensitive files using strong cryptography, authentication, auto-locking, and recovery mechanisms.

Developed as part of the experiments in
The-Ultimate-Python-Course by
Mohitscodiclab

---

## 📌 Overview

UI Vault is a cyber-security focused application designed to ensure **data-at-rest protection** through:

* AES-256 encryption
* Password-based authentication
* Recovery question system
* Auto-lock on inactivity
* Secure first-time initialization
* GUI session control

The system ensures that files remain encrypted and inaccessible without proper authentication — even if the application is closed.

---

## 🎯 Objectives

* Protect confidential user files
* Implement real-world encryption workflow
* Demonstrate secure authentication design
* Apply inactivity-based session locking
* Build a modular, scalable architecture

---

# 🧠 Security Model

### 🔑 Encryption

* AES-256 GCM (authenticated encryption)
* Scrypt key derivation
* Random salt & nonce

### 🔐 Authentication

* SHA-256 hashed password
* Hashed recovery answer
* First-run secure setup

### ⏱ Session Protection

* Auto-lock on inactivity
* Auto-lock on window close
* Lock on focus loss

### 🛡 Data Protection

* Files encrypted at rest
* No plaintext credential storage
* Config isolation in system directory

---

# 🗂 Folder Structure

```
UI_vault/
│── locker.py
│── requirements.txt
│
├── core/
│   ├── auth.py
│   ├── config_manager.py
│   ├── crypto_utils.py
│   ├── vault_handler.py
```

---

# ⚙️ Module Description

## 🔐 core/auth.py

Handles:

* Password hashing
* Credential verification
* Password reset
* Recovery question updates

---

## 🧾 core/config_manager.py

Responsible for:

* Secure config creation
* Config read/write
* First-run detection

---

## 🔑 core/crypto_utils.py

Implements:

* AES file encryption
* AES file decryption
* Key derivation using Scrypt

This is the **core security engine**.

---

## 📂 core/vault_handler.py

Controls:

* Vault creation
* Locking files (encryption)
* Unlocking files (decryption)

---

## 🖥 locker.py

Main GUI controller:

* First-time setup flow
* Unlock workflow
* Forgot password workflow
* Auto-lock engine
* Activity tracking
* Session state management

---

# 🚀 Installation

### 1️⃣ Clone the repository

```bash
git clone https://github.com/Mohitscodiclab/The-Ultimate-Python-Course.git
cd UI_vault
```

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Run the application

```bash
python locker.py
```

---

# 🧪 First-Time Setup Flow

On first run:

1. Create new password
2. Confirm password
3. Set recovery question
4. Set recovery answer
5. Vault opens

After setup, these options appear:

* Unlock Folder
* Forget Password
* Exit

---

# 🔄 Forgot Password Flow

1. Answer security question
2. Set new password
3. Optionally update recovery question

---

# ⏱ Auto-Lock Behaviour

Vault locks automatically when:

* User inactive for defined time
* Application window loses focus
* Application is closed

---

# 🧑‍💻 Technologies Used

* Python
* Tkinter (GUI)
* Cryptography library
* JSON (secure config storage)
* Threading (background auto-lock)

---

# 📊 Use Cases

* Personal secure storage
* Cyber-security academic project
* Demonstration of data-at-rest protection
* Encryption workflow learning

---

# ⚠️ Security Considerations

This system protects **data at rest**.

If an attacker has full OS-level control, they can:

* Delete the application
* Modify runtime environment

However, encrypted vault data **remains inaccessible without the password**.

---

# 🔮 Future Enhancements

### 🔐 Security

* Brute-force protection with exponential delay
* Two-factor authentication (OTP / USB key)
* Biometric unlock integration
* Decoy password (honeypot vault)

### 📜 Monitoring

* Vault access logs
* Failed attempt alerts
* Session history panel

### 🧠 UX Improvements

* Drag & drop file support
* File preview inside vault
* Password strength meter
* Dark / hacker theme UI

### 📦 Deployment

* One-click EXE build
* Installer with system integration
* Portable encrypted vault

### ☁ Advanced

* Secure cloud sync (end-to-end encrypted)
* Multi-user vault with role separation

---

# 📚 References

* NIST – Recommendation for Block Cipher Modes of Operation
* OWASP – Cryptographic Storage Guidelines
* Python Cryptography Documentation
* Ferguson, Schneier & Kohno – *Cryptography Engineering*
* Menezes et al. – *Handbook of Applied Cryptography*

---

# ✅ Conclusion

UI Vault demonstrates how secure software should be designed:

* Encryption is applied before access control
* Authentication never stores plaintext secrets
* Sessions are time-bound and monitored
* Recovery mechanisms are controlled and verifiable

This project moves beyond a basic folder locker and implements a **real data-protection model aligned with modern cyber-security practices**.

---

# ⭐ Author

**Mohit Kumar**
GitHub: Mohitscodiclab

---

# 🏆 Academic Value

This project showcases:

* Secure application architecture
* Practical cryptography implementation
* GUI + security integration
* Real-world threat-aware design

Making it suitable for:

✔ Cyber-security coursework
✔ Final year mini project
✔ Portfolio demonstration

---

## ☕ Support the Project

If you find this project helpful, consider supporting my work:

**Buy Me a Coffee:**
👉 [https://buymeacoffee.com/mohitscodiclab](https://buymeacoffee.com/mohitscodiclab)

Your support helps in building more open-source cyber-security tools, educational experiments, and advanced Python projects.

---

## 👨‍💻 Author

**Mohit Kumar**
GitHub: Mohitscodiclab
Buy Me a Coffee: [https://buymeacoffee.com/mohitscodiclab](https://buymeacoffee.com/mohitscodiclab)

---

## 🌟 Show Your Support

If you like this project:

⭐ Star the repository
🍴 Fork it
☕ Support via Buy Me a Coffee
🛠 Contribute to future features
