import os
import re
import json
from time import sleep
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 配置路径
CHROME_BINARY_PATH = r"D:\ai_analysis_model\chrome-win64\chrome.exe"
CHROMEDRIVER_PATH = r"D:\ai_analysis_model\chromedriver-win64\chromedriver.exe"

# 匹配规则
EMAIL_RE = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
PHONE_RE = r'(\+?\d[\d\s\-\.\(\)]{7,}\d)'
BAD_DOMAINS = ['zhihu.com', 'baidu.com', 'bilibili.com', 'weibo.com', 'jianshu.com']
VALID_EMAIL_SUFFIXES = ['.com', '.net', '.org', '.cn', '.co.uk', '.de', '.edu']
CHINA_MOBILE_RE = r'^1[3-9]\d{9}$'
CHINA_LANDLINE_RE = r'^0\d{2,3}-?\d{7,8}$'
INTERNATIONAL_RE = r'^\+[\d\s\-().]{8,}$'

def create_driver():
    chrome_options = Options()
    chrome_options.binary_location = CHROME_BINARY_PATH
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-dev-shm-usage")
    service = Service(CHROMEDRIVER_PATH)
    return webdriver.Chrome(service=service, options=chrome_options)

def is_valid_url(url):
    return not any(bad in url for bad in BAD_DOMAINS)

def clean_emails(emails):
    cleaned = []
    for e in emails:
        e = e.strip().lower()
        if any(e.endswith(suf) for suf in VALID_EMAIL_SUFFIXES):
            if not any(skip in e for skip in ['noreply', 'example', 'admin@', '.png', '.jpg', '.jpeg', '.svg']):
                if '@' in e:
                    cleaned.append(e)
    return list(set(cleaned))

def clean_phones(phones):
    cleaned = []
    for p in phones:
        p = p.strip()
        digits_only = re.sub(r'\D', '', p)
        if re.fullmatch(CHINA_MOBILE_RE, digits_only):
            cleaned.append(digits_only)
        elif re.fullmatch(CHINA_LANDLINE_RE, p):
            cleaned.append(p)
        elif re.match(INTERNATIONAL_RE, p):
            cleaned.append(p)
    return list(set(cleaned))

def search_and_get_links_bing(driver, keyword, max_links=10):
    print(f"\n[Bing] 正在搜索关键词: {keyword}")
    query = f"https://www.bing.com/search?q={keyword}"
    driver.get(query)
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li.b_algo h2 a"))
        )
    except Exception:
        print("[!] Bing 搜索结果加载超时，尝试继续")
    links = []
    for a in driver.find_elements(By.CSS_SELECTOR, "li.b_algo h2 a"):
        href = a.get_attribute("href")
        if href and href.startswith("http") and is_valid_url(href):
            links.append(href)
        if len(links) >= max_links:
            break
    print(f"[Bing][DEBUG] 有效链接数: {len(links)}")
    return links

def search_serper_links(keyword, max_links=10):
    payload = {"q": keyword}
    url = "https://google.serper.dev/search"
    headers = {
        "X-API-KEY": "",  # 👈 用你自己的 API Key 替换
        "Content-Type": "application/json"
    }
    try:
        res = requests.post(url, headers=headers, json=payload, timeout=10)
        res.raise_for_status()
        data = res.json()
        links = []
        for item in data.get("organic", []):
            link = item.get("link")
            if link and link.startswith("http") and is_valid_url(link):
                links.append(link)
            if len(links) >= max_links:
                break
        print(f"[Serper] 共提取有效链接数: {len(links)}")
        return links
    except Exception as e:
        print(f"[Serper][错误] 搜索失败: {e}")
        return []

def extract_contacts_from_url(driver, url):
    try:
        driver.get(url)
        sleep(2)
        text = driver.page_source
        emails = clean_emails(re.findall(EMAIL_RE, text))
        phones = clean_phones(re.findall(PHONE_RE, text))
        if emails or phones:
            print(f"[✓] 提取到联系方式于: {url}")
            return {"url": url, "emails": emails, "phones": phones}
    except Exception as e:
        print(f"[x] 出错: {url} - {e}")
    return None

def run_engine(keyword, max_sites=10, output_path="contacts.json"):
    driver = create_driver()
    links_bing = search_and_get_links_bing(driver, keyword, max_sites)
    links_serper = search_serper_links(keyword, max_sites)
    all_links = list(dict.fromkeys(links_bing + links_serper))
    print(f"\n[INFO] 总共准备抓取 {len(all_links)} 个链接")
    results = []
    for link in all_links:
        print(f"[→] 正在处理: {link}")
        contact = extract_contacts_from_url(driver, link)
        if contact:
            results.append(contact)
        sleep(1)
    driver.quit()
    if results:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"\n[✓] 共提取 {len(results)} 条联系方式，已保存至 {output_path}")
    else:
        print("\n[!] 未提取到任何联系方式")
