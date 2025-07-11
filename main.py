from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://courses.yale.edu/?srcdb=202503&subject=AFAM")
time.sleep(5)

results = driver.find_elements(By.CLASS_NAME, "result__headline")

for result in results:
    try:
        code = result.find_element(By.CLASS_NAME, "result__code").text
        title = result.find_element(By.CLASS_NAME, "result__title").text
        print(f"{code}: {title}")
    except Exception as e:
        print("Skipping:", e)

driver.quit()
