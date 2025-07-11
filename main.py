from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

# Initialize browser
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Define terms and subject
terms = {
    "Fall 2025": "202503",
    "Spring 2026": "202601"
}
subject = "MENG"  # Change this to whatever subject you want

for term_name, term_code in terms.items():
    url = f"https://courses.yale.edu/?srcdb={term_code}&subject={subject}"
    driver.get(url)
    time.sleep(5)  # Wait for JavaScript to load

    print(f"\n=== {term_name} ({subject}) ===")
    results = driver.find_elements(By.CLASS_NAME, "result__headline")

    if not results:
        print("No courses found.")
        continue

    for result in results:
        try:
            code = result.find_element(By.CLASS_NAME, "result__code").text
            title = result.find_element(By.CLASS_NAME, "result__title").text
            print(f"{code}: {title}")
        except Exception as e:
            print("Skipping:", e)

driver.quit()
