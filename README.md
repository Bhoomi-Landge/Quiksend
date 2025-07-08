# Quiksend 📧

**Quiksend** is a lightweight email marketing web application that allows users to efficiently send bulk emails to large subscriber lists. It provides user-friendly tools to create, customize, and edit HTML email templates — making email campaigns faster, smarter, and more effective.

---

## 🔧 Built With

- **Frontend:** HTML, CSS  
- **Backend:** Python (Flask)   
- **Templating:** Jinja2  
- **Mailing:** SMTP (via Flask-Mail or similar)

---

## 🚀 Features

- ✅ Send bulk emails with ease  
- ✅ Create and edit custom HTML email templates  
- ✅ Save and manage multiple templates  
- ✅ Manage subscriber lists  
- ✅ Simple and clean UI  
- ✅ Built with Flask (Python backend)  

## 📁 Project Structure

```
Quiksend/
├── static/                # CSS files and assets
├── templates/             # HTML email templates and UI
├── app.py                 # Flask application
├── config.py              # SMTP and app configurations
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation
```

---

## ⚙️ Installation

1. **Clone the repository**


git clone https://github.com/Bhoomi-Landge/Quiksend.git
cd Quiksend


2. **Create virtual environment (optional but recommended)**

python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`


3. **Install dependencies**

pip install -r requirements.txt


4. **Set your environment variables**  
   (Create a `.env` file or update `config.py` directly with your SMTP credentials)
   
MAIL_SERVER=smtp.example.com
MAIL_PORT=587
MAIL_USERNAME=your-email@example.com
MAIL_PASSWORD=your-password
MAIL_USE_TLS=True

5. **Run the app**

python app.py


Then go to `http://127.0.0.1:5000` in your browser.

## 📸 Screenshots

## 💡 Future Enhancements
  
- 📊 Email analytics (open/click rates)  
- 🗓️ Email scheduling  
- 🧠 AI-based subject line and content suggestions


