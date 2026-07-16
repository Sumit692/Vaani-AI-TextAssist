# 🧠 VAANI AI – TextAssist

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Flask-3.1-black?style=for-the-badge&logo=flask" />
  <img src="https://img.shields.io/badge/Google-Gemini_AI-4285F4?style=for-the-badge&logo=google" />
  <img src="https://img.shields.io/badge/OCR-Tesseract-5C2D91?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Text_to_Speech-gTTS-FF6F00?style=for-the-badge" />
</p>

<p align="center">
An AI-powered document assistant that extracts text from PDF files, simplifies complex content using Google Gemini, answers questions based on uploaded documents, and converts text into speech for improved accessibility.
</p>

<p align="center">

## 🌐 Live Demo

🚀 **Try the application here:**  
**https://vaani-ai-textassist-1.onrender.com/**

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

<img width="1366" height="768" alt="Screenshot (6)" src="https://github.com/user-attachments/assets/7ca01f02-31b5-467b-b0f4-72152a6e2eb4" />
<img width="1366" height="768" alt="Screenshot (7)" src="https://github.com/user-attachments/assets/3ddc4c23-4273-4c96-908d-f5b161cf53bb" />
<img width="1366" height="768" alt="Screenshot (8)" src="https://github.com/user-attachments/assets/29d31ab9-f3c0-4df0-a69a-c6314892a93a" />


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
- LinkedIn: https://www.linkedin.com/in/sumitkumarsingh24/

---

⭐ If you found this project useful, consider giving it a **Star** on GitHub!
