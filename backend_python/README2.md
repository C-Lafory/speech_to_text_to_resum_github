# 🎙️ Audio Transcription Project with Whisper

This project allows **converting an audio file to text** using **OpenAI Whisper**. It supports audio file conversion to `.wav` (16kHz, mono) before transcription.

---

## 🚀 Installation

### 1️⃣ **Clone the project**
```bash
git clone https://github.com/your-repo.git
cd your-repo
```

### 2️⃣ **Create a virtual environment**
> **Note:** Before running the command, ensure that `python3` is installed. [see more...](#Installing-Python)
```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate    # On Windows
```

### 3️⃣ **Install dependencies**
```bash
pip install -r requirements.txt
```

📌 If you are using a **GPU with CUDA**, install PyTorch with this command (modify according to your CUDA version):
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

---

## 📂 Project Structure
```
/your_project
│── /models                # 📂 Folder to store the Whisper model
│── /static                # 📂 Folder to store audio files and transcriptions
│── main.py                # 📝 Main script
│── requirements.txt       # 📜 Dependencies
│── .gitignore             # 🚫 Ignore the model in Git
│── README.md              # 📖 Documentation
```

---

## 📥 Downloading the Whisper Model

Whisper **automatically downloads the model** into `/models/` on the first run. To download it manually, run:
```bash
python -c "import whisper; whisper.load_model('small', download_root='models')"
```
📌 **Available models:** `tiny`, `base`, `small`, `medium`, `large`.

---

## 🎙️ Usage

### 1️⃣ **Convert and transcribe an audio file**
If your audio file is `my_audio.m4a`, run:
```bash
python main.py my_audio m4a
```
This script will:
✅ Convert `my_audio.m4a` to `my_audio.wav`
✅ Transcribe the audio with Whisper
✅ Save the text in `static/file/my_audio/transcription.txt`

---

## ⚠️ Error Resolution

### ❌ *Warning: FP16 is not supported on CPU; using FP32 instead*
💡 **Solution:** Add this line in `main.py` to force FP32 on CPU:
```python
import torch
model = whisper.load_model("small", download_root="models", device="cpu").to(dtype=torch.float32)
```

---

## Installing Python

### Windows

1. Download the Python installer from the [official website](https://www.python.org/downloads/windows/).
2. Run the installer and follow the instructions. Make sure to check the box that says "Add Python to PATH".

### macOS

1. Install Homebrew if you don't have it already:
    ```bash
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    ```
2. Install Python using Homebrew:
    ```bash
    brew install python
    ```

### Linux

1. Use your package manager to install Python. For example:

    **Debian-based systems:**
    ```bash
    sudo apt update
    sudo apt install python3
    ```

    **Red Hat-based systems:**
    ```bash
    sudo dnf install python3
    ```

    **Arch-based systems:**
    ```bash
    sudo pacman -S python
    ```

    **openSUSE:**
    ```bash
    sudo zypper install python3
    ```

---

## 📜 License
This project is licensed under the **MIT** license.

---

🔥 **Ready to transcribe!** If you have any questions, feel free to ask. 🚀

