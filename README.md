# NSL - Nmap Script Lookup
 
NSL (Nmap Script Lookup) is a lightweight Python-based utility designed to help security professionals, penetration testers, students, and Nmap users quickly search, discover, and reference Nmap NSE (Nmap Scripting Engine) scripts from a simple interface.
 
Instead of manually browsing hundreds of NSE scripts, NSL provides a faster way to locate scripts relevant to specific services, protocols, technologies, and testing objectives.
 
---
 
## Features
 
- Search NSE scripts quickly
- Lookup scripts by keyword
- Review script information in a convenient format
- Ideal for penetration testing and security assessments
- Lightweight and easy to run
- Built entirely in Python
 
---
 
## Why NSL?
 
The Nmap Scripting Engine contains hundreds of powerful scripts covering:
 
- Enumeration
- Vulnerability Detection
- Authentication Checks
- Brute Force Testing
- Service Discovery
- Malware Detection
- Information Gathering
 
Finding the right script can sometimes be time-consuming.
 
NSL aims to simplify that process by acting as a quick reference and lookup tool for NSE scripts.
 
---
 
## Requirements
 
### Python
 
- Python 3.8 or newer recommended
- Python 3.x required
 
Check your version:
 
```bash
python --version
```
 
---
 
## Installation
 
### Clone the Repository
 
```bash
git clone https://github.com/k7fi/NSL.git
cd NSL
```
 
### Install Dependencies
 
```bash
pip install -r requirements.txt
```
 
---
 
## Running NSL
 
Execute the tool using:
 
```bash
python NSL_0.py
```
 
---
 
## Windows Users
 
If you encounter issues related to command-line input handling, install `pyreadline3` manually:
 
```bash
pip install pyreadline3
```
 
---
 
## Example Use Cases
 
### Finding SMB Scripts
 
Search for:
 
```
smb
```
 
Possible results may include scripts related to:
 
- SMB enumeration
- SMB security checks
- SMB vulnerability detection
 
### Looking for HTTP Scripts
 
Search for:
 
```
http
```
 
Results can help identify scripts for:
 
- Web server enumeration
- Security header checks
- HTTP authentication testing
 
---
 
## Typical Workflow
 
1. Launch NSL.
2. Enter a keyword or service name.
3. Review matching NSE scripts.
4. Select a script of interest.
5. Use the script with Nmap.
 
Example:
 
```bash
nmap --script http-title target.com
```
 
or
 
```bash
nmap --script smb-os-discovery 192.168.1.10
```
 
---
 
## Project Structure
 
```text
NSL/
│
├── NSL_0.py
├── README.md
├── requirements.txt
└── nmap_script_lookup/
```
 
---
 
## Target Audience
 
This project is useful for:
 
- Penetration Testers
- Red Team Operators
- Blue Team Analysts
- Cybersecurity Students
- Nmap Enthusiasts
- Security Researchers
 
---
 
## Troubleshooting
 
### Dependency Errors
 
Update pip:
 
```bash
python -m pip install --upgrade pip
```
 
Then reinstall:
 
```bash
pip install -r requirements.txt
```
 
### Windows Terminal Issues
 
Install:
 
```bash
pip install pyreadline3
```
 
### Python Not Found
 
Verify Python installation:
 
```bash
python --version
```
 
If unavailable, install Python from:
 
https://www.python.org/downloads/
 
---
 
## Contributing
 
Contributions, bug reports, suggestions, and feature requests are welcome.
 
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Submit a Pull Request
 
---
 
## Future Improvements
 
- Advanced filtering
- Script categorization
- Search by NSE category
- CVE-based lookup
- TUI/GUI interface
- Offline database support
- Export search results
 
---
 
## Disclaimer
 
This tool is intended for educational, research, and authorised security testing purposes only.
 
Users are responsible for ensuring their activities comply with applicable laws, policies, and regulations.
 
---
 
## Author
 
**Ebrahim Albaker**
 
GitHub: https://github.com/k7fi
