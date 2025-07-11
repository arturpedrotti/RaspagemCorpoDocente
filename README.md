# FGV Faculty Scraper

A modular web application built with Streamlit in Python to scrape and display public faculty data from FGV's ECMI and EMAP departments.

Developed independently by [Artur Pedrotti](https://github.com/arturpedrotti), this project demonstrates structured data scraping and modular UI development with Python.

---

## 🔧 Requirements

Before running this project, make sure the following are installed:

- Git: https://git-scm.com/
- Python 3.x: https://www.python.org/downloads/
- pip: https://pip.pypa.io/en/stable/installation/
- Firefox: https://www.mozilla.org/en-US/firefox/new/

---

## 🚀 Quickstart (Cross-platform)

### Option 1 — Linux/macOS setup with script

Run the executable setup script:

    chmod +x executable.sh
    ./executable.sh

This will:
- Check Python, pip, and Firefox installation
- Install required dependencies
- Launch the Streamlit application

---

### Option 2 — Manual setup (All platforms)

Clone and run manually:

    git clone https://github.com/arturpedrotti/fgv-faculty-scraper
    cd fgv-faculty-scraper
    pip install -r requirements.txt
    streamlit run raspagemMain.py

---

## 📁 Project Structure

- `raspagemMain.py`: Streamlit app entry point
- `app_01.py`: ECMI scraping logic
- `app_02.py`: EMAP scraping logic
- `keywords.txt`: Keywords used to filter role descriptions
- `requirements.txt`: Project dependencies
- `executable.sh`: Quick setup script for Unix-like systems

---

## 🧪 Features

- Clean sidebar UI for navigation between ECMI and EMAP scraping
- Displays simplified staff data from official FGV sites
- Modular architecture for extending scraping logic
- Shell script support for rapid setup

---

## 📄 License

This repository is released for academic and demonstrative purposes only. Data usage should respect FGV’s public data sharing guidelines.

---

© 2025 Artur Pedrotti — All rights reserved.
