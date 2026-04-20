import pickle
import time
from collections import defaultdict
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

chromedriver = "C:/Users/hi/Desktop/chromedriver-win64/chromedriver.exe"
service = Service(executable_path=chromedriver)

driver = webdriver.Chrome(service=service)
driver.implicitly_wait(15)

wait = WebDriverWait(driver, 10)

url = "https://forum.openai.com/public/content?category=video"
driver.get(url)

# popular
popular_button = wait.until(EC.element_to_be_clickable(
    (By.XPATH, "//button[.//span[text()='Popular']]")
))
popular_button.click()
print("Popular 버튼 클릭 완료")
time.sleep(5)

contents = defaultdict(list)

# tag select
for idx in range(1, 20) : # 20
    print(idx)
    # --- 1. "Select content tag" 드롭다운 열기 ---
    print("Tag 드롭다운 열기 시도...")
    # aria-label이 'Select content tag'인 input을 포함한 가장 가까운 부모 selector div를 찾습니다.
    tag_dropdown = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//input[@aria-label='Select content tag']/ancestor::div[contains(@class, 'rc-select-selector')]")
    ))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", tag_dropdown)
    time.sleep(1) # 스크롤 애니메이션이 끝날 때까지 잠시 대기
    # ActionChains로 확실하게 이동 후 클릭
    actions = ActionChains(driver)
    actions.move_to_element(tag_dropdown).click().perform()

    # 목록이 뜰 때까지 대기
    time.sleep(5)

    # 여기서 옵션 선택 코드 진행...
    tag_options = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".rc-select-item-option")))

    tag_options[idx].click()

    time.sleep(5)

    sessions = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[data-content-item='true']")))
    links = []
    for session in sessions:
        try:
            link_element = session.find_element(By.CSS_SELECTOR, "div > div:nth-child(2) a")
            link = link_element.get_attribute("href")
            links.append(link)
        except Exception:
            # 링크가 없는 아이템이 있을 수 있으므로 예외처리
            continue
    contents[idx] = links

    print(f"{idx}까지의 contents 저장 중")
    with open("./session_links.pickle","wb") as fw:
        pickle.dump(contents, fw)

    print(f"{idx}까지의 contents 저장 완료")


