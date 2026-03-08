import os
import socket
import qrcode
from flask import Flask, render_template_string, request, send_from_directory, jsonify

app = Flask(__name__)
UPLOAD_FOLDER = 'shared_files'
QR_FOLDER = os.path.join('static', 'qrcodes')

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(QR_FOLDER, exist_ok=True)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lumina-Link Pro | Official</title>
    <script src="https://cdn.jsdelivr.net/npm/jsqr@1.4.0/dist/jsQR.min.js"></script>
    <style>
        :root { --primary: #2ea043; --bg: #0d1117; --card: #161b22; }
        body { background: var(--bg); color: #c9d1d9; font-family: 'Segoe UI', sans-serif; margin: 0; text-align: center; }
        header { background: #010409; padding: 25px; border-bottom: 1px solid #30363d; }
        .container { display: flex; flex-wrap: wrap; justify-content: center; gap: 20px; padding: 40px 20px; }
        .card { background: var(--card); border: 1px solid #30363d; border-radius: 12px; padding: 25px; width: 400px; transition: 0.3s; }
        .card:hover { border-color: var(--primary); }
        .btn { background: var(--primary); color: white; border: none; padding: 12px; width: 100%; border-radius: 8px; font-weight: bold; cursor: pointer; margin-top: 15px; font-size: 16px; }
        #video-container { position: relative; width: 100%; height: 250px; background: #000; border-radius: 8px; overflow: hidden; display: none; margin-top: 15px; border: 1px solid #333; }
        .laser { position: absolute; top: 0; width: 100%; height: 3px; background: var(--primary); box-shadow: 0 0 15px var(--primary); animation: scan 2s infinite linear; }
        @keyframes scan { 0% { top: 0; } 100% { top: 100%; } }
        .qr-box img { width: 220px; border: 5px solid white; border-radius: 10px; margin-top: 15px; }
    </style>
</head>
<body>
    <header>
        <h1 style="margin:0; color:var(--primary);">LUMINA-LINK PRO 🚀</h1>
        <p style="color:#8b949e; margin:5px 0 0;">Enterprise Secure File Gateway</p>
    </header>
    <div class="container">
        <div class="card">
            <h2>💻 Sender</h2>
            <input type="file" id="fileInput" style="margin:15px 0; color:#8b949e; width: 100%;">
            <button onclick="generateInstantQR()" class="btn">GENERATE INSTANT QR</button>
            <div id="qrResult" class="qr-box" style="display:none;">
                <img id="qrImg" src="">
                <p id="fileName" style="color:var(--primary); margin-top:10px; font-weight: bold;"></p>
                <progress id="uploadProgress" value="0" max="100" style="width:100%;"></progress>
            </div>
        </div>
        <div class="card">
            <h2>📱 Receiver</h2>
            <button id="startBtn" class="btn" style="background:#58a6ff;">START SCANNER</button>
            <div id="video-container">
                <video id="video" playsinline style="width:100%; height:100%;"></video>
                <div class="laser"></div>
            </div>
            <p id="status" style="margin-top:10px; color:#8b949e;">[ SYSTEM IDLE ]</p>
        </div>
    </div>
    <script>
        async function generateInstantQR() {
            const file = document.getElementById('fileInput').files[0];
            if (!file) return alert("Please select a file.");
            
            // This detects if you are using Ngrok or Local IP automatically
            const currentUrl = window.location.origin;

            const response = await fetch('/get_qr_link', {
                method: 'POST',
                body: JSON.stringify({ name: file.name, base_url: currentUrl }),
                headers: { 'Content-Type': 'application/json' }
            });
            const data = await response.json();
            document.getElementById('qrImg').src = data.qr;
            document.getElementById('fileName').innerText = "Streaming: " + file.name;
            document.getElementById('qrResult').style.display = 'block';

            const formData = new FormData();
            formData.append('file', file);
            const xhr = new XMLHttpRequest();
            xhr.open('POST', '/upload_bg', true);
            xhr.upload.onprogress = (e) => {
                document.getElementById('uploadProgress').value = (e.loaded / e.total) * 100;
            };
            xhr.send(formData);
        }

        const video = document.getElementById('video');
        document.getElementById('startBtn').addEventListener('click', () => {
            navigator.mediaDevices.getUserMedia({ video: { facingMode: "environment" } }).then(stream => {
                video.srcObject = stream;
                video.play();
                document.getElementById('video-container').style.display = 'block';
                document.getElementById('startBtn').style.display = 'none';
                document.getElementById('status').innerText = "[ SCANNING... ]";
                requestAnimationFrame(tick);
            }).catch(err => { alert("Camera Error: Please allow permissions."); });
        });

        function tick() {
            if (video.readyState === video.HAVE_ENOUGH_DATA) {
                const canvas = document.createElement('canvas');
                canvas.height = video.videoHeight; canvas.width = video.videoWidth;
                const ctx = canvas.getContext('2d');
                ctx.drawImage(video, 0, 0);
                const code = jsQR(ctx.getImageData(0,0,canvas.width,canvas.height).data, canvas.width, canvas.height);
                if (code) { window.location.href = code.data; return; }
            }
            requestAnimationFrame(tick);
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/get_qr_link', methods=['POST'])
def get_qr_link():
    data = request.json
    name = data.get('name')
    base_url = data.get('base_url')
    link = f"{base_url}/download/{name}"
    
    qr_name = f"qr_{name.replace(' ', '_')}.png"
    qr_path = os.path.join(QR_FOLDER, qr_name)
    qrcode.make(link).save(qr_path)
    return jsonify({"qr": f"/static/qrcodes/{qr_name}"})

@app.route('/upload_bg', methods=['POST'])
def upload_bg():
    file = request.files.get('file')
    if file: file.save(os.path.join(UPLOAD_FOLDER, file.filename))
    return "Success"

@app.route('/download/<f>')
def download(f):
    return send_from_directory(UPLOAD_FOLDER, f)

@app.route('/static/qrcodes/<f>')
def send_qr(f):
    return send_from_directory(QR_FOLDER, f)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)