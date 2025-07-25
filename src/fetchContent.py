from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import deque
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from typing import List, Tuple
from urllib.parse import urlparse, urlunparse

excluded_roles = {'navigation', 'banner'}
heading_tags = {'h1', 'h2', 'h3'}

# Helper function to check if a tag is inside an excluded-role div
def is_excluded(tag):
    while tag is not None:
        # Exclude <div> with role in excluded_roles
        if tag.name == 'div' and tag.get('role') in excluded_roles:
            return True
        # Exclude <li> with class "navbar-right"
        if tag.name == 'li' and 'navbar-right' in tag.get('class', []):
            return True
        tag = tag.parent
    return False

def extract_text_skip_excluded(tag):
    if is_excluded(tag) or tag is None:
        return ''
    
    if tag.name == 'a':
        href = tag.get('href')
        return f'[LINK: {href}]' if href else ''
    
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

def split_html_by_sections(soup: BeautifulSoup, url: str, contentId: str = "main") -> List[Tuple[str, int, str]]:
    main_div = soup.find('div', id=contentId)
    if not main_div:
        return []

    chunks = []
    current_chunk = ""

    # Iterate over immediate children only (recursive=False)
    for child in main_div.find_all(recursive=False):
        if is_excluded(child):
            continue

        if child.name in heading_tags:
            # Save previous chunk if exists
            if current_chunk.strip():
                chunks.append((url, current_chunk.strip()))
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
        chunks.append((url, current_chunk.strip()))

    return chunks

def normalize_url(url):
    parsed = urlparse(url)
    # Keep only scheme, netloc, and path
    return urlunparse((parsed.scheme, parsed.netloc, parsed.path, '', '', ''))

def crawl_site(driver, start_url, output_file, contentId="main", max_level=2):
    domain = urlparse(start_url).netloc
    visited = set()
    exclude_patterns = ["dashboard", "settings/", "account", "appointments", "/profile"]
    queue = deque([(start_url, 0)])

    with open(output_file, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['url', 'content'])  # Header

        while queue:
            url, level = queue.popleft()
            normalized = normalize_url(url)
            if normalized in visited or level > max_level or any(pattern in url.lower() for pattern in exclude_patterns) :
                continue
            visited.add(normalized)

            try:
                driver.get(url)
                if "resources/search" in url.lower():
                    time.sleep(10)
                else:
                    time.sleep(1)

                html =  driver.page_source
                soup = BeautifulSoup(html, 'html.parser')
                chunks = split_html_by_sections(soup, url, contentId)
                for row in chunks:
                    writer.writerow(row)
                
                print(f"[Level {level}] {url}")

                if level < max_level:
                    for link in soup.find_all('a', href=True):
                        href = link['href']
                        if (not href or
                            href.startswith('mailto:') or
                            href.startswith('javascript:') or
                            href == '/students/logout'):
                            continue  # Skip unwanted links
                        
                        full_url = urljoin(url, href)
                        if urlparse(full_url).netloc == domain and full_url not in visited:
                            queue.append((full_url, level + 1))

            except Exception as e:
                print(f"❌ Error on {url}: {e}")
                continue

    print(f"\n✅ Done! Output saved to '{output_file}'")

# Setup Chrome
options = Options()
options.add_argument('--log-level=3')
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument('--start-maximized')

driver = webdriver.Chrome(options=options)

start_url = "https://successportal.conestogac.on.ca/students/resources/search/?order=Relevance&topicsUseAnd=true&take=428"
driver.get(start_url)

# Wait for user to log in manually
print("⏳ Waiting for manual login...")
time.sleep(40)  # You can adjust the time
crawl_site(driver, start_url, 'data/conestogac_successportal.csv', max_level=5)
driver.quit()

# crawl_site(driver, 'https://www.conestogac.on.ca', 'data/conestogac.csv', 'maincontent', 4)
# driver.quit()

print(f"\n✅ Crawl completed.")

