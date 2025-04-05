# Smart CV Generator - Documentation

This documentation will guide you through the setup, running, and usage of the **Smart CV Generator** web application.

---

## 🚀 Overview
The **Smart CV Generator** is a web-based tool built with **FastAPI** that allows users to enter their professional and personal details via a form and generate a CV in multiple formats (DOCX, PDF, and Image).

---

## ✅ Prerequisites
Ensure you have the following installed:

- **Python** (>=3.8)
- **pip** (Python package manager)

Check via terminal:
```bash
python --version
pip --version
```

If not installed, download Python from [python.org](https://www.python.org/downloads/).

---

## 📁 Project Structure
```
cv-generator/
├── backend/
│   └── main.py              # FastAPI backend logic
├── static/
│   └── styles.css           # Frontend styles
├── templates/
│   └── index.html           # HTML frontend form
├── requirements.txt         # Python dependencies
```

---

## 📦 Installing Dependencies
Navigate to the project root directory and install the required packages:
```bash
cd cv-generator
pip install -r requirements.txt
```

If `requirements.txt` is not created yet, generate it with:
```bash
echo "fastapi\nuvicorn\npython-docx\njinja2" > requirements.txt
```

---

## 🚀 Running the Server
To start the FastAPI development server:
```bash
uvicorn backend.main:app --reload
```

You should see:
```
Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

---

## 🌐 Accessing the Web Application
Open your browser and visit:
```
http://127.0.0.1:8000
```

You'll see the CV Generator form.

---

## ✏️ Using the Form
Fill in the form fields:
- Full Name, Email, Phone
- GitHub, Portfolio
- Career Objective
- Education
- Technical Skills
- Projects
- Strengths
- Personal Details

Choose the desired export format:
- **DOCX**
- **PDF** (Upcoming)
- **Image (PNG)** (Upcoming)

Click **Generate CV** to trigger download.

---

## 📄 Supported Output Formats
- **DOCX**: Generated using `python-docx`
- **PDF**: Coming Soon using `reportlab` or `pdfkit`
- **Image**: Coming Soon using `imgkit` or `html2canvas`

---

## 💡 Tips
- Use the `--reload` flag during development to auto-restart on changes.
- You can add dropdowns or suggestion boxes in the HTML to speed up form filling.

---

## 📤 Hosting on GitHub Pages (Frontend Only)
1. Move all HTML, CSS, and JS files into a `/frontend` folder.
2. Push that folder to a GitHub repo.
3. Go to **Settings > Pages**, select the branch, and `/root` folder.
4. You'll get a public GitHub Pages link.

For the backend:
- Host on [Render](https://render.com), [Railway](https://railway.app), or [Vercel](https://vercel.com) (serverless).
- Update your JS fetch URLs to point to the hosted backend URL.

---

## 📁 To-Do for Enhancements
- Add PDF & PNG output support
- Improve CV formatting with CSS and Word styles
- Allow user login and saved CVs
- Multi-template support

---

## 📬 Need Help?
If you get stuck or want help with deployment or customization, feel free to ask!

