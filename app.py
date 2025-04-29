from flask import Flask, request, render_template, send_from_directory
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def form():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    phone = request.form.get('phone')
    email = request.form.get('email')
    dob = request.form.get('dob')
    uploaded_file = request.files.get('file')

    if uploaded_file and uploaded_file.filename != '':
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
        uploaded_file.save(file_path)
        file_link = f"/uploads/{uploaded_file.filename}"
    else:
        file_link = None

    return f"""
    <h3>Submitted Info</h3>
    <p><strong>Name:</strong> {name}</p>
    <p><strong>Phone:</strong> {phone}</p>
    <p><strong>Email:</strong> {email}</p>
    <p><strong>Date of Birth:</strong> {dob}</p>
    {'<p><strong>Uploaded File:</strong> <a href="' + file_link + '">Download</a></p>' if file_link else '<p>No file uploaded.</p>'}
    <br><a href="/">Back to form</a>
    """

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
