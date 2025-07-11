from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

# Setup driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
subject = "MENG"

# Define terms
current_terms = {
    "Fall 2025": "202503",
    "Spring 2026": "202601"
}
old_terms = {
    "Fall 2024": "202401",
    "Spring 2025": "202403"
}
credit_hours = ["0.5", "1", "1.5", "2"]

# Step 1: Build old course map (title → old code)
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

# Step 2: Fetch new courses with credit filters and match
for term_name, term_code in current_terms.items():
    print(f"\n=== {term_name} ({subject}) ===")
    for hours in credit_hours:
        url = f"https://courses.yale.edu/?srcdb={term_code}&subject={subject}&hours={hours}"
        driver.get(url)
        time.sleep(5)

        results = driver.find_elements(By.CLASS_NAME, "result__headline")
        for result in results:
            try:
                title = result.find_element(By.CLASS_NAME, "result__title").text.strip()
                code = result.find_element(By.CLASS_NAME, "result__code").text.strip()
                credit_display = f"{hours} credit" if hours != "1" else "1 credit"

                if title in old_courses_by_title:
                    old_code = old_courses_by_title[title]
                    print(f"{code}: {title} ({credit_display}) (previously {old_code})")
                else:
                    print(f"{code}: {title} ({credit_display})")
            except Exception:
                continue

driver.quit()
