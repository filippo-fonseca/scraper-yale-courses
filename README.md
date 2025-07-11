# scraper-yale-courses

This is what it does:

- Scrape Fall 2025 and Spring 2026 courses

- Match to old course titles (Fall 2024 and Spring 2025)

- Store each course with:

  - codes: array of codes (Fall 2025/Spring 2026 first, then any matched old codes)

  - name: course title

  - credits: numeric value

  - department: subject (e.g., "MENG")

- Save results to ./data/MENG.json (or ./data/{subject}.json)
