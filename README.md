# 📰 HN Translator

> A Python tool that scrapes Hacker News top stories and auto-translates titles into Chinese — delivered as clean Markdown reports.

[![Python](https://img.shields.io/badge/Python-3.14-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-active-success.svg)]()

---

## ✨ Features

- 🔍 **Scrapes top 20 stories** from Hacker News front page
- 🌐 **Auto-translates** English titles to Chinese (via MyMemory API)
- 📄 **Outputs clean Markdown** reports with date stamps
- ⚡ **Fast & lightweight** — runs in under 30 seconds
- 🎯 **Zero config** — works out of the box

---

## 📸 Demo

Example output (`hn-summary-2026-05-14.md`):

markdown
# Hacker News Daily Digest — 2026-05-14

1. **Show HN: A new way to learn programming**
   显示HN:学习编程的新方法
   Score: 312 | Comments: 89

2. **OpenAI releases new reasoning model**
   OpenAI发布新的推理模型
   Score: 521 | Comments: 234


---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- pip

### Installation

bash
# Clone the repo
git clone https://github.com/houvincent/hn-translator.git
cd hn-translator

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt


### Usage

bash
python hn_translate.py


Output: `hn-summary-YYYY-MM-DD.md`

---

## 🛠️ Tech Stack

- **Python 3.14** — Core language
- **BeautifulSoup4** — HTML parsing
- **Requests** — HTTP client
- **MyMemory API** — Free translation service

---

## 📂 Project Structure


hn-translator/
├── hn_translate.py          # Main script
├── requirements.txt         # Python dependencies
├── .gitignore               # Git ignore rules
├── README.md                # You are here
└── hn-summary-*.md          # Generated reports


---

## 🎯 Use Cases

- 📰 **Daily news digest** for Chinese-speaking developers
- 🌍 **Bilingual content** generation for blogs and newsletters
- 📊 **Data collection** for tech trend research
- 🤖 **Foundation** for AI-powered news bots

---

## 🔮 Roadmap

- [ ] Support Show HN / Ask HN sections
- [ ] Integrate Claude API for higher quality translation
- [ ] Email digest delivery
- [ ] Web dashboard
- [ ] Multi-language support (JP, KR, ES)

---

## 👨‍💻 About the Author

I'm **Vincent**, an independent developer specializing in:

- 🐍 **Python automation** & web scraping
- 🤖 **AI tools** (Claude, OpenAI, Gemini APIs)
- 📊 **Data extraction** & processing

### 💼 Available for Hire

Need a custom scraper, automation tool, or AI integration?

➡️ **Get in touch** — freelance services launching soon.

I respond within 6 hours.

---

## 📄 License

MIT License — feel free to use, modify, and share.

---

## ⭐ Show Your Support

If this project helped you, please consider giving it a ⭐ on GitHub!
