# GOODIE AI ASSISTANT - BUILD GUIDE

Complete step-by-step instructions to build EXE and MSI installers from scratch.

---

## 📋 PREREQUISITES

Before you start, make sure you have:

### 1. **Python Installation**
   - Download Python 3.11 from: https://www.python.org/downloads/
   - **IMPORTANT**: During installation, check the box: ☑️ "Add Python to PATH"
   - Click "Install Now"

   **Verify installation:**
   ```bash
   python --version
   ```
   Should show: `Python 3.11.x` or higher

### 2. **Git (Optional, but recommended)**
   - Download from: https://git-scm.com/download/win
   - Install with default settings
   - This helps you manage the project better

### 3. **7-Zip or WinRAR** (Optional)
   - To extract files if needed
   - Available from: https://www.7-zip.org/

---

## 🚀 STEP-BY-STEP BUILD PROCESS

### STEP 1: Clone or Download the Project

**Option A: Using Git (Recommended)**
```bash
git clone https://github.com/infrea/Goodie.git
cd Goodie
```

**Option B: Download ZIP**
1. Go to https://github.com/infrea/Goodie
2. Click "Code" → "Download ZIP"
3. Extract the ZIP file
4. Open Command Prompt in the extracted folder

### STEP 2: Open Command Prompt in Project Directory

1. Open File Explorer
2. Navigate to the Goodie project folder
3. Press `Shift + Right-Click` inside the folder
4. Select "Open PowerShell window here" or "Open Command Prompt here"

### STEP 3: Create Virtual Environment

A virtual environment keeps project dependencies isolated.

```bash
python -m venv venv
```

**Wait for it to complete** (1-2 minutes)

### STEP 4: Activate Virtual Environment

**On Windows (PowerShell):**
```bash
.\venv\Scripts\Activate.ps1
```

**If you get an error about execution policy**, run this first:
```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then activate again:
```bash
.\venv\Scripts\Activate.ps1
```

**If you're using Command Prompt (CMD):**
```bash
venv\Scripts\activate.bat
```

**Verify activation:** You should see `(venv)` at the start of your command line:
```
(venv) C:\Users\YourName\Goodie>
```

### STEP 5: Upgrade pip (Python Package Manager)

```bash
python -m pip install --upgrade pip
```

### STEP 6: Install Required Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- PyInstaller (for building EXE)
- All GOODIE dependencies (llama-cpp-python, faster-whisper, etc.)

**This may take 5-10 minutes. Be patient!**

### STEP 7: Verify Installation

Check if all packages installed correctly:

```bash
pip list
```

You should see packages like:
- PyInstaller
- llama-cpp-python
- faster-whisper
- piper-tts
- etc.

---

## 🔨 BUILD OPTIONS

### OPTION A: BUILD EXE (Standalone Executable)

**Most Common Choice - Easiest to Distribute**

```bash
python build.py --format exe
```

**What it does:**
- Packages GOODIE into a single `.exe` file
- ~150-200MB after compilation
- No Python installation needed on target machine
- Users just run the EXE file

**Where to find the output:**
```
Goodie\dist\exe\GOODIE.exe
```

**How long it takes:** 5-15 minutes depending on your computer

**Progress indicators:**
```
Building EXE installer...
creating .\build\goodie\...
UPX is not available...
Analyzing base_library.zip...
```

When complete, you'll see:
```
✅ EXE build completed successfully!
📦 Output: dist/exe/GOODIE.exe
```

---

### OPTION B: BUILD MSI (Windows Installer)

**Professional Installation Experience**

**Prerequisites for MSI:**
1. Download WiX Toolset v3.11.2 from: https://github.com/wixtoolset/wix3/releases/download/wix3112rtm/wix311.exe
2. Install it (keep default settings)

**Build MSI:**
```bash
python build.py --format msi
```

**Manual MSI Creation (If automatic fails):**

1. First ensure you have the WiX configuration:
```bash
python build.py --format msi
```

2. Open Command Prompt and navigate to WiX installation (usually):
```bash
cd "C:\Program Files (x86)\WiX Toolset v3.11\bin"
```

3. Create the MSI:
```bash
candle.exe "C:\path\to\Goodie\build\goodie.wxs" -o build\
light.exe build\goodie.wixobj -o "C:\path\to\Goodie\dist\msi\goodie.msi"
```

**Output location:**
```
Goodie\dist\msi\goodie.msi
```

**MSI advantages:**
- Professional installer with wizard
- Can add/remove from Control Panel
- Better for enterprise deployment

---

### OPTION C: BUILD BOTH EXE AND MSI

```bash
python build.py --format all
```

This builds both formats in sequence.

---

## 📁 BUILD OUTPUT STRUCTURE

After successful build, you'll have:

```
Goodie/
├── dist/
│   ├── exe/
│   │   └── GOODIE.exe          ← Standalone executable
│   └── msi/
│       └── goodie.msi          ← Windows installer
├── build/
│   ├── goodie/                 ← Compiled files
│   ├── goodie.wxs              ← MSI configuration
│   └── specs/
│       └── goodie.spec         ← Build specification
└── ...
```

---

## ✅ TESTING THE BUILD

### Test the EXE:

1. Navigate to `dist/exe/`
2. Double-click `GOODIE.exe`
3. You should see the banner and configuration output
4. The app will check for the Qwen3 4B model

### First Launch Behavior:

```
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║           GOODIE AI ASSISTANT v1.0.0                     ║
║     Your Professional Desktop Companion                  ║
║          Powered by Qwen3 4B GGUF                        ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝

