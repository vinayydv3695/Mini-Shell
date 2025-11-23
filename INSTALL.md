# 🚀 Installation Guide - Mini Shell

This guide will help you set up and run Mini Shell on any machine.

## 📋 Prerequisites

- **Python 3.6 or higher**
- **Linux/macOS** (or WSL on Windows)
- **Git** (to clone the repository)

---

## 🔧 Method 1: Automatic Setup (Recommended)

### Step 1: Clone the Repository
```bash
git clone https://github.com/vinayydv3695/Mini-Shell.git
cd Mini-Shell
```

### Step 2: Run Setup Script
```bash
bash setup.sh
```

This script will:
- ✅ Check Python version
- ✅ Create a virtual environment
- ✅ Activate the virtual environment
- ✅ Install any requirements (if needed)
- ✅ Make scripts executable

### Step 3: Start Mini Shell
```bash
bash run.sh
```

Or manually:
```bash
source venv/bin/activate
python3 mini_shell.py
```

---

## 🛠️ Method 2: Manual Setup

### Step 1: Clone the Repository
```bash
git clone https://github.com/vinayydv3695/Mini-Shell.git
cd Mini-Shell
```

### Step 2: Create Virtual Environment
```bash
python3 -m venv venv
```

### Step 3: Activate Virtual Environment

**On Linux/macOS:**
```bash
source venv/bin/activate
```

**On Windows:**
```cmd
venv\Scripts\activate
```

### Step 4: Install Requirements (Optional)
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Note:** Mini Shell uses only Python standard library, so no external packages are required!

### Step 5: Make Executable
```bash
chmod +x mini_shell.py
```

### Step 6: Run Mini Shell
```bash
python3 mini_shell.py
```

Or directly:
```bash
./mini_shell.py
```

---

## 🚀 Method 3: Quick Start (No Virtual Environment)

If you don't want to use a virtual environment:

```bash
git clone https://github.com/vinayydv3695/Mini-Shell.git
cd Mini-Shell
chmod +x mini_shell.py
python3 mini_shell.py
```

---

## 📦 What Gets Installed?

Mini Shell uses **only Python standard library modules**:
- `os` - Operating system interface
- `sys` - System-specific parameters
- `subprocess` - Subprocess management
- `json` - JSON encoding/decoding
- `readline` - GNU readline interface
- `shutil` - High-level file operations
- `fnmatch` - Unix filename pattern matching
- `re` - Regular expressions
- `difflib` - Helpers for computing deltas
- `pathlib` - Object-oriented filesystem paths
- `datetime` - Date and time handling

**No external packages required!** 🎉

---

## 🖥️ Platform-Specific Notes

### Linux
- Works out of the box
- `readline` is included by default

### macOS
- Works out of the box
- `readline` is included by default

### Windows
- Use WSL (Windows Subsystem for Linux) for best experience
- Alternatively, install `pyreadline3` for readline support:
  ```bash
  pip install pyreadline3
  ```

---

## ✅ Verify Installation

After installation, verify everything works:

```bash
# Check Python version
python3 --version

# Start Mini Shell
python3 mini_shell.py

# Inside Mini Shell, try:
pwd
ls
echo Hello from Mini Shell!
help
exit
```

---

## 🔄 Updating Mini Shell

To get the latest version:

```bash
cd Mini-Shell
git pull origin main
```

If you're using a virtual environment, reactivate it:
```bash
source venv/bin/activate
```

---

## 🗑️ Uninstallation

### Remove Virtual Environment
```bash
cd Mini-Shell
rm -rf venv
```

### Remove Configuration Files
```bash
rm ~/.minishell_config.json
rm ~/.minishell_history
```

### Remove Mini Shell
```bash
cd ..
rm -rf Mini-Shell
```

---

## 🐛 Troubleshooting

### Issue: `python3: command not found`
**Solution:** Install Python 3.6 or higher
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3

# macOS
brew install python3
```

### Issue: `permission denied` when running script
**Solution:** Make the script executable
```bash
chmod +x mini_shell.py setup.sh run.sh
```

### Issue: `readline` not found on Windows
**Solution:** Install pyreadline3
```bash
pip install pyreadline3
```

### Issue: Virtual environment not activating
**Solution:** Make sure you're in the correct directory
```bash
cd Mini-Shell
source venv/bin/activate
```

### Issue: Colors not showing properly
**Solution:** Use a modern terminal emulator that supports ANSI colors
- Linux: GNOME Terminal, Konsole
- macOS: iTerm2, Terminal.app
- Windows: Windows Terminal, WSL

---

## 📞 Support

If you encounter issues:
1. Check the [Troubleshooting](#-troubleshooting) section
2. Read the main [README.md](README.md)
3. Open an issue on [GitHub](https://github.com/vinayydv3695/Mini-Shell/issues)

---

## 🎉 Quick Reference

### Common Commands

```bash
# Setup (first time only)
bash setup.sh

# Start Mini Shell
bash run.sh
# or
source venv/bin/activate && python3 mini_shell.py

# Deactivate virtual environment
deactivate

# Update Mini Shell
git pull origin main
```

---

**Happy Coding! 🐚**
