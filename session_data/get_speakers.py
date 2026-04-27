import os
import json
import time
import pickle

from google import genai
from google.genai.errors import ServerError

with open('C:\\Users\\hi\\Desktop\\peachtree\\project-01-data\\session_data\\session_summary.json', 'r', encoding='utf-8') as rj :
    session_data = json.load(rj)

MODEL = "gemini-2.5-flash" 

with open('./gemini_apikey.json', 'r', encoding='utf-8') as key_j :
    json_api = json.load(key_j)
API_KEY = os.getenv("GEMINI_API_KEY", json_api['API_KEY'])



def run_flash_model(speaker) -> str :
    instructions = f"""
        이것은 AI Forum 연사의 정보입니다.
        'introduction': {speaker['introduction']}, 
        'name': {speaker['name']}, 
        'position': {speaker['position']}, 
        'organization': {speaker['organization']}
        ===
        이를 바탕으로 AI Forum 웹사이트에 입력할 연사 이력을 작성해주세요.
        예를 들면 
        "year" : [2010, 2015],
        "content" : [OO대학교 컴퓨터공학과 박사 졸업, OpenAI 개발팀 Policy Researcher]

        이런식으로요. 연사 이력은 5개 이하로 introduction에서 추출할 수 있는 정도로 적어주세요.
        year에 Current라고 적지 말고 임의의 연도를 작성해주세요.

        요청에 맞게 작성했다는 미사여구 제외하고 JSON만 작성해주세요.
    """

    client = genai.Client(api_key=API_KEY)

    response = client.models.generate_content(
        model=MODEL,
        contents=instructions,
    )
    answer = response.text
    
    return answer

speakers = []
json_speakers = {}
if 'speakers.pickle' in os.listdir('./') :
    with open("./speakers.pickle", 'rb') as rp :
        speakers = pickle.load(rp)

if 'speakers.json' in os.listdir('./') :
    with open('./speakers.json', 'r', encoding='utf-8') as rj :
        json_speakers = json.load(rj)

print("===load 확인===")
print(speakers)
print(json_speakers)

time.sleep(30)

# 30번째부터 하기
for idx in range(42, len(session_data)) :
    print(f"--- {idx}번째 데이터 처리 중 ---")
    temp = session_data[idx]['speakers']

    for t in temp :
        if t['name'] not in speakers :
            success = False
            for i in range(5) :
                try :
                    speaker = {
                        'name' : t['name'],
                        'img' : t['img'],
                        'introduction' : t['introduction'],
                        'position' : t['position'],
                        'organization' : t['organization'],
                    }
                    response = run_flash_model(speaker)
                    print(response)
                    json_response = json.loads(response[8:-4])
                    print(json_response)
                    speaker['history'] = json_response
                    
                    json_speakers[t['name']] = speaker
                    speakers.append(t['name'])
                    with open('./speakers.json', 'w', encoding='utf-8') as wj :
                        json.dump(json_speakers, wj, default=str, ensure_ascii=False)
                    
                    with open('./speakers.pickle', 'wb') as wp :
                        pickle.dump(speakers, wp)

                    success = True
                    break

                except ServerError as e :
                    if "503" in str(e):
                        wait_time = (2 ** i) + 5  # 5, 7, 9... 조금 더 여유있게 대기
                        print(f"서버 과부하(503). {wait_time}초 후 다시 시도합니다... (시도 {i+1}/5)")
                        time.sleep(wait_time)
                    else:
                        # 503 이외의 심각한 에러는 바로 중단
                        print(f"예상치 못한 서버 에러 발생: {e}")
                        raise e
                # except Exception as e:
                #     print(f"기타 에러 발생: {e}")
            if not success:
                print(f"⚠️ {idx}번째 데이터는 여러 번의 시도 끝에 실패했습니다.")
                break
            
            time.sleep(2)

