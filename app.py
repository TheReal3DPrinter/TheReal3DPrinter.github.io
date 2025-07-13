from flask import Flask, request, redirect, url_for, send_from_directory, render_template_string
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create the uploads directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# HTML with conditional file display
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>File Upload</title>
</head>
<body>
    <h1>Upload a file</h1>
    <form method="post" action="/upload" enctype="multipart/form-data">
        <input type="file" name="file" required><br><br>
        <button type="submit">Upload</button>
    </form>

    {% if filename %}
        <h2>Uploaded File:</h2>
        <a href="{{ url_for('uploaded_file', filename=filename) }}" target="_blank">{{ filename }}</a>
        <br><br>
        {% if filename.endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')) %}
            <img src="{{ url_for('uploaded_file', filename=filename) }}" alt="Uploaded Image" style="max-width: 500px;">
        {% endif %}
    {% endif %}
</body>
</html>
"""

@app.route('/', methods=['GET'])
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files.get('file')
    if not file or file.filename == '':
        return redirect('/')
    filename = file.filename
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    return render_template_string(HTML_TEMPLATE, filename=filename)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
