import os
import time
import random
import csv
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv

# Load credentials from .env
load_dotenv()
EMAIL = os.getenv("LINKEDIN_EMAIL")
PASSWORD = os.getenv("LINKEDIN_PASSWORD")
CSV_FILE = "applied_jobs.csv"

def human_sleep(min_sec=2, max_sec=5):
    time.sleep(random.uniform(min_sec, max_sec))

def log_applied_job(title, company, link, status="Applied", filename=CSV_FILE):
    file_exists = os.path.isfile(filename)
    with open(filename, mode="a", newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Title", "Company", "Link", "Status", "Timestamp"])
        writer.writerow([title, company, link, status, datetime.now().isoformat()])

def linkedin_login(driver):
    driver.get('https://www.linkedin.com/login')
    human_sleep(2, 4)

    driver.find_element(By.ID, 'username').send_keys(EMAIL)
    driver.find_element(By.ID, 'password').send_keys(PASSWORD)
    driver.find_element(By.ID, 'password').send_keys(Keys.RETURN)
    human_sleep(3, 6)

    current_url = driver.current_url.lower()
    if "checkpoint" in current_url or "captcha" in current_url:
        print("\n[!] CAPTCHA or verification triggered.")
        input("    Please complete CAPTCHA manually, then press Enter...\n")
        human_sleep(3, 5)
    else:
        print("[+] Logged in successfully.\n")

def search_internships(driver, keyword="cybersecurity", location="Virginia", skill_level="internship"):
    search_url = f"https://www.linkedin.com/jobs/search/?keywords={keyword}&location={location}&f_TP=1%2C2&f_AL=true&f_E=1%2C2&f_JT={skill_level}"
    driver.get(search_url)
    human_sleep(3, 5)

    jobs = driver.find_elements(By.CLASS_NAME, 'base-card')
    if not jobs:
        print("[!] No jobs found.")
        input("Press Enter to exit and close browser...")
        return []

    print(f"[+] Found {len(jobs)} job listings.\n")
    return jobs

def apply_to_easy_apply_jobs(driver, jobs):
    print("[*] Beginning Easy Apply process...\n")

    for i, job in enumerate(jobs):
        try:
            driver.execute_script("arguments[0].scrollIntoView();", job)
            job.click()
            human_sleep(3, 5)

            try:
                title = driver.find_element(By.CLASS_NAME, 'jobs-unified-top-card__job-title').text.strip()
                company = driver.find_element(By.CLASS_NAME, 'jobs-unified-top-card__company-name').text.strip()
                link = driver.current_url
            except:
                title = company = link = "N/A"

            easy_apply_button = driver.find_element(By.XPATH, '//button[contains(@class, "jobs-apply-button")]')
            if easy_apply_button:
                print(f"[{i+1}] Easy Apply found for: {title} at {company}")
                easy_apply_button.click()
                human_sleep(2, 4)

                try:
                    submit_button = driver.find_element(By.XPATH, '//button[contains(@aria-label, "Submit application")]')
                    submit_button.click()
                    print("   [+] Application submitted!\n")
                    log_applied_job(title, company, link, "Applied")
                except:
                    print("   [!] Complex application. Skipping auto-submit.\n")
                    log_applied_job(title, company, link, "Skipped - Complex Form")
                    try:
                        close_btn = driver.find_element(By.XPATH, '//button[contains(@aria-label, "Dismiss")]')
                        close_btn.click()
                    except:
                        pass

            else:
                print(f"[{i+1}] No Easy Apply button. Skipping.\n")
                log_applied_job(title, company, link, "Skipped - No Easy Apply")

        except Exception as e:
            print(f"[{i+1}] Error during apply: {e}\n")
            try:
                log_applied_job(title, company, link, f"Error: {e}")
            except:
                pass

        human_sleep(3, 6)

if __name__ == "__main__":
    print("[*] Launching Chrome WebDriver...")
    driver = webdriver.Chrome()

    try:
        linkedin_login(driver)
        jobs = search_internships(driver)
        if jobs:
            apply_to_easy_apply_jobs(driver, jobs)
    finally:
        print("[-] Process complete. Closing browser.")
        driver.quit()