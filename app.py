import os
import re
import logging
import uuid
import threading
from flask import Flask, request, render_template, redirect, url_for, send_from_directory, jsonify
from werkzeug.utils import secure_filename
import pytesseract
import fitz  # PyMuPDF
from PIL import Image
from gtts import gTTS
import google.generativeai as genai

# ========================
# --- CONFIGURATION ---
# ========================

logging.getLogger("pytesseract").setLevel(logging.ERROR)

# 🔑 TEMP: directly set your new API key here
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY environment variable is not set. Please create a .env file."
    ) 


try:
    genai.configure(api_key=API_KEY)
    print("✅ Google AI SDK configured successfully.")
except Exception as e:
    print(f"❌ Error configuring Google AI SDK: {e}")

model = None
try:
    model = genai.GenerativeModel("gemini-3.1-flash-lite")
    print("✅ Using model: gemini-3.1-flash-lite")	
except Exception as e:
    print(f"⚠️ gemini-3.1-flash-lite unavailable: {e}")
    try:
        model = genai.GenerativeModel("gemini-3.5-flash")
        print("✅ Falling back to model: gemini-3.5-flash")
    except Exception as ex:
        print(f"❌ Failed to initialize any Gemini model: {ex}")
        model = None


UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
ALLOWED_EXTENSIONS = {'pdf'}

try:
    TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    if os.path.exists(TESSERACT_PATH):
        pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH
except Exception:
    print("Tesseract executable not found at specified path. Ensure it's installed and the path is correct if you're on Windows.")


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

tasks = {}

# ========================
# --- CORE FUNCTIONS ---
# ========================

def extract_text_from_pdf(pdf_path, task_id):
    tasks[task_id]['status'] = 'Processing... (Step 1/3: Extracting Text)'
    tasks[task_id]['progress'] = 15
    full_text = ""
    try:
        doc = fitz.open(pdf_path)
        total_pages = len(doc)
        
        # Try direct text extraction first
        direct_text = ""
        for page_num in range(total_pages):
            page = doc.load_page(page_num)
            direct_text += page.get_text() + "\n\n"
            
        # If direct text extraction extracted significant content, use it!
        if len(direct_text.strip()) > 100:
            print("✅ Extracted text directly from PDF (digital PDF detected).")
            full_text = direct_text
            tasks[task_id]['progress'] = 55
        else:
            # Fall back to OCR
            print("⚠️ Direct extraction empty, falling back to OCR...")
            matrix = fitz.Matrix(3, 3)
            for page_num in range(total_pages):
                page = doc.load_page(page_num)
                pix = page.get_pixmap(matrix=matrix)
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                img = img.convert("L")
                page_text = pytesseract.image_to_string(img)
                full_text += page_text + "\n\n"
                tasks[task_id]['progress'] = 15 + int(40 * (page_num + 1) / total_pages)
        doc.close()
    except Exception as e:
        print(f"❌ Error during text extraction: {e}")
        return f"An error occurred during text extraction: {e}"
    return full_text

def simplify_text(text, language, task_id):
    tasks[task_id]['status'] = 'Processing... (Step 2/3: Generating AI Notes)'
    tasks[task_id]['progress'] = 60
    if not text or not text.strip():
        return "⚠️ No readable text was extracted from the PDF."

    prompt = f"""
Your single most important job is to make the text below extremely easy to understand for someone who finds reading difficult.

First, translate the text into **{language}**. Then, rewrite it in that language following these strict rules:

1.  **Use Simple Words:** Use common, everyday words only.
2.  **Short Sentences:** Keep every sentence very short.
3.  **One Idea Per Sentence:** Each sentence should only have one main idea.
4.  **Explain Big Words:** If you must use a complicated word, explain it right away in parentheses (like this).
5.  **Use Analogies:** If possible, use a simple analogy or example to explain the main point.
6.  **Focus on "What" and "Why":** Explain what the text is about and why it matters in the simplest way possible.

Do not try to sound academic or formal. Your tone should be encouraging and very clear.

Text to process:
---
{text}
---
"""
    try:
        if not model:
            return "⚠️ AI Model is not configured. Cannot simplify text."
        response = model.generate_content(prompt)
        tasks[task_id]['progress'] = 85
        return response.text
    except Exception as e:
        print(f"❌ AI simplification error: {e}")
        return f"⚠️ Could not simplify text due to AI service error: {e}"

def convert_text_to_speech(text, output_filename, lang_code, task_id):
    tasks[task_id]['status'] = 'Processing... (Step 3/3: Creating Audio File)'
    tasks[task_id]['progress'] = 90
    try:
        speech_text = re.sub(r'[\*#✅→🧠🔬💡]', '', text)
        tts_text = ' '.join(speech_text.split()[:500])
        if not tts_text.strip(): return None

        tts = gTTS(text=tts_text, lang=lang_code, slow=False)
        filepath = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
        tts.save(filepath)
        tasks[task_id]['progress'] = 100
        return output_filename
    except Exception as e:
        print(f"❌ Error in TTS: {e}")
        return None

