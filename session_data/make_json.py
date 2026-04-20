import json
import pickle
import requests
import time

from bs4 import BeautifulSoup as bs
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# selenium settings
chromedriver = "C:/Users/hi/Desktop/chromedriver-win64/chromedriver.exe"
service = Service(executable_path=chromedriver)

driver = webdriver.Chrome(service=service)
driver.implicitly_wait(15)

wait = WebDriverWait(driver, 10)


with open("session_links.pickle", 'rb') as fr :
    links = pickle.load(fr)

# links 하나로 모아 set으로 만들어 중복 제거
filtered_links = set([])
for idx in range(19) :
    filtered_links.update(links[idx])

data = []
errors = []
for idx, url in enumerate(filtered_links) :
    print(idx, ':', url)
    try :
        session = {}
        page = requests.get(url)
        soup = bs(page.text, 'html.parser')


        session['title'] = soup.find('h1').text

        video_container = soup.find(id='tenant-video-container')

        vc_sibling = video_container.find_next_sibling('div')
        target_divs = vc_sibling.find_all('div')

        date_str = target_divs[0].text.split(' | ')[0].split('Posted ')[1]
        session['date'] = datetime.strptime(date_str, "%b %d, %Y")

        session['category'] = target_divs[1].text.split('# ')[1:]

        # speakers
        speakers_div = video_container.find_next_siblings('div')[1].find_all('div', recursive=False)
        session['speakers'] = []
        for speaker_div in speakers_div :
            speaker = {}
            speaker['img'] = speaker_div.find('img').get('src')
            speaker['introduction'] = speaker_div.find('p').text

            speaker_right_div = speaker_div.find_all('div', recursive=False)[1]
            speaker['name'] = speaker_right_div.find_all('div')[0].text
            speaker['position'], speaker['organization'] = speaker_right_div.find_all('div')[1].text.split(' @ ')

            session['speakers'] .append(speaker)

        # get video link
        driver.get(url)
        # 1. 일단 영상 근처로 스크롤
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);") 
        time.sleep(3) # 충분히 기다림

        # 2. 아주 단순하게 모든 iframe 다 찾기 (Shadow DOM 무시 버전)
        final_attempt_js = """
        let results = [];
        // 1. 일반 DOM의 iframe
        document.querySelectorAll('iframe').forEach(f => results.push(f.getAttribute('data-src') || f.src));

        // 2. Shadow DOM 내부의 iframe (전역 검색)
        function findAll(root) {
            root.querySelectorAll('*').forEach(el => {
                if (el.tagName === 'IFRAME') results.push(el.getAttribute('data-src') || el.src);
                if (el.shadowRoot) findAll(el.shadowRoot);
            });
        }
        findAll(document);

        return results.filter(src => src && src.includes('vimeo')).join(', ');
        """

        vimeo_num = driver.execute_script(final_attempt_js).split('?')[0].split('/')[-1]
        session['video_url'] = 'https://vimeo.com/' + vimeo_num

        # Description
        # 1. 모든 h2를 찾아서 2번째(인덱스 1) h2를 선택합니다.
        all_h2 = soup.find_all('h2')

        if len(all_h2) >= 3:
            target_h2 = all_h2[1]
            # 2. h2 바로 다음에 오는 첫 번째 형제 div를 찾습니다.
            next_div = target_h2.find_next_sibling('div')
            
            if next_div:
                # 3. 해당 div 안에 있는 모든 p 태그의 텍스트를 추출합니다.
                p_tags = next_div.find_all('p')
                summary_text = "\n".join([p.get_text(strip=True) for p in p_tags])

                session['description'] = summary_text
                session['summary'] = ''

        data.append(session)
    except Exception :
        errors.append((idx, url))

# data = json.dumps(data, default=str, ensure_ascii=False)
# 결과: {"name": "example", "created_at": "2026-04-17 10:00:00.000000"}

with open("./session.json", "w", encoding="utf-8") as json_file:
    json.dump(data, json_file, default=str, ensure_ascii=False)

print(errors)
with open("./errors.pickle","wb") as fw:
    pickle.dump(errors, fw)