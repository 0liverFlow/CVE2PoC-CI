import requests
from bs4 import BeautifulSoup as bsoup
from playwright.sync_api import sync_playwright
import re
 
def search_thm_rooms():
    url = "https://tryhackme.com/module/recent-threats"

    cve_pattern = re.compile(r"CVE-\d{4}-\d+")

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)

        links = page.query_selector_all("a[href^='/room/']")

        results = []

        for link in links:
            text = link.inner_text().strip()
            href = link.get_attribute("href")

            match = cve_pattern.search(text)
            if match:
                cve = match.group()
                full_url = "https://tryhackme.com" + href
                results.append((cve, full_url))

        browser.close()
    
    return results
    
if __name__ == '__main__':
    latest_thm_rooms = search_thm_rooms()
    if latest_thm_rooms:
      with open('latest_thm_rooms.txt', 'a+') as f:
        default_thm_rooms = f.readlines()
        f.seek(0)
        thm_rooms = f.readlines()
        thm_rooms_cves = [cve.split(':')[0].lower() for cve in thm_rooms]
        for cve, machine in latest_thm_rooms:
            if cve.lower() not in thm_rooms_cves:
                f.write(f'{cve}:{machine}\n')
