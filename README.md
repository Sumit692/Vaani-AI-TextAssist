# 🧠 VAANI AI – TextAssist

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python" />
  <img src="https://img.shields.io/badge/Flask-Web%20Framework-black?style=for-the-badge&logo=flask" />
  <img src="https://img.shields.io/badge/Google%20Gemini-AI-green?style=for-the-badge&logo=google" />
  <img src="https://img.shields.io/badge/OCR-Tesseract-orange?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Text%20To%20Speech-gTTS-red?style=for-the-badge" />
</p>

---

# 📖 About the Project

**VAANI AI – TextAssist** is an AI-powered accessibility and learning assistant designed to help users understand text extracted from PDF documents. It combines **Optical Character Recognition (OCR)** with **Google Gemini AI** to provide intelligent question answering and uses **Text-to-Speech (TTS)** to make information more accessible.

The application is designed for users who need a simple and interactive way to extract knowledge from documents instead of reading lengthy PDFs manually.

---

# 🎯 Who is this Project Designed For?

VAANI AI – TextAssist is especially useful for:

- 🎓 Students preparing for exams from PDF notes
- 👨‍🏫 Teachers creating learning material
- 📚 Researchers reading long documents
- 👨‍💻 Developers exploring AI-powered document assistants
- ♿ People with visual impairments who benefit from text-to-speech
- 📖 Anyone who wants to ask questions directly from PDF content instead of reading the entire document

---

# ✨ Features

- 📄 Upload PDF documents
- 🔍 Extract text using OCR (Tesseract OCR)
- 🤖 AI-powered question answering using Google Gemini
- 🔊 Convert extracted text into speech
- 🧠 Intelligent document understanding
- 💬 Interactive question-answer interface
- ⚡ Fast and lightweight Flask application
- 🌐 Simple web interface

---

# 🛠️ Tech Stack

### Backend
- Python
- Flask

### AI
- Google Gemini API
- Google Generative AI SDK

### OCR
- Tesseract OCR
- PyMuPDF (fitz)
- Pillow (PIL)

### Text-to-Speech
- Google Text-to-Speech (gTTS)

### Frontend
- HTML5
- CSS3
- JavaScript

---

# 📂 Project Structure

```text
VAANI-AI-TEXTASSIST/
│
├── templates/
│   ├── index.html
│   └── qa.html
│
├── uploads/
├── outputs/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
└── .env (Not included)
```

---

# ⚙️ Installation

### Clone the repository

```bash
git clone https://github.com/Sumit692/Vaani-AI-TextAssist.git
```

Go into the project folder

```bash
cd Vaani-AI-TextAssist
```

Create a virtual environment

```bash
python -m venv venv
```

Activate the environment

Windows

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file in the project root.

```env
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
```

---

# ▶️ Run the Application

```bash
python app.py
```

Open your browser and visit

```
http://127.0.0.1:5000
```

---

# 🚀 How It Works

1. Upload a PDF document.
2. OCR extracts text from the document.
3. Extracted content is processed.
4. Ask questions about the document.
5. Google Gemini generates intelligent responses.
6. The application can also convert text into speech for improved accessibility.

---

# 📸 Screenshots

> Add screenshots of:
- Home Page
- PDF Upload
- Question Answer Page
- Generated Answers

---

# 🔮 Future Improvements

- 📁 Support multiple file formats
- 🌍 Multilingual translation
- 📝 Automatic summarization
- 🎤 Voice-based questioning
- 📚 Document history
- 👥 User authentication
- ☁️ Cloud deployment
- 📱 Responsive mobile interface

---

# 🤝 Contributing

Contributions are welcome.

1. Fork the repository
2. Create a feature branch

```bash
git checkout -b feature-name
```

3. Commit your changes

```bash
git commit -m "Added new feature"
```

4. Push to GitHub

```bash
git push origin feature-name
```

5. Open a Pull Request

---

# 📄 License

This project is intended for educational and learning purposes.

---

# 👨‍💻 Author

**Sumit Kumar Singh**

- GitHub: https://github.com/Sumit692
- LinkedIn: *(Add your LinkedIn profile here)*

---

⭐ If you found this project useful, consider giving it a **Star** on GitHub!
