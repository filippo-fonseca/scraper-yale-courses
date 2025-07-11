import os
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# Setup
subject = "MENG"  # Change this for other departments
output_dir = "data"
os.makedirs(output_dir, exist_ok=True)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Term codes
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

# Step 2: Build list of unique courses for current terms
seen_titles = set()
course_entries = []

for term_name, term_code in current_terms.items():
    for hours in credit_hours:
        url = f"https://courses.yale.edu/?srcdb={term_code}&subject={subject}&hours={hours}"
        driver.get(url)
        time.sleep(5)

        results = driver.find_elements(By.CLASS_NAME, "result__headline")
        for result in results:
            try:
                title = result.find_element(By.CLASS_NAME, "result__title").text.strip()
                code = result.find_element(By.CLASS_NAME, "result__code").text.strip()
                credits = float(hours)

                # Avoid duplicates across terms/hours
                if title in seen_titles:
                    continue
                seen_titles.add(title)

                codes = [code]
                if title in old_courses_by_title:
                    codes.append(old_courses_by_title[title])

                course_entry = {
                    "codes": codes,
                    "name": title,
                    "credits": credits,
                    "department": subject
                }

                course_entries.append(course_entry)

            except Exception:
                continue

driver.quit()

# Step 3: Write to JSON
output_path = os.path.join(output_dir, f"{subject}.json")
with open(output_path, "w") as f:
    json.dump(course_entries, f, indent=2)

print(f"✅ Saved {len(course_entries)} courses to {output_path}")
