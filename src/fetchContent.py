import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import deque
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from typing import List, Tuple

excluded_roles = {'navigation', 'banner'}
heading_tags = {'h1', 'h2', 'h3'}

# Helper function to check if a tag is inside an excluded-role div
def is_in_excluded_role(tag):
    while tag is not None:
        if tag.name == 'div' and tag.get('role') in excluded_roles:
            return True
        tag = tag.parent
    return False

def extract_text_skip_excluded(tag):
    if is_in_excluded_role(tag):
        return ''
    if tag.name == 'a':  # skip <a> tags completely
        return ''
    if not hasattr(tag, 'children') or not list(tag.children):
        return tag.get_text(separator=" ", strip=True)
    texts = []
    for child in tag.children:
        if hasattr(child, 'name'):
            text = extract_text_skip_excluded(child)
            if text:
                texts.append(text)
        else:
            text = str(child).strip()
            if text:
                texts.append(text)
    return ' '.join(texts)

def split_html_by_sections(soup: BeautifulSoup, url: str) -> List[Tuple[str, int, str]]:
    main_div = soup.find('div', id='maincontent')
    if not main_div:
        return []

    chunks = []
    current_chunk = ""
    chunk_index = 1

    # Iterate over immediate children only (recursive=False)
    for child in main_div.find_all(recursive=False):
        if is_in_excluded_role(child):
            continue

        if child.name in heading_tags:
            # Save previous chunk if exists
            if current_chunk.strip():
                chunks.append((url, chunk_index, current_chunk.strip()))
                chunk_index += 1
                current_chunk = ""

            # Start new chunk with heading text
            heading_text = extract_text_skip_excluded(child)
            if heading_text:
                current_chunk += heading_text + " "
        else:
            # Add text from other tags
            text = extract_text_skip_excluded(child)
            if text:
                current_chunk += text + " "

    # Add last chunk if any
    if current_chunk.strip():
        chunks.append((url, chunk_index, current_chunk.strip()))

    return chunks

def crawl_site(session, start_url, output_file, max_level=2):
    domain = urlparse(start_url).netloc
    visited = set()
    queue = deque([(start_url, 0)])

    with open(output_file, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['url', 'chunk_number', 'content'])  # Header

        while queue:
            url, level = queue.popleft()
            if url in visited or level > max_level:
                continue
            visited.add(url)

            try:
                response = session.get(url, timeout=10)
                if response.status_code != 200:
                    continue

                soup = BeautifulSoup(response.text, 'html.parser')
                chunks = split_html_by_sections(soup, url)
                for row in chunks:
                    writer.writerow(row)
                
                print(f"[Level {level}] {url}")

                if level < max_level:
                    for link in soup.find_all('a', href=True):
                        full_url = urljoin(url, link['href'])
                        if urlparse(full_url).netloc == domain and full_url not in visited:
                            queue.append((full_url, level + 1))

            except Exception as e:
                print(f"❌ Error on {url}: {e}")
                continue

    print(f"\n✅ Done! Output saved to '{output_file}'")

# --- Configuration ---
# max_level = 0  # ⬅️ Change this to control how deep you want to crawl
# crawl_site(requests.Session(), 'https://www.conestogac.on.ca/subsidized-training/academic-upgrading', 'data/conestogac.csv', 0)

# # Setup Chrome
# options = Options()
# options.add_argument('--log-level=3')  # Suppress most logs
# options.add_experimental_option('excludeSwitches', ['enable-logging'])
# options.add_argument('--start-maximized')  # Not headless for login
# driver = webdriver.Chrome(options=options)

# start_url = "https://successportal.conestogac.on.ca/"
# # Step 1: Go to login page and complete login manually (if needed)
# driver.get(start_url)
# time.sleep(50)  # Wait for manual login if needed

# # Step 2: Save cookies
# cookies = driver.get_cookies()
# driver.quit()

# # Step 3: Use cookies in requests session
# session = requests.Session()
# for cookie in cookies:
#     session.cookies.set(cookie['name'], cookie['value'])

# # --- Step 5: Crawl the page (or start your full crawl) ---
# response = session.get(start_url)
# print("\n✅ Page content:")
# print(response.text[:500])  # Print first 500 characters

# crawl_site(session, 'https://successportal.conestogac.on.ca/', 'data/conestogac_successportal.csv', max_level)


print(f"\n✅ Crawl completed.")

