# 📡 Lumina Link Pro: High-Speed P2P & LAN File Transfer

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Framework-Flask-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask" />
  <img src="https://img.shields.io/badge/Transfer%20Limit-Up%20to%2010GB-00C853?style=for-the-badge" alt="Transfer Limit" />
  <img src="https://img.shields.io/badge/Pairing-QR%20Code%20Technology-FF6F00?style=for-the-badge" alt="QR Pairing" />
  <img src="https://img.shields.io/badge/Live%20Demo-Render-46E3B7?style=for-the-badge&logo=render&logoColor=white" alt="Render Demo" />
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License" />
</p>

An enterprise-grade local network (LAN / Wi-Fi Hotspot) and web file transfer engine engineered with **Python**, **Flask**, and **QR Code generation**. Designed for zero-cloud latency, **Lumina Link Pro** streams large files (up to **10 GB**) across devices via direct binary chunking and instant mobile camera pairing.

---

## 🌐 Live Demo & Deployment

Experience the cloud-hosted prototype online:
🔗 **[Live Demo on Render](https://lumina-link-pro.onrender.com/)**

---

## 🎯 Objective

Transferring large media assets, video files, or software builds between laptops, smartphones, and cross-platform devices is often bottlenecked by cloud upload limits, compression, external messenger limits, or complex pairing protocols.

**Lumina Link Pro** provides:
- **Zero-Cloud Direct Transfer**: Bypasses slow third-party cloud uploads by keeping data inside the local high-speed network.
- **Extreme Buffer Throughput**: Optimized 128 MB binary chunked streaming for sustained multi-gigabyte transfers.
- **One-Scan Pairing**: Instant QR code generation that converts mobile cameras into direct download triggers without installing client apps.

---

## ✨ Key Features

- **🚀 10 GB Large File Support**:
  - Configured with `MAX_CONTENT_LENGTH = 10 GB` to support heavy video files, disk images, and raw datasets.
  - Custom binary stream buffering in **128 MB chunks** avoids memory bloat and prevents RAM exhaustion.
- **📱 Instant QR Code Mobile Pairing**:
  - Every file upload instantly generates an ephemeral, high-resolution QR code (`qrcode` library).
  - Mobile recipients simply point their native camera at the host screen to trigger the confirmation download screen.
- **🔄 Multi-Threaded Streaming Engine**:
  - Flask server configured with `threaded=True` to support concurrent upload and download streams simultaneously across multiple client devices.
- **🛡️ Receiver Confirmation Gateway**:
  - Built-in `confirm.html` receiver gate to prevent unauthorized silent downloads.

---

## 🛠️ Tech Stack Used

| Layer | Component | Description |
|---|---|---|
| **Backend Framework** | [Flask](https://flask.palletsprojects.com/) | Lightweight, multi-threaded HTTP server and route dispatcher |
| **QR Code Engine** | [`qrcode[pil]`](https://pypi.org/project/qrcode/) | Dynamic image generation for instantaneous mobile URL resolution |
| **Image Processing** | [Pillow (PIL)](https://python-pillow.org/) | Rendering and PNG serialization of generated QR codes |
| **Frontend UI** | HTML5, Modern CSS3, JavaScript | Responsive file dropzone and QR modal viewer |

---

## 📁 Repository Structure

```plaintext
Lumina-Link-Pro/
├── app.py              # Main Flask application with binary chunking & QR routes
├── requirements.txt    # Production Python dependencies
├── shared_files/       # Storage directory for uploaded transfer files
├── static/
│   └── qrcodes/        # Cache of generated ephemeral QR code PNGs
├── templates/
│   ├── index.html      # Sender upload interface with live QR display
│   └── confirm.html    # Receiver download verification screen
└── README.md           # Project documentation
```

---

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/kunalnevage10-lgtm/Lumina-Link-Pro.git
cd Lumina-Link-Pro
```

### 2. Set Up Virtual Environment
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 🚀 Usage Instructions

### 1. Find Your Local Network IP Address
To enable transfers across devices on your local Wi-Fi or mobile hotspot:
* **Windows**: Open terminal and run `ipconfig` (note the *IPv4 Address*, e.g., `192.168.1.34`).
* **macOS / Linux**: Open terminal and run `ifconfig` or `ip a`.

Update the `MY_IP` variable inside [`app.py`](file:///c:/Users/Asus/Documents/antigravity/friendly-babbage/Lumina-Link-Pro/app.py):
```python
MY_IP = '192.168.1.34'  # Replace with your actual local network IP
```

### 2. Start the Server
```bash
python app.py
```

### 3. Share Files Across Devices
1. On your PC, open `http://localhost:5000`.
2. Drag and drop or browse for any file (up to 10 GB) and click **Upload**.
3. A custom QR code will appear on screen.
4. Open the camera on your smartphone or second laptop (connected to the same Wi-Fi/Hotspot) and scan the QR code.
5. Tap **Confirm Download** to receive the file directly at maximum local Wi-Fi transfer speeds!

---

## 🛡️ License

This project is licensed under the [MIT License](LICENSE).
