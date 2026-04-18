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

**IMPORTANT:** Read this section carefully before using the application.

### Responsibility & Liability
- **We are NOT responsible** for any damage to your computer system, data loss, or hardware issues
- **We are NOT responsible** for any legal consequences, violations of laws, or legal trouble resulting from usage
- **We are NOT responsible** for network issues, ISP problems, or internet service disruptions
- **We are NOT responsible** for any security vulnerabilities or compromises to your system
- **We are NOT responsible** for any financial losses, business interruption, or consequential damages
- **We are NOT responsible** for account suspensions, IP bans, or blacklisting by services
- **We are NOT responsible** for third-party service interruptions or API changes
- **We are NOT responsible** for any mental health issues, stress, or anxiety caused by usage
- **We are NOT responsible** for any reputation damage or social consequences
- **We are NOT responsible** for any violation of computer crime laws, cyberbullying, or harassment
- **We are NOT responsible** for any unauthorized access to confidential or proprietary information
- **We are NOT responsible** for any damage to target websites, servers, or digital infrastructure
- **We are NOT responsible** for any privacy violations, data breaches, or identity theft
- **We are NOT responsible** for any employment issues, job loss, or professional consequences
- **We are NOT responsible** for any educational institution disciplinary actions
- **We are NOT responsible** for any immigration or visa issues resulting from usage
- **We are NOT responsible** for any family disputes, relationship problems, or personal conflicts
- **We are NOT responsible** for any addiction, compulsive behavior, or psychological dependency
- **We are NOT responsible** for any physical health issues from prolonged computer use
- **We are NOT responsible** for any software conflicts, system crashes, or operating system corruption
- **We are NOT responsible** for any malware infections, virus transmissions, or security compromises
- **We are NOT responsible** for any unauthorized purchases, subscriptions, or financial transactions
- **We are NOT responsible** for any intellectual property disputes, trademark violations, or copyright claims
- **We are NOT responsible** for any regulatory compliance issues, industry violations, or professional license problems
- **We are NOT responsible** for any tax issues, audit problems, or financial reporting complications
- **We are NOT responsible** for any insurance claim denials or premium increases
- **We are NOT responsible** for any travel restrictions, border issues, or customs problems

### Usage Terms
- This tool is for **educational and authorized testing only**
- **You must** obtain explicit permission before scanning any target
- **You must** comply with all applicable local, state, federal, and international laws
- **You must** respect website terms of service and robots.txt files
- **You must** use this tool responsibly and ethically

### Risk Acknowledgment
By using this application, you acknowledge and agree that:
- You understand the risks involved in security testing
- You are solely responsible for your actions and their consequences
- You will not hold the developers liable for any misuse or damages
- You will use this tool only on systems you own or have explicit permission to test

### Copyright & Intellectual Property
**WARNING:** This tool is protected by copyright and intellectual property laws.

**Official Distribution:** GitHub is the ONLY official and authorized distribution channel. Any copies found elsewhere are unauthorized and illegal.

**Strictly Prohibited:**
- **DO NOT** copy, reproduce, or distribute this tool outside of GitHub
- **DO NOT** reverse-engineer, decompile, or attempt to extract source code under any circumstances
- **DO NOT** create derivative works that are substantially similar to this tool
- **DO NOT** remove or alter copyright notices, watermarks, or attribution
- **DO NOT** upload this tool to other platforms, websites, or distribution channels
- **DO NOT** sell, license, or commercialize this tool in any form

**Reverse Engineering Protection:**
- This tool contains anti-tampering mechanisms and code obfuscation
- Any attempts to reverse-engineer will be detected and prosecuted
- Decompilation, debugging, or code extraction attempts are illegal
- We use advanced techniques to protect our intellectual property

**Allowed:** Creating tools *inspired by* the concepts or functionality, provided they are:
- Original implementations with your own code (no copying)
- Not direct copies or near-identical reproductions
- Properly attributed if referencing concepts
- Distributed through your own GitHub repository with proper attribution

**Enforcement:** We actively monitor all platforms for copyright infringement and will take down unauthorized copies through legal means including DMCA notices, cease and desist letters, and legal action if necessary. Violators may face criminal charges.

### No Warranty
This software is provided "AS IS" without any warranties, express or implied. The developers make no guarantees about the software's functionality, reliability, or suitability for any purpose.

## FAQ

### How many paths are scanned by default?
The scanner includes 200+ built-in admin and sensitive paths covering common admin panels, login pages, configuration files, and sensitive directories.

### Can I add my own paths?
Yes! Use the "Import Wordlist" feature to load custom paths from a .txt file. Each path should be on a separate line.

### What do the different colors mean?
- **Green (200):** Path exists and is accessible
- **Yellow (301/302):** Path redirects to another location
- **Orange (403):** Path exists but access is forbidden
- **Grey (404):** Path does not exist
- **White:** Other status codes or errors

### How long does a scan take?
Scan time depends on:
- Number of paths in your wordlist
- Delay setting between requests
- Target server response time
- Network conditions

Typical scans with default settings take 2-10 minutes.

### Is this tool legal to use?
This tool is legal for authorized security testing only. Always get explicit permission before scanning any target you don't own.

## Troubleshooting Tips

### Scan is very slow
- Reduce the delay setting (but be careful not to overwhelm the server)
- Check your internet connection
- Verify the target server is responding

### Getting many 404 errors
- This is normal! Most paths won't exist on most servers
- Focus on 200, 301/302, and 403 responses for interesting findings

### Connection errors
- Verify the target domain is correct
- Check if the website is accessible in your browser
- Try adding https:// if you used http:// (or vice versa)

## Version

**v1.0** Initial release

---

**Thank you for using Admin Path Scanner!**  
Remember to use responsibly and only on authorized targets.
