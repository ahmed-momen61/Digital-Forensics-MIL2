Windows Registry Forensic Artifact Extractor

- Overview

This Python script is a lightweight digital forensics tool designed to automate the extraction of critical artifacts from standard Windows Registry hives. It was developed as part of a forensic investigation case study to analyze user behavior, installed applications, and system usage on a Windows 7 workstation.

The tool parses the raw registry hive files (SAM, SOFTWARE, SYSTEM, NTUSER.DAT) to provide a quick triage summary without requiring heavy forensic suites like EnCase or FTK for the initial analysis.

- Features

The script performs the following automated analyses:

User Account Enumeration:

Reads the SAM hive.

Lists all local user accounts found on the system.

Installed Applications:

Reads the SOFTWARE hive.

Extracts the display name and version of installed software from Microsoft\Windows\CurrentVersion\Uninstall.

USB Device History:

Reads the SYSTEM hive.

Parses the USBSTOR key to identify connected external devices.

Extracts Vendor, Product ID, Friendly Name (if available), and the Last Connected Timestamp.

User Activity Analysis:

Reads the NTUSER.DAT hive.

RunMRU: Decodes and lists commands typed into the Windows "Run" box.

UserAssist: automatically decrypts ROT13 encoded entries to reveal a history of executed programs (GUI applications).

- Prerequisites

To run this script, you need:

Python 3.x installed on your system.

The third-party library python-registry.

Installation

Install the required library using pip:

pip install python-registry


 - Usage

Step 1: Export Registry Hives

This script does not run on the live system registry; it analyzes exported hive files. You must extract the following files from your forensic disk image (using tools like FTK Imager or Autopsy):

SAM: C:\Windows\System32\config\SAM

SOFTWARE: C:\Windows\System32\config\SOFTWARE

SYSTEM: C:\Windows\System32\config\SYSTEM

NTUSER.DAT: C:\Users\[USERNAME]\NTUSER.DAT (Hidden file)

Step 2: Run the Script

Place the script in the same folder as your extracted hives (optional but recommended) and run it via the command line:

python forensic_extractor.py


Step 3: Follow the Prompts

The script attempts to find the hive files automatically in the current directory. If a file is missing, it will prompt you to enter the full path. You can simply drag and drop the file into the terminal window when asked.

- Code Structure

The code is modularized for clarity:

rot13(s): Helper function to decode UserAssist entries.

show_user_accounts(): Iterates through SAM\Domains\Account\Users.

show_installed_apps(): Iterates through Uninstall keys in SOFTWARE.

show_usb_history(): Recursively parses Enum\USBSTOR in SYSTEM.

show_user_activity(): Handles the logic for parsing RunMRU and decoding UserAssist in NTUSER.DAT.

- Disclaimer

This tool is intended for educational and authorized forensic analysis purposes only. Always ensure you have the legal right to analyze the data you are processing.

- Author
  "AhmedMoamen.61"

[Your Name]
Digital Forensics Student / Analyst
