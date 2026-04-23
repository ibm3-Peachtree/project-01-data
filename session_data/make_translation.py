import os
import json
import time

from google import genai
from google.genai.errors import ServerError
from openai import OpenAI

MODEL = "gemini-2.5-flash" 
# 관련 링크 https://ai.google.dev/gemini-api/docs/models/gemini-2.5-flash?hl=ko&_gl=1*t7dyb5*_up*MQ..*_ga*MTExNDkwNTA1My4xNzc2NDA0OTk1*_ga_P1DBVKWT6V*czE3NzY0MDQ5OTQkbzEkZzAkdDE3NzY0MDQ5OTQkajYwJGwwJGg4NjQ0Mjg0OTY.


with open('./gemini_apikey.json', 'r', encoding='utf-8') as key_j :
    json_api = json.load(key_j)
API_KEY = os.getenv("GEMINI_API_KEY", json_api['API_KEY'])

with open('./session_summary.json', 'r', encoding='utf-8') as j :
    session_data = json.load(j)



def run_flash_model(text:str)->str:
    instructions = """
        "===" 아래 입력은 AI Forum에서의 세션 강의 내용입니다. 
        AI Forum 한국인 참가자들에게 핵심 내용이 전달될 수 있도록 한국어로 번역해주세요.
        사족 붙이지 말고("결과 :" 등) 번역 내용만 작성해주세요.
        ===\n
    """
    text = instructions + text

    # Gemini
    client = genai.Client(api_key=API_KEY)
    response = client.models.generate_content(
        model=MODEL,
        contents=text,
    )
    answer = response.text
    
    return answer
# 40번째 데이터부터 시작하기
for idx in range(44, len(session_data)):
    print(f"--- {idx}번째 데이터 처리 중 ---")
    text = session_data[idx]['description']
    
    # 재시도 루프
    success = False
    for i in range(5):  # 최대 5번 재시도
        try:
            response = run_flash_model(text)
            session_data[idx]['kor_description'] = response
            success = True
            break  # 성공하면 재시도 루프 탈출
            
        except ServerError as e:
            if "503" in str(e):
                wait_time = (2 ** i) + 5  # 5, 7, 9... 조금 더 여유있게 대기
                print(f"서버 과부하(503). {wait_time}초 후 다시 시도합니다... (시도 {i+1}/5)")
                time.sleep(wait_time)
            else:
                # 503 이외의 심각한 에러는 바로 중단
                print(f"예상치 못한 서버 에러 발생: {e}")
                raise e
        except Exception as e:
            print(f"기타 에러 발생: {e}")
            time.sleep(65)
            
    if not success:
        print(f"⚠️ {idx}번째 데이터는 여러 번의 시도 끝에 실패했습니다.")

    print(f"결과: {session_data[idx]['kor_description']}")
    # 다음 API 호출 전 최소한의 매너 타임
    time.sleep(2)

    with open("./session_summary.json", "w", encoding="utf-8") as json_file:
        json.dump(session_data, json_file, default=str, ensure_ascii=False)






# run_flash_model(text)