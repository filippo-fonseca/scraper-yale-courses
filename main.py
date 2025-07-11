from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

# Setup driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Define current and old terms
current_terms = {
    "Fall 2025": "202503",
    "Spring 2026": "202601"
}
old_terms = {
    "Fall 2024": "202401",
    "Spring 2025": "202403"
}

subject = "MENG"  # You can change this to any subject

# Step 1: Fetch old course titles and codes (3-digit era)
old_courses_by_title = {}

for term_name, term_code in old_terms.items():
    url = f"https://courses.yale.edu/?srcdb={term_code}&subject={subject}"
    driver.get(url)
    time.sleep(5)

    results = driver.find_elements(By.CLASS_NAME, "result__headline")
    for result in results:
        try:
            title = result.find_element(By.CLASS_NAME, "result__title").text.strip()
            code = result.find_element(By.CLASS_NAME, "result__code").text.strip()
            if title not in old_courses_by_title:
                old_courses_by_title[title] = code
        except Exception:
            continue

# Step 2: Fetch current course titles and codes (4-digit era) and match
for term_name, term_code in current_terms.items():
    print(f"\n=== {term_name} ({subject}) ===")
    url = f"https://courses.yale.edu/?srcdb={term_code}&subject={subject}"
    driver.get(url)
    time.sleep(5)

    results = driver.find_elements(By.CLASS_NAME, "result__headline")
    for result in results:
        try:
            title = result.find_element(By.CLASS_NAME, "result__title").text.strip()
            code = result.find_element(By.CLASS_NAME, "result__code").text.strip()
            if title in old_courses_by_title:
                old_code = old_courses_by_title[title]
                print(f"{code}: {title} (previously {old_code})")
            else:
                print(f"{code}: {title}")
        except Exception:
            continue

driver.quit()
