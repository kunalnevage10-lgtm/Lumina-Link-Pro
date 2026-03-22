import os
import qrcode
from flask import Flask, render_template, request, send_from_directory, jsonify

app = Flask(__name__)
# Supporting high-speed large file transfers up to 10GB
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024 * 1024 

UPLOAD_FOLDER = 'shared_files'
QR_FOLDER = 'static/qrcodes'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(QR_FOLDER, exist_ok=True)

# YOUR ACTIVE HOTSPOT IP (Update this from ipconfig)
MY_IP = '192.168.1.34' 

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file"}), 400
    
    file = request.files['file']
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    
    # 10GB/min Logic: Direct binary stream with 128MB buffer
    with open(file_path, "wb") as f:
        while True:
            chunk = file.stream.read(128 * 1024 * 1024)
            if not chunk: break
            f.write(chunk)
    
    # Generate the local high-speed download link
    download_link = f"http://{MY_IP}:5000/confirm_download/{file.filename}"
    
    # Save the QR code for the specific file
    qr_filename = f"qr_{os.urandom(4).hex()}.png"
    qr_path = os.path.join(QR_FOLDER, qr_filename)
    qr = qrcode.make(download_link)
    qr.save(qr_path)
    
    return jsonify({
        "status": "success", 
        "qr_path": f"/static/qrcodes/{qr_filename}",
        "raw_link": download_link
    })

@app.route('/confirm_download/<filename>')
def confirm_download(filename):
    # Receiver's confirmation screen
    return render_template('confirm.html', filename=filename)

@app.route('/get_file/<filename>')
def get_file(filename):
    # Direct file serving via Flask
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    # Threaded mode allows multiple high-speed streams
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)