def process_file_in_background(filepath, language, filename, task_id):
    try:
        extracted_text = extract_text_from_pdf(filepath, task_id)
        if "An error occurred" in extracted_text or not extracted_text.strip():
            tasks[task_id]['status'] = 'Error'
            tasks[task_id]['result'] = {'original_text': extracted_text, 'simplified_text': "Could not extract readable text from the PDF."}
            return

        simplified_text = simplify_text(extracted_text, language, task_id)

        lang_codes = {'English': 'en', 'Hindi': 'hi', 'Kannada': 'kn'}
        lang_code = lang_codes.get(language, 'en')
        base_filename = filename.rsplit('.', 1)[0]
        audio_filename = f"{base_filename}_{lang_code}.mp3"
        convert_text_to_speech(simplified_text, audio_filename, lang_code, task_id)

        tasks[task_id]['status'] = 'Complete'
        tasks[task_id]['result'] = {'original_text': extracted_text, 'simplified_text': simplified_text, 'audio_file': audio_filename}
    except Exception as e:
        print(f"❌ Background task failed: {e}")
        tasks[task_id]['status'] = 'Error'
        tasks[task_id]['result'] = {'original_text': f"An unexpected error occurred: {e}", 'simplified_text': f"An unexpected error occurred: {e}"}

# ========================
# --- FLASK ROUTES ---
# ========================

@app.route('/', methods=['GET'])
def index():
    task_id = request.args.get('task_id')
    if task_id and task_id in tasks and tasks[task_id].get('status') == 'Complete':
        task = tasks[task_id]
        return render_template('index.html', task_id=task_id, result=task.get('result'))
    return render_template('index.html', task_id=None, result=None)

@app.route('/upload', methods=['POST'])
def upload_file_route():
    if 'file' not in request.files: return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '': return jsonify({'error': 'No selected file'}), 400

    if file and '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        language = request.form.get('language', 'English')
        task_id = str(uuid.uuid4())
        tasks[task_id] = {'status': 'Queued', 'progress': 0}

        thread = threading.Thread(target=process_file_in_background, args=(filepath, language, filename, task_id))
        thread.start()

        return jsonify({'task_id': task_id})
    return jsonify({'error': 'Invalid file type. Please upload a PDF.'}), 400

@app.route('/status/<task_id>')
def task_status(task_id):
    return jsonify(tasks.get(task_id, {}))

@app.route('/outputs/<filename>')
def serve_output_file(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename)

# --- NEW Q&A ROUTES ---
@app.route('/qa/<task_id>')
def qa_page(task_id):
    """Renders the Q&A chat page for a specific task."""
    if task_id not in tasks or tasks[task_id].get('status') != 'Complete':
        return redirect(url_for('index'))
    return render_template('qa.html', task_id=task_id)

@app.route('/ask', methods=['POST'])
def ask_question():
    """Handles a question about a document and returns an AI-generated answer."""
    data = request.get_json()
    task_id = data.get('task_id')
    question = data.get('question')

    if not task_id or not question:
        return jsonify({'error': 'Missing task_id or question'}), 400

    task = tasks.get(task_id)
    if not task or task.get('status') != 'Complete':
        return jsonify({'answer': 'Sorry, the document context is not available or still processing.'}), 404

    document_context = task['result'].get('original_text')
    if not document_context:
        return jsonify({'answer': 'Could not find the text for this document.'}), 404

    # Initialize chat history if not present
    if 'chat_history' not in task:
        task['chat_history'] = []

    history = task['chat_history']

    # Conversational system prompt combining document context with general chatbot instructions
    system_prompt = f"""You are a helpful and intelligent AI chatbot.
You have access to the following document text uploaded by the user:
--- DOCUMENT TEXT START ---
{document_context}
--- DOCUMENT TEXT END ---

Guidelines:
1. Answer the user's questions about the document using the text above.
2. If the user asks a general question, greets you (e.g. "hi", "hello"), or wants to have a normal conversation (not directly related to the document), answer them friendly and naturally using your general knowledge.
3. If they ask a question about the document that isn't answered in the text, you can tell them that it's not in the document, but then offer the general answer or explain the concept using your general knowledge.
4. Maintain a helpful, conversational, and encouraging tone.
"""

    # Construct the conversational prompt including history
    full_prompt = system_prompt + "\n--- CONVERSATION HISTORY ---\n"
    for msg in history:
        role_name = "User" if msg['role'] == 'user' else "Assistant"
        full_prompt += f"{role_name}: {msg['text']}\n"
    
    full_prompt += f"User: {question}\nAssistant:"

    try:
        if not model:
            return jsonify({'answer': 'The AI model is not available.'}), 500
        
        print(f"💬 Q&A Request - Task ID: {task_id}")
        print(f"❓ Question: {question}")
        
        response = model.generate_content(full_prompt)
        answer = response.text
        
        print(f"🤖 Answer: {answer}")
        
        # Save to history
        history.append({'role': 'user', 'text': question})
        history.append({'role': 'assistant', 'text': answer})
        task['chat_history'] = history
        
    except Exception as e:
        print(f"❌ AI Q&A error: {e}")
        answer = f"Sorry, I encountered an error while trying to find the answer: {e}"
    
    return jsonify({'answer': answer})


@app.route('/clear_chat', methods=['POST'])
def clear_chat():
    """Resets the chat history for a specific task."""
    data = request.get_json()
    task_id = data.get('task_id')
    if task_id and task_id in tasks:
        tasks[task_id]['chat_history'] = []
        return jsonify({'status': 'success'})
    return jsonify({'error': 'Invalid task_id'}), 400


# ========================
# --- MAIN ENTRY POINT ---
# ========================
if __name__ == '__main__':
    app.run(debug=True)