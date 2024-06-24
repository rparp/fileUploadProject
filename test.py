import os
import sqlite3
from flask import Flask, flash, jsonify, request, redirect, render_template
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "secret key"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

path = os.getcwd()
uploadFolder = 'app/uploads'
if not os.path.isdir(uploadFolder):
    os.mkdir(uploadFolder)
app.config['UPLOAD_FOLDER'] = uploadFolder

allowedExtensions = set(['txt'])

# Initialize SQLite database
#database = os.path.join(path, 'file_uploads.db')
database = 'file_uploads.db'

# Health check to see if the service is active
@app.route('/healthCheck', methods=['GET'])
def checkStatus():
    response = {
        'healthCheck': 'Flask service is up and running!'
    }
    return jsonify(response), 200

def createTable():
    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS words
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 word TEXT NOT NULL,
                 filename TEXT NOT NULL,
                 filepath TEXT NOT NULL)''')
    conn.commit()
    conn.close()

createTable()

def allowedFile(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowedExtensions

@app.route('/')
def uploadForm():
    return render_template('upload.html')

@app.route('/', methods=['POST'])
def uploadFile():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        
        if file and allowedFile(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Read content of the file and split into words
            with open(filepath, 'r') as f:
                content = f.read()
                words = content.split()
            
            # Insert each word into the SQLite database
            conn = sqlite3.connect(database)
            c = conn.cursor()
            for word in words:
                c.execute("INSERT INTO words (word, filename, filepath) VALUES (?, ?, ?)", (word, filename, filepath))
            conn.commit()
            conn.close()
            
            flash('File successfully uploaded and words saved to database')
            return render_template('upload.html')
        else:
            flash('Allowed file types are txt')
            return redirect(request.url)

# Route to get word by ID
@app.route('/word/<int:id>', methods=['GET'])
def getWordById(id):
    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute("SELECT word FROM words WHERE id=?", (id,))
    word = c.fetchone()
    conn.close()
    if word:
        return jsonify({'id': id, 'word': word[0]}), 200
    else:
        return jsonify({'error': 'Word not found'}), 404

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
