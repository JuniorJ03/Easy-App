# LinkedIn Cybersecurity Internship Scraper

A Python script that automates logging into LinkedIn and scrapes cybersecurity internship job listings based on keyword, location, and experience level filters using Selenium.

---

## Features

- Logs into LinkedIn securely using credentials stored in a `.env` file.
- Detects CAPTCHA or verification pages and prompts manual solving.
- Searches for internships based on keywords, location, and experience levels.
- Prints job titles, companies, and links.
- Uses human-like random delays to reduce bot detection.

---

## Prerequisites

- Python 3.7+
- Google Chrome browser
- ChromeDriver (compatible with your Chrome version) installed and added to your system PATH.
- `pip` installed Python packages:
  - `selenium`
  - `python-dotenv`

---

## Setup Instructions

1. **Clone the repository or download the script**

2. **Install dependencies**

```bash
pip install selenium python-dotenv
