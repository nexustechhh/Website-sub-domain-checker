# Admin Path Scanner - Installation and Usage Guide

**[IMPORTANT]** This is a desktop application. You MUST download the project files and run them locally. It will NOT work in a web browser.

---
**Watermark:** Created for authorized security testing | Admin Path Scanner v1.0
---

## Overview

The Admin Path Scanner is a desktop application designed to discover admin panels, login pages, and other sensitive paths on web servers. It's built using Python 3 and tkinter, and works on Linux (Debian/Ubuntu) and Windows environments.

## Features

- Scan for common admin/sensitive paths (200+ built-in paths)
- Import custom wordlists from .txt files
- Configurable delay between requests to avoid detection
- User-agent rotation to mimic real browsers
- Color-coded results table (green=200, yellow=301/302, orange=403, grey=404)
- Non-blocking GUI with threading
- Automatic report generation (TXT and CSV formats)
- Real-time progress tracking
- Stop scan mid-way capability

## System Requirements

- Linux (Debian/Ubuntu) or Windows
- Python 3.6 or higher
- requests>=2.25.1
- Internet connection

## Installation

### Linux (Debian/Ubuntu)

1. Open terminal and update system:
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

2. Install required packages:
   ```bash
   sudo apt install python3 python3-pip python3-tk -y
   ```

3. Navigate to your application directory:
   ```bash
   cd "path/to/your/folder"
   ```
   *(Create your own folder and place the application files there)*

4. Install dependencies:
   ```bash
   pip3 install -r requirements.txt
   ```

5. Verify installation:
   ```bash
   python3 --version
   pip3 list | grep requests
   ```

### Windows (CMD / PowerShell / Windows Terminal)

1. Install Python from https://www.python.org/downloads/ (Make sure to check "Add Python to PATH")

2. Navigate to your project folder:
   ```bash
   cd "path\to\your\folder"
   ```
   *(Create your own folder and place the application files there)*

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Verify installation:
   ```bash
   python --version
   pip list
   ```

## Running the Application

**IMPORTANT:** You must run this program locally from your terminal. Do NOT attempt to open files in a browser.

- **Linux:** `python3 main.py`
- **Windows:** `python main.py`

## GUI Usage

- Enter target domain (example.com or https://example.com)
- Set delay between requests (default: 1.0)
- Click "Start Scan"
- Monitor results in real time
- Use "Stop Scan" to halt
- Reports generate automatically

## Importing Wordlists

- Click "Import Wordlist"
- Select a .txt file

Example:
```
/admin
/login
/dashboard
/custom-path
```

## Saving Reports

- Reports auto-save after scan
- Or click "Save Report"
- Files saved as .txt and .csv

## Usage Examples

### Basic Scan
- Enter domain
- Set delay
- Start scan

### Fast Scan (use carefully)
- Set delay to 0.1
- Monitor for rate limiting

## Interpreting Results

### Status Codes
- **200:** Exists
- **301/302:** Redirect
- **403:** Forbidden
- **404:** Not found

### Response Time
- **Lower** = faster server
- **Higher** = slower server

## Troubleshooting

### GUI not showing (Linux)
```bash
export DISPLAY=:0
```

### Missing tkinter
```bash
sudo apt install python3-tk -y
```

### Network errors
- Check internet
- Verify domain
- Try https://

### Permission issues
```bash
chmod +x main.py
python3 main.py
```

## Advanced Usage

- Edit default_wordlist in main.py
- Modify user_agents
- Adjust request timeout

## Security Notes

- Only scan authorized targets
- Respect site rules
- Use responsibly

## Legal Disclaimer

This tool is for educational and authorized testing only. The user is responsible for proper usage.

## Version

**v1.0** Initial release
