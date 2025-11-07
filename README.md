# 🧠 Incident Insights
### A Windows Forensic Log Analyzer for Investigators & Researchers  
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](./LICENSE)
[![Tests](https://github.com/yourusername/incident-insights/actions/workflows/test.yml/badge.svg)](https://github.com/yourusername/incident-insights/actions)
[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)](#-contributing)

---

## 🧩 Overview

**Incident Insights** is a Python-based command-line tool designed to help forensic analysts and cybersecurity students extract and correlate evidence from **Windows artefacts**.

It parses Event Logs, Registry Hives, and USB device history to detect:
- Suspicious logon activity  
- USB connections and disconnections  
- Process creation events  
- Installed software and system changes  

This project is built with modularity and transparency in mind, providing structured outputs for both **human reports** and **machine parsing**.

---

## 🚀 Features

- 🔍 Parse Windows Event Logs (`.evtx`)
- 🧱 Extract USB and user activity from Registry Hives
- 🧠 Detect suspicious processes and logons
- 🧾 Generate reports in **HTML**, **JSON**, or **Markdown**
- 🗂️ Store parsed data in **SQLite** for query-based analysis
- 💻 Simple, extensible **CLI interface**
- ✅ Tested with **pytest** and CI integration

---

## 🏗️ Project Structure

incident_insights/
│
├── incident_insights/
│ ├── cli.py
│ ├── parsers/
│ │ ├── evtx_parser.py
│ │ ├── registry_parser.py
│ │ └── usb_parser.py
│ ├── analyzers/
│ │ ├── usb_activity.py
│ │ ├── user_logon.py
│ │ └── suspicious_process.py
│ ├── reporters/
│ │ ├── html_report.py
│ │ └── json_report.py
│ └── utils/
│ ├── time_convert.py
│ └── paths.py
│
├── tests/
│ ├── test_evtx_parser.py
│ ├── test_registry_parser.py
│ └── test_usb_activity.py
│
├── requirements.txt
├── setup.py
├── LICENSE
└── README.md


---

## ⚙️ Installation

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/yourusername/incident-insights.git
cd incident-insights

python3 -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
pip install -r requirements.txt


python -m incident_insights parse --source ./evidence/