🔧 Initializing GOODIE...

==================================================
GOODIE AI ASSISTANT CONFIGURATION
==================================================

📦 MODEL SETTINGS
  Default Model: Qwen3 4B
  Quantization: Q4_K_M
  Engine: llama.cpp
  Context Length: 8192
  GPU Acceleration: ✓

...
```

---

## 🐛 TROUBLESHOOTING

### Problem 1: "python: command not found" or "python is not recognized"

**Solution:**
1. Python might not be in PATH
2. Reinstall Python and **CHECK** "Add Python to PATH"
3. Or use full path: `C:\Python311\python.exe --version`

### Problem 2: Virtual Environment activation fails

**Solution (PowerShell):**
```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
Then activate again.

### Problem 3: "pip: command not found"

**Solution:**
```bash
python -m pip install --upgrade pip
```

### Problem 4: "ModuleNotFoundError: No module named 'PyInstaller'"

**Solution:**
```bash
pip install PyInstaller
```

### Problem 5: Build takes very long or freezes

**Solution:**
- Close other applications
- Make sure you have at least 2GB free disk space
- Try building again

### Problem 6: "The system cannot find the path specified"

**Solution:**
- Make sure you're in the correct directory
- Check path with: `cd` (shows current directory)
- Navigate to Goodie folder: `cd C:\Users\YourName\Goodie`

### Problem 7: PyInstaller build fails

**Solution:**
```bash
# Clean previous build
rmdir /s build dist

# Try building again
python build.py --format exe
```

---

## 🎯 NEXT STEPS AFTER BUILDING

### If you built an EXE:

1. **Test it:**
   - Double-click the EXE
   - Make sure it runs without errors

2. **Share it:**
   - Send `dist/exe/GOODIE.exe` to users
   - No installation needed, just run

3. **Create a shortcut:**
   - Right-click GOODIE.exe
   - Select "Create shortcut"
   - Move shortcut to Desktop

### If you built an MSI:

1. **Test it:**
   - Double-click the MSI file
   - Follow the installer wizard
   - Verify it installs to Program Files

2. **Share it:**
   - Users can double-click to install
   - Add/remove programs support
   - Better for corporate deployment

---

## 📊 SYSTEM REQUIREMENTS FOR BUILD

Your computer needs:

- **OS**: Windows 7 or later
- **RAM**: 4GB minimum (8GB recommended)
- **Disk**: 5GB free space
- **Python**: 3.9 or higher
- **Internet**: For downloading dependencies

---

## 🔄 REBUILDING AFTER CHANGES

If you modify the code and want to rebuild:

```bash
# Make sure virtual environment is active
(venv) C:\Users\YourName\Goodie>

# Clean previous build
rmdir /s build dist

# Build again
python build.py --format exe
```

---

## 📞 GETTING HELP

If you get stuck:

1. **Check error messages carefully** - they often tell you what's wrong
2. **Google the error** - most Python errors have solutions online
3. **Check Python version**: `python --version` (should be 3.9+)
4. **Verify pip**: `pip --version`
5. **Reinstall dependencies**: `pip install --upgrade -r requirements.txt`

---

## 🎉 SUCCESS CHECKLIST

- ✅ Python installed and added to PATH
- ✅ Virtual environment created and activated
- ✅ All dependencies installed (`pip list` shows packages)
- ✅ Build script ran successfully
- ✅ EXE/MSI files created in `dist/` folder
- ✅ Tested the executable

Congratulations! You've successfully built GOODIE! 🚀

---

## 💡 QUICK REFERENCE COMMANDS

```bash
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Build EXE
python build.py --format exe

# Build MSI
python build.py --format msi

# Build both
python build.py --format all

# Clean build
rmdir /s build dist

# Deactivate virtual environment
deactivate
```

---

**Version**: 1.0.0  
**Last Updated**: 2026-06-22  
**Status**: Ready for Production